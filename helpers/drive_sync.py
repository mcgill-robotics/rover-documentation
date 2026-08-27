"""
drive_sync.py — Google Drive -> local staging/ mirror for the
McGill Robotics rover-documentation site.

WHAT THIS DOES EVERY RUN
  1. Wipes and rebuilds staging/ from scratch so it exactly mirrors
     Drive's CURRENT structure. If something was deleted from Drive,
     it's simply absent from the rebuilt staging/ -- no separate
     "handle deletions" logic needed.
  2. Uses a persistent cache/ directory (never wiped) keyed by Drive
     file ID. A file is only re-exported/re-converted if its
     modifiedTime changed since the last run; otherwise the previous
     conversion is copied straight from cache/ into staging/. This
     keeps API + pandoc/LibreOffice calls limited to what actually
     changed, even though the folder listing itself is re-walked
     every run (that part is cheap metadata-only calls).
  3. No underscore filtering happens here -- everything found inside
     a synced folder gets synced. Underscore-based selection of what
     goes LIVE on the site happens later, in publish_staging.py.

TWO CONTENT SHAPES

  DEPARTMENTS (-> docs/<slug>/, folded into the "Documentation" tab):
      <Department>/                <- e.g. "Electrical"
          Tutorials/                <- not ALL-CAPS -> SKIPPED
          POWER/                    <- ALL-CAPS -> SYNCED (a category)
              <anything>/               everything inside, any casing,
                                         is included recursively

  HANDBOOKS (-> docs/handbook/<slug>/, powers the separate "Handbook" tab):
      <Handbook root>/             <- e.g. "Elec Handbook"
          Any Subfolder/            <- ALWAYS synced (a "subtab"/category,
                                        no ALL-CAPS filter -- a handbook's
                                        subfolders are already a deliberately
                                        curated table of contents)
              <anything>/               everything inside, any casing,
                                         is included recursively
"""
import re, io, json, shutil, subprocess, hashlib, base64, zipfile
from pathlib import Path
from PIL import Image
import numpy as np
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from googleapiclient.errors import HttpError

# ---------------------------------------------------------------- settings
SCOPES = ['https://www.googleapis.com/auth/drive.readonly']
SERVICE_ACCOUNT_FILE = 'credentials.json'

# Each entry: display name -> Drive folder ID for that department's own
# folder (NOT a shared "Documentation" parent folder). Point directly at
# each department -- avoids relying on folder-sharing permissions
# propagating down through an extra level you haven't set up/shared.
# Add more departments here later, e.g. 'Mechanical': '...ID...'.
DEPARTMENTS = {
    'Electrical': '1iqUM0cXgjagoZwO95iYEpEQeOBBlGwUK',  # <-- Electrical's own folder ID
}

# Same idea, but for handbook-style content -- every direct subfolder of a
# handbook root becomes a sidebar category ("subtab") with NO ALL-CAPS
# filtering. Add more handbook roots here later the same way, e.g.
# 'Mech Handbook': '...ID...'. All handbook roots live together under the
# single "Handbook" navbar tab (see handbookSidebar in sidebars.ts).
HANDBOOKS = {
    'Elec Handbook': '1RyqQCgMESoat4u__m2uzVGwy9QVg4YTv',  # <-- grab from the folder's Drive URL
}

HARNESSING = {
    'Harnessing': '1i8_CjQ1qllqLwsCzIGsqnZ8GuKQ6loni'
}

STAGING_DIR = Path('staging')       # wiped + rebuilt every run
CACHE_DIR = Path('cache')           # persistent, never wiped
MANIFEST_PATH = Path('sync_manifest.json')

DOC_MIME = 'application/vnd.google-apps.document'
SLIDES_MIME = 'application/vnd.google-apps.presentation'
DRAWING_MIME = 'application/vnd.google-apps.drawing'
FOLDER_MIME = 'application/vnd.google-apps.folder'
DOCX_MIME = 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
XLSX_MIME = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'

creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
drive = build('drive', 'v3', credentials=creds)


# ------------------------------------------------------------- Drive I/O
def list_children(folder_id):
    results, page_token = [], None
    while True:
        resp = drive.files().list(
            q=f"'{folder_id}' in parents and trashed = false",
            fields="nextPageToken, files(id, name, mimeType, modifiedTime)",
            pageToken=page_token,
            pageSize=1000,
        ).execute()
        results.extend(resp['files'])
        page_token = resp.get('nextPageToken')
        if not page_token:
            break
    return results


def _download_media(request):
    buf = io.BytesIO()
    downloader = MediaIoBaseDownload(buf, request)
    done = False
    while not done:
        _, done = downloader.next_chunk()
    return buf.getvalue()


def export_bytes(file_id, mime_type):
    return _download_media(drive.files().export_media(fileId=file_id, mimeType=mime_type))


def download_bytes(file_id):
    return _download_media(drive.files().get_media(fileId=file_id))


# ------------------------------------------------------------- naming helpers
def is_all_caps(name):
    letters = [c for c in name if c.isalpha()]
    return bool(letters) and name == name.upper()


def department_slug_and_label(name):
    slug = re.sub(r'[^a-zA-Z0-9]', '', name)
    if not slug:
        slug = 'department'
    slug = slug[0].lower() + slug[1:] + 'Documentation'
    return slug, f"{name} Documentation"


def handbook_slug_and_label(name):
    """Like department_slug_and_label, but doesn't force-append a suffix --
    a handbook root's Drive name (e.g. "Elec Handbook") is already the
    label you want, and slugging needs real word-boundary camelCasing
    since these names are more often multi-word."""
    words = re.sub(r'[^A-Za-z0-9]+', ' ', name).strip().split()
    if not words:
        words = ['handbook']
    slug = words[0].lower() + ''.join(w.capitalize() for w in words[1:])
    return slug, name


def category_slug(name):
    slug = re.sub(r'[^a-zA-Z0-9]', '', name).lower()
    return slug or 'category'


def safe_filename(name):
    """Preserves a leading underscore -- that's meaningful for publish_staging.py."""
    return re.sub(r'\s+', '-', name.strip())


# ------------------------------------------------------------ image matching
# Same approach as the user's original script: hash match first, mean-squared
# error visual similarity as a fallback. Source of "real" images is now a
# .docx export of the same Google Doc (a .docx is a zip; images live under
# word/media/), since plain markdown base64 export was found unreliable.
def _load_image(img_bytes):
    return Image.open(io.BytesIO(img_bytes)).convert('RGB')


def _image_hash(img_bytes):
    """Hash of the DECODED PIXEL DATA, not the raw file bytes -- this is what
    makes matching work at all, since the same image re-encoded via base64
    markdown export vs. docx export rarely has byte-identical file contents
    even though the pixels are identical."""
    return hashlib.md5(_load_image(img_bytes).tobytes()).hexdigest()


def _image_mse(bytes_a, bytes_b):
    try:
        a = _load_image(bytes_a).resize((128, 128))
        b = _load_image(bytes_b).resize((128, 128))
        arr_a = np.asarray(a, dtype=np.float64)
        arr_b = np.asarray(b, dtype=np.float64)
        return float(np.mean((arr_a - arr_b) ** 2))
    except Exception:
        return float('inf')


def _extract_docx_images(docx_bytes):
    images = []
    with zipfile.ZipFile(io.BytesIO(docx_bytes)) as z:
        for name in z.namelist():
            if name.startswith('word/media/'):
                images.append((name.split('/')[-1], z.read(name)))
    return images


def _match_images(base64_images, docx_images):
    """base64_images: list of (ref, ext, bytes) parsed from the markdown export.
       docx_images: list of (filename, bytes) from the docx's word/media/.
       Returns {ref: matched_bytes}, falling back to the base64 bytes
       themselves if nothing in the docx matches well enough.

       Exact pixel-hash match is tried first (and, like the MSE fallback,
       only against docx images not already claimed by an earlier ref --
       otherwise two identical images in one doc could both get matched to
       the same docx file)."""
    remaining = list(docx_images)
    matches = {}

    for ref, ext, b64_bytes in base64_images:
        h = _image_hash(b64_bytes)
        exact = next((entry for entry in remaining if _image_hash(entry[1]) == h), None)
        if exact is not None:
            matches[ref] = exact[1]
            remaining.remove(exact)
            continue

        best, best_score = None, float('inf')
        for name, b in remaining:
            score = _image_mse(b64_bytes, b)
            if score < best_score:
                best, best_score = (name, b), score
        if best is not None and best_score < 2000:  # loose similarity threshold
            matches[ref] = best[1]
            remaining.remove(best)
        else:
            matches[ref] = b64_bytes  # give up, keep the base64 copy
    return matches


# ------------------------------------------------------------ per-type conversion
def remove_exported_tab_title(md_text: str, doc_name: str) -> str:
    """
    Remove the Google Docs tab title if Google Docs exported it as the
    first Markdown heading.

    The actual Google Drive file name is used by the sync system as the
    canonical document name, so the tab name should not become the
    Docusaurus page title.
    """
    lines = md_text.splitlines()

    # Find the first non-empty line.
    first = next(
        (i for i, line in enumerate(lines) if line.strip()),
        None
    )

    if first is None:
        return md_text

    line = lines[first].strip()

    # Google Docs Markdown export generally represents a title as # Title.
    if line.startswith('# '):
        exported_title = line[2:].strip()

        # Only remove it if it is NOT the actual Drive document name.
        # This prevents accidentally deleting a legitimate document title.
        if exported_title != doc_name.strip():
            lines.pop(first)

            # Remove the blank separator that commonly follows the heading.
            if first < len(lines) and not lines[first].strip():
                lines.pop(first)

            return '\n'.join(lines)

    return md_text

def convert_google_doc(file_id, dest_stem: Path, doc_name: str):
    md_text = export_bytes(file_id, 'text/markdown').decode('utf-8')

    # Google Docs can export the active tab's name as the first Markdown
    # heading. We don't want the tab name to become the Docusaurus title.
    # The Drive file name (doc_name) is the canonical document name.
    md_text = remove_exported_tab_title(md_text, doc_name)    
    md_text = f"---\ntitle: {doc_name}\n---\n\n" + md_text

    base64_images = re.findall(
        r'\[(image\d+)\]:\s*<data:image/(\w+);base64,([A-Za-z0-9+/=]+)>', md_text)
    base64_images = [(ref, ext, base64.b64decode(b64)) for ref, ext, b64 in base64_images]

    if base64_images:
        docx_images = []
        try:
            docx_bytes = export_bytes(file_id, DOCX_MIME)
            docx_images = _extract_docx_images(docx_bytes)
        except HttpError as e:
            if getattr(e.resp, 'status', None) == 403 and 'exportSizeLimitExceeded' in str(e):
                print("    [warn] doc too large for docx export (>10MB Drive limit) -- "
                      "falling back to embedded markdown images (lower quality)")
            else:
                raise

        matched = (_match_images(base64_images, docx_images) if docx_images
                   else {ref: b64_bytes for ref, ext, b64_bytes in base64_images})

        img_dir = dest_stem.parent / (dest_stem.name + '-img')
        img_dir.mkdir(parents=True, exist_ok=True)
        for ref, ext, _ in base64_images:
            img_filename = f"{ref}.{ext}"
            (img_dir / img_filename).write_bytes(matched[ref])
            md_text = md_text.replace(f'![][{ref}]', f'![]({img_dir.name}/{img_filename})')

    md_text = re.sub(r'\n\[image\d+\]:\s*<data:image/\w+;base64,[A-Za-z0-9+/=]+>', '', md_text)
    (dest_stem.parent / f"{dest_stem.name}.md").write_text(md_text, encoding='utf-8')


def convert_native_docx(file_bytes, dest_stem: Path):
    tmp_in = dest_stem.parent / f"__tmp_{dest_stem.name}.docx"
    tmp_in.write_bytes(file_bytes)
    img_dir = dest_stem.parent / (dest_stem.name + '-img')
    img_dir.mkdir(parents=True, exist_ok=True)
    md_path = dest_stem.parent / f"{dest_stem.name}.md"

    subprocess.run(
        ['pandoc', str(tmp_in), '-o', str(md_path), f'--extract-media={img_dir}'],
        check=True,
    )
    tmp_in.unlink()

    # Pandoc bakes the invocation-time --extract-media path (including the
    # cache/<file_id>/ prefix) into the image references it writes. That
    # path doesn't exist once this content is copied out of cache/ into
    # staging/ and then docs/ -- only img_dir's own name survives, sitting
    # as a sibling of the .md file. Rewrite refs to be relative to the .md
    # itself, matching how convert_google_doc builds its own paths.
    text = md_path.read_text(encoding='utf-8')
    text = text.replace(str(img_dir) + '/', img_dir.name + '/')
    md_path.write_text(text, encoding='utf-8')

def convert_native_xlsx(file_bytes, dest_stem: Path):
    tmp_in = dest_stem.parent / f"__tmp_{dest_stem.name}.xlsx"
    tmp_in.write_bytes(file_bytes)
    subprocess.run(
        ['soffice', '--headless', '--convert-to', 'pdf', '--outdir', str(dest_stem.parent), str(tmp_in)],
        check=True,
    )
    (dest_stem.parent / f"__tmp_{dest_stem.name}.pdf").rename(dest_stem.parent / f"{dest_stem.name}.pdf")
    tmp_in.unlink()


# ------------------------------------------------------------ cache <-> staging
def cache_path_for(file_id):
    return CACHE_DIR / file_id


def copy_cached(file_id, dest_dir: Path):
    src = cache_path_for(file_id)
    for item in src.iterdir():
        dest = dest_dir / item.name
        if item.is_dir():
            shutil.copytree(item, dest, dirs_exist_ok=True)
        else:
            shutil.copy2(item, dest)


def refresh_cache_and_copy(item, dest_dir: Path):
    file_id, name, mime = item['id'], item['name'], item['mimeType']
    cdir = cache_path_for(file_id)
    if cdir.exists():
        shutil.rmtree(cdir)
    cdir.mkdir(parents=True)

    stem = cdir / safe_filename(name)

    if mime == DOC_MIME:
        print(f"  [convert] doc: {name}")
        convert_google_doc(file_id, stem, name)    
    elif mime == SLIDES_MIME:
        print(f"  [convert] slides -> pdf: {name}")
        (cdir / f"{safe_filename(name)}.pdf").write_bytes(export_bytes(file_id, 'application/pdf'))
    elif mime == DRAWING_MIME:
        print(f"  [convert] drawing -> png: {name}")
        (cdir / f"{safe_filename(name)}.png").write_bytes(export_bytes(file_id, 'image/png'))
    elif mime == DOCX_MIME:
        print(f"  [convert] native docx: {name}")
        convert_native_docx(download_bytes(file_id), stem)
    elif mime == XLSX_MIME:
        print(f"  [convert] native xlsx -> pdf: {name}")
        convert_native_xlsx(download_bytes(file_id), stem)
    else:
        print(f"  [download] {name}")
        suffix = Path(name).suffix
        base = safe_filename(Path(name).stem)
        (cdir / f"{base}{suffix}").write_bytes(download_bytes(file_id))

    copy_cached(file_id, dest_dir)


def sync_file(item, dest_dir: Path, manifest):
    file_id = item['id']
    prev = manifest.get(file_id)
    if prev and prev.get('modifiedTime') == item['modifiedTime'] and cache_path_for(file_id).exists():
        copy_cached(file_id, dest_dir)
    else:
        refresh_cache_and_copy(item, dest_dir)
    manifest[file_id] = {'name': item['name'], 'modifiedTime': item['modifiedTime']}


# ------------------------------------------------------------ folder walk
def sync_category_folder(folder_id, dest_dir: Path, manifest):
    """Inside a synced folder (an ALL-CAPS department category, or a
    handbook subtab): sync everything, any casing, recursively.
    A failure on any single file is caught and logged rather than aborting the
    whole run -- that file is simply left out of the manifest, so it's retried
    (and, if it keeps failing, keeps getting logged) on the next run."""
    dest_dir.mkdir(parents=True, exist_ok=True)
    for item in list_children(folder_id):
        if item['mimeType'] == FOLDER_MIME:
            sync_category_folder(item['id'], dest_dir / safe_filename(item['name']), manifest)
        else:
            try:
                sync_file(item, dest_dir, manifest)
            except Exception as e:
                print(f"  [error] failed to sync '{item['name']}': {e}")
                print("          skipping this file -- will retry next run")


def sync_department_folder(folder_id, dept_name, staging_dir: Path, manifest):
    slug, label = department_slug_and_label(dept_name)
    dept_dest = staging_dir / slug
    dept_dest.mkdir(parents=True, exist_ok=True)
    (dept_dest / '_category_.json').write_text(json.dumps({"label": label, "position": 10}, indent=2))

    for item in list_children(folder_id):
        if item['mimeType'] != FOLDER_MIME or not is_all_caps(item['name']):
            continue  # only ALL-CAPS category folders one level under a department sync
        cat_dest = dept_dest / category_slug(item['name'])
        cat_dest.mkdir(parents=True, exist_ok=True)
        (cat_dest / '_category_.json').write_text(
            json.dumps({"label": item['name'].title(), "position": 10}, indent=2))
        sync_category_folder(item['id'], cat_dest, manifest)


def sync_handbook_folder(folder_id, handbook_name, staging_dir: Path, manifest):
    """A handbook root's direct subfolders each become a sidebar category
    (a "subtab") -- unlike sync_department_folder, there's no ALL-CAPS
    filter: a handbook's subfolders are already a deliberately curated
    table of contents, not a mixed bag needing a filter. Multiple handbook
    roots (if added to HANDBOOKS later) all nest under docs/handbook/, so
    they share the single "Handbook" navbar tab automatically."""
    slug, label = handbook_slug_and_label(handbook_name)
    hb_dest = staging_dir / 'electricalHandbook'
    hb_dest.mkdir(parents=True, exist_ok=True)
    (hb_dest / '_category_.json').write_text(json.dumps({"label": label, "position": 10}, indent=2))

    for item in list_children(folder_id):
        if item['mimeType'] != FOLDER_MIME:
            print(f"  [skip] file directly in handbook root (expected a subfolder): {item['name']}")
            continue
        cat_dest = hb_dest / category_slug(item['name'])
        cat_dest.mkdir(parents=True, exist_ok=True)
        (cat_dest / '_category_.json').write_text(
            json.dumps({"label": item['name'].title(), "position": 10}, indent=2))
        sync_category_folder(item['id'], cat_dest, manifest)


def sync_harnessing_folder(folder_id, staging_dir: Path, manifest):
    """
    Sync the Harnessing Drive root directly into staging/harnessing/.

    Every folder and file is preserved recursively so the Docusaurus
    autogenerated sidebar follows the Google Drive structure.
    """
    harness_dest = staging_dir / 'harnessing'
    harness_dest.mkdir(parents=True, exist_ok=True)

    for item in list_children(folder_id):
        if item['mimeType'] == FOLDER_MIME:
            folder_dest = harness_dest / safe_filename(item['name'])
            folder_dest.mkdir(parents=True, exist_ok=True)

            (folder_dest / '_category_.json').write_text(
                json.dumps(
                    {
                        "label": item['name'],
                        "position": 10
                    },
                    indent=2
                )
            )

            sync_category_folder(item['id'], folder_dest, manifest)

        else:
            try:
                sync_file(item, harness_dest, manifest)
            except Exception as e:
                print(f"  [error] failed to sync '{item['name']}': {e}")
                print("          skipping this file -- will retry next run")


def load_manifest():
    return json.loads(MANIFEST_PATH.read_text()) if MANIFEST_PATH.exists() else {}


def save_manifest(manifest):
    MANIFEST_PATH.write_text(json.dumps(manifest, indent=2))


def main():
    if STAGING_DIR.exists():
        shutil.rmtree(STAGING_DIR)
    STAGING_DIR.mkdir(parents=True)
    CACHE_DIR.mkdir(parents=True, exist_ok=True)

    manifest = load_manifest()

    for dept_name, folder_id in DEPARTMENTS.items():
        print(f"Department: {dept_name}")
        sync_department_folder(folder_id, dept_name, STAGING_DIR, manifest)

    for hb_name, folder_id in HANDBOOKS.items():
        print(f"Handbook: {hb_name}")
        sync_handbook_folder(folder_id, hb_name, STAGING_DIR, manifest)

    for harness_name, folder_id in HARNESSING.items():
        print(f"Harnessing: {harness_name}")
        sync_harnessing_folder(folder_id, STAGING_DIR, manifest)

    save_manifest(manifest)
    print("Done -- staging/ rebuilt from current Drive contents.")


if __name__ == '__main__':
    main()
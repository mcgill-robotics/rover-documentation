"""
publish_staging.py — walks staging/ (rebuilt fresh by drive_sync.py every
run) and copies content into the live repo's docs/ tree. _category_.json
files and plain ALL-CAPS category folders always pass through unchanged.

UNDERSCORE TOGGLE
  REQUIRE_UNDERSCORE = True  (default): only items whose name DONT start with
    "_" get published, everything else stays synced-and-cached in staging/ but off the site.
  REQUIRE_UNDERSCORE = False: publish everything found in staging/, no
    filtering. Can also be set per-run without editing the file:
      SYNC_REQUIRE_UNDERSCORE=0 ./run_sync.sh

Because staging/ is a full, current rebuild of Drive every run, and this
script re-derives docs/<department>/ from scratch (deleting anything that
no longer has a match in staging/), deletions in Drive propagate all the
way to the published site automatically -- and get called out in the
email report below.

EMAIL REPORT
  After publishing, emails EMAIL_TO a plain-text changelog of what was
  added/updated/removed this run. Requires SYNC_SMTP_PASSWORD to be set
  as an environment variable (never hardcode a password in this file).
  For Gmail: use an App Password, not your normal login password
  (https://myaccount.google.com/apppasswords). Set SEND_EMAIL_REPORT to
  False to disable entirely.

Run by run_sync.sh right after drive_sync.py.
"""
import os
import shutil
import smtplib
import re
from datetime import datetime
from email.message import EmailMessage
from pathlib import Path

STAGING_DIR = Path('staging')
# Adjust if your two project folders aren't siblings under ~/dev/
DOCS_DEST = Path('../rover-documentation/docs')

#REQUIRE_UNDERSCORE = os.environ.get('SYNC_REQUIRE_UNDERSCORE', '1') != '0'
REQUIRE_UNDERSCORE = 0
# --- email report settings ---
SEND_EMAIL_REPORT = True
EMAIL_TO = 'seth.wick31@gmail.com'  # <-- set this to where the changelog should go
EMAIL_FROM = os.environ.get('SYNC_SMTP_USER', EMAIL_TO)
SMTP_SERVER = os.environ.get('SYNC_SMTP_SERVER', 'smtp.gmail.com')
SMTP_PORT = int(os.environ.get('SYNC_SMTP_PORT', '465'))
SMTP_USER = os.environ.get('SYNC_SMTP_USER', EMAIL_FROM)
SMTP_PASSWORD = os.environ.get('SYNC_SMTP_PASSWORD')  # export this in your shell, DONT hardcode it


def dest_name(name: str):
    """Returns the published filename/dirname, or None if this item
    should be skipped."""
    if name == '_category_.json':
        return name

    stem, suffix = Path(name).stem, Path(name).suffix

    # Images/folders ending in -img
    if stem.endswith('-img'):
        base = stem[:-len('-img')]

        # Underscore-prefixed -img items are hidden
        if base.startswith('_'):
            return None if REQUIRE_UNDERSCORE else base[1:] + '-img'

        return base + '-img'

    # Underscore-prefixed files are hidden
    if stem.startswith('_'):
        return None if REQUIRE_UNDERSCORE else stem[1:] + suffix

    # Normal files are published
    return stem + suffix


def sanitize_mdx_braces(text: str) -> str:
    """MDX parses top-level '{...}' outside code as JS expressions. Content
    synced from Google Docs/Word often has stray braces in plain prose
    (e.g. pasted shell/CMake snippets not wrapped in code fences), which
    breaks the build. Escape braces everywhere EXCEPT inside fenced
    (```...```) or inline (`...`) code, where MDX already treats them as
    literal text."""
    def escape_plain(segment: str) -> str:
        return segment.replace('{', '\\{').replace('}', '\\}')

    # split on fenced code blocks first, leave those untouched entirely
    fence_parts = re.split(r'(```[\s\S]*?```)', text)
    for i, part in enumerate(fence_parts):
        if part.startswith('```'):
            continue
        # within non-fenced text, also protect inline `code spans`
        inline_parts = re.split(r'(`[^`\n]*`)', part)
        for j, sp in enumerate(inline_parts):
            if sp.startswith('`') and sp.endswith('`') and len(sp) > 1:
                continue
            inline_parts[j] = escape_plain(sp)
        fence_parts[i] = ''.join(inline_parts)
    return ''.join(fence_parts)

def publish_dir(src: Path, dest: Path, rel_prefix: str = ""):
    """Returns (added, updated, removed) -- lists of relative path strings,
    for the email changelog. Only real content files are logged (not
    _category_.json, not -img folders) to keep the report readable."""
    dest.mkdir(parents=True, exist_ok=True)
    keep_names = set()
    added, updated, removed = [], [], []

    # Figure out renames first (needed to fix image links inside .md files
    # in the same pass, e.g. "_Overview-img" -> "Overview-img")
    rename_map = {}
    for item in src.iterdir():
        if item.is_dir():
            out_name = dest_name(item.name)
            if out_name is None:
                out_name = item.name  # plain folder (e.g. an ALL-CAPS category) passes through
            if out_name != item.name:
                rename_map[item.name] = out_name

    for item in src.iterdir():
        if item.is_dir():
            out_name = rename_map.get(item.name, item.name)
            keep_names.add(out_name)
            c_added, c_updated, c_removed = publish_dir(
                item, dest / out_name, f"{rel_prefix}{out_name}/")
            added += c_added
            updated += c_updated
            removed += c_removed
        else:
            out_name = dest_name(item.name)
            if out_name is None:
                continue
            keep_names.add(out_name)
            dest_path = dest / out_name
            is_new = not dest_path.exists()

            if item.suffix == '.md':
                text = item.read_text(encoding='utf-8')
                for old, new in rename_map.items():
                    text = text.replace(old + '/', new + '/')
                text = sanitize_mdx_braces(text)   # <-- replaces ensure_md_format_frontmatter
                dest_path.write_text(text, encoding='utf-8')
            else:
                shutil.copy2(item, dest_path)

            if out_name != '_category_.json' and not out_name.endswith('-img'):
                label = f"{rel_prefix}{out_name}"
                (added if is_new else updated).append(label)

    # prune anything in dest that no longer exists in this staging run
    for existing in dest.iterdir():
        if existing.name not in keep_names:
            if existing.name != '_category_.json' and not existing.name.endswith('-img'):
                removed.append(f"{rel_prefix}{existing.name}")
            if existing.is_dir():
                shutil.rmtree(existing)
            else:
                existing.unlink()

    return added, updated, removed


def send_email_report(added, updated, removed):
    if not SEND_EMAIL_REPORT:
        return
    if not SMTP_PASSWORD:
        print("SYNC_SMTP_PASSWORD not set -- skipping email report.")
        return

    lines = [f"Rover docs sync report -- {datetime.now():%Y-%m-%d %H:%M}", ""]
    if not (added or updated or removed):
        lines.append("No changes this run.")
    else:
        if added:
            lines.append(f"Added ({len(added)}):")
            lines += [f"  + {p}" for p in added]
            lines.append("")
        if updated:
            lines.append(f"Updated ({len(updated)}):")
            lines += [f"  ~ {p}" for p in updated]
            lines.append("")
        if removed:
            lines.append(f"Removed ({len(removed)}):")
            lines += [f"  - {p}" for p in removed]

    msg = EmailMessage()
    msg['Subject'] = f"Rover docs sync -- {len(added)} added, {len(updated)} updated, {len(removed)} removed"
    msg['From'] = EMAIL_FROM
    msg['To'] = EMAIL_TO
    msg.set_content('\n'.join(lines))

    try:
        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
            server.login(SMTP_USER, SMTP_PASSWORD)
            server.send_message(msg)
        print(f"Emailed report to {EMAIL_TO}")
    except Exception as e:
        print(f"Failed to send email report: {e}")


def main():
    if not STAGING_DIR.exists():
        raise SystemExit("staging/ not found -- run drive_sync.py first.")

    all_added, all_updated, all_removed = [], [], []
    for dept_dir in STAGING_DIR.iterdir():
        if not dept_dir.is_dir():
            continue
        print(f"Publishing: {dept_dir.name}")
        added, updated, removed = publish_dir(dept_dir, DOCS_DEST / dept_dir.name, f"{dept_dir.name}/")
        all_added += added
        all_updated += updated
        all_removed += removed

    print(f"Done -- {len(all_added)} added, {len(all_updated)} updated, {len(all_removed)} removed.")
    send_email_report(all_added, all_updated, all_removed)


if __name__ == '__main__':
    main()
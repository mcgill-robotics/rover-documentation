import os
import re
import zipfile
import base64
import hashlib
from pathlib import Path
from PIL import Image
from io import BytesIO
import numpy as np


def validate_file_paths(md_path, zip_path):
    md_file = Path(md_path)
    zip_file = Path(zip_path)

    if md_file.suffix != '.md' or zip_file.suffix != '.zip':
        raise ValueError("One file must be a .md file and the other a .zip file.")

    if md_file.stem != zip_file.stem:
        raise ValueError("The files must have the same name, excluding the extension.")


def extract_images_from_zip(zip_path):
    images = {}
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        for file_name in zip_ref.namelist():
            if file_name.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
                with zip_ref.open(file_name) as file:
                    img = Image.open(file).convert('RGB')
                    images[file_name] = img
                    # print(f"Displaying: {file_name}")
                    # img.show(title=file_name)  # Opens image in viewer
    print(f"Total images in zip : {len(images)}")
    return images

def parse_markdown(md_path):
    with open(md_path, 'r', encoding='utf-8') as file:
        content = file.read()

    image_refs = re.findall(r'!\[\]\[(image\d+)\]', content)
    base64_images = re.findall(r'\[(image\d+)\]:\s*<data:image/\w+;base64,([A-Za-z0-9+/=]+)>', content)

    print(f"Total images in markdown : {len(image_refs)}")
    return content, image_refs, base64_images

def save_base64_images(base64_images):
    saved_images = {}
    for ref, b64_data in base64_images:
        img_data = base64.b64decode(b64_data)
        img = Image.open(BytesIO(img_data)).convert('RGB')
        img_hash = hashlib.md5(img.tobytes()).hexdigest()
        saved_images[img_hash] = (ref, img)
    return saved_images

def image_difference(img1, img2):
    """Return mean squared error (MSE) between two images."""
    img1 = img1.resize((128, 128))
    img2 = img2.resize((128, 128))
    arr1 = np.asarray(img1).astype("float32")
    arr2 = np.asarray(img2).astype("float32")
    return np.mean((arr1 - arr2) ** 2)

def match_images(zip_images, md_images):
    matched = {}
    used_zip_keys = set()

    for md_hash, (ref, md_img) in md_images.items():
        md_bytes = md_img.tobytes()
        best_match = None
        best_score = float('inf')

        for zip_key, zip_img in zip_images.items():
            if zip_key in used_zip_keys:
                continue

            if hashlib.md5(zip_img.tobytes()).hexdigest() == md_hash:
                best_match = zip_key
                break

            score = image_difference(md_img, zip_img)
            if score < best_score:
                best_score = score
                best_match = zip_key

        if best_match is not None:
            matched[ref] = (best_match, zip_images[best_match])
            used_zip_keys.add(best_match)
        else:
            raise ValueError(f"No suitable image match found for {ref} in Markdown.")

    return matched

def update_markdown(content, matches, output_folder):
    # Remove all hex image references
    content = re.sub(r'\n\[image\d+\]:\s*<data:image/\w+;base64,[A-Za-z0-9+/=]+>', '', content)

    for ref, (filename, _) in matches.items():
        filename = os.path.basename(filename)
        content = content.replace(f'![][ {ref} ]', f'![]({output_folder}/{filename})')
        content = content.replace(f'![][{ref}]', f'![]({output_folder}/{filename})')  # if brackets are tight

    return content

def save_images(output_folder, matches, md_path):
    # print(f"thjdklkjhgfhjkl{Path(md_path).parent}, __++__ {output_folder}")
    os.makedirs(os.path.join(Path(md_path).parent,output_folder), exist_ok=True)
    for ref, (filepath, img) in matches.items():
        filename = os.path.basename(filepath)
        # print(f"thisdaw{filename}") #optimized this is not
        path = os.path.join(output_folder, filename)
        # print(f"thisdaw{path}")
        path = os.path.join(Path(md_path).parent, path)
        # print(f"thisdaw{path}")
        img.save(path)

def process_markdown_and_zip(md_path: str, zip_path: str):
    validate_file_paths(md_path, zip_path)

    zip_images = extract_images_from_zip(zip_path)
    content, image_refs, base64_images = parse_markdown(md_path)
    md_images = save_base64_images(base64_images)
    matches = match_images(zip_images, md_images)

    output_folder = Path(md_path).stem.replace(' ', '-') + "-img"
    print(Path(md_path))
    print(f"Saving images to: {output_folder}")
    save_images(output_folder, matches, md_path)

    updated_content = update_markdown(content, matches, output_folder)
    # Create a new file with the same name in the new folder

    # output_folder = Path(md_path).stem.replace(' ', '-')
    # print(output_folder)
    output_folder_path = Path(md_path).parent
    print(output_folder_path)

    # Create the output folder if it doesn't exist
    output_folder_path.mkdir(parents=True, exist_ok=True)

    new_md_path = output_folder_path / Path(md_path).name.replace(' ', '-')
    with open(new_md_path, 'w', encoding='utf-8') as file:
        file.write(updated_content)


# Example usage
md_path = 'rover-documentation\python\ROCKER SUSPENSION-DRIVE-Mechanical-Documentation.md'
zip_path = 'rover-documentation\python\ROCKER SUSPENSION-DRIVE-Mechanical-Documentation.zip'
process_markdown_and_zip(md_path, zip_path)

import fitz
import os
import json
import re

pdf_path = "lmobile.pdf"
output_folder = "images_extraites"
os.makedirs(output_folder, exist_ok=True)

doc = fitz.open(pdf_path)
image_list = []
img_counter = [1]

def save_image(doc, xref, page_index=None):
    if not isinstance(xref, int):
        return
    try:
        img_info = doc.extract_image(xref)
    except Exception:
        return
    if img_info:
        img_bytes = img_info["image"]
        img_ext = img_info["ext"]
        if page_index is not None:
            filename = f"page{page_index+1:03d}_img{img_counter[0]:05d}.{img_ext}"
        else:
            filename = f"img{img_counter[0]:05d}.{img_ext}"
        path = os.path.join(output_folder, filename)
        with open(path, "wb") as f:
            f.write(img_bytes)
        image_list.append({
            "image_name": filename,
            "page": page_index + 1 if page_index is not None else None,
            "extension": img_ext,
            "path": path,
        })
        img_counter[0] += 1

def extract_xref_images(doc, xref, page_index=None, visited=None):
    if visited is None:
        visited = set()
    if xref in visited:
        return
    visited.add(xref)

    try:
        obj = doc.xref_object(xref, compressed=True)
    except Exception:
        return

    # Sauvegarder image si possible
    save_image(doc, xref, page_index)

    # Trouver récursivement d'autres XObjects
    # Les Form XObjects contiennent souvent "/XObject" suivi d'un numéro de référence
    xrefs_found = re.findall(r"/XObject\s+(\d+)\s+0\s+R", obj)
    for ref_str in xrefs_found:
        try:
            ref = int(ref_str)
            extract_xref_images(doc, ref, page_index, visited)
        except Exception:
            continue

def extract_images_from_page(doc, page_index):
    page = doc[page_index]

    # 1. Images classiques référencées par get_images()
    for img in page.get_images(full=True):
        xref = img[0]
        extract_xref_images(doc, xref, page_index)

    # 2. Images dans les annotations
    annots = page.annots()
    if annots:
        for annot in annots:
            if annot.type[0] == 8:  # image annotation
                info = annot.get_image_info()
                xref = info.get("xref")
                if isinstance(xref, int):
                    extract_xref_images(doc, xref, page_index)

    # 3. Images dans les blocs de texte (type 1 = image)
    blocks = page.get_text("dict").get("blocks", [])
    for b in blocks:
        if b.get("type") == 1:  # bloc image
            xref = b.get("image")
            if isinstance(xref, int):
                extract_xref_images(doc, xref, page_index)

def extract_all_images(doc):
    for i in range(len(doc)):
        extract_images_from_page(doc, i)

extract_all_images(doc)

with open("liste_images.json", "w", encoding="utf-8") as f:
    json.dump(image_list, f, indent=4, ensure_ascii=False)

print(f"✅ {len(image_list)} images extraites.")
print("📄 Liste enregistrée dans liste_images.json")

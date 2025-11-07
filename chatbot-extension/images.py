import fitz  # PyMuPDF
import os
import re

# === CONFIGURATION ===
pdf_path = "lmobile.pdf"
output_dir = "images_titre_associe"
os.makedirs(output_dir, exist_ok=True)

def clean_filename(text):
    """Nettoie un texte pour l’utiliser comme nom de fichier"""
    text = re.sub(r"[^\w\s-]", "", text)  # supprime symboles
    text = re.sub(r"\s+", "-", text.strip())  # espaces → tirets
    return text[:40].lower()  # max 40 caractères

def get_closest_title(blocks, image_y0):
    """Trouve le titre/sous-titre le plus proche au-dessus de l’image"""
    candidate = ""
    max_font = 0
    min_distance = float("inf")

    for block in blocks:
        if block["type"] != 0:
            continue  # uniquement texte
        y1 = block["bbox"][3]
        if y1 >= image_y0:
            continue  # le bloc est en dessous

        for line in block["lines"]:
            for span in line["spans"]:
                font_size = span.get("size", 0)
                if font_size >= max_font:
                    distance = image_y0 - y1
                    if distance < min_distance:
                        min_distance = distance
                        candidate = span["text"]
                        max_font = font_size
    return clean_filename(candidate) if candidate else None

def extract_images_with_titles(pdf_path):
    doc = fitz.open(pdf_path)
    total = 0

    for page_num, page in enumerate(doc):
        images = page.get_images(full=True)
        blocks = page.get_text("dict")["blocks"]

        for i, img in enumerate(images):
            xref = img[0]
            try:
                base_image = doc.extract_image(xref)
                image_bytes = base_image["image"]
                image_ext = base_image["ext"]
            except:
                continue

            bbox = fitz.Rect(img[1], img[2], img[3], img[4]) if len(img) >= 5 else None
            image_y0 = bbox.y0 if bbox else 0

            title = get_closest_title(blocks, image_y0)
            if not title:
                title = f"image{page_num+1}_{i+1}"

            filename = f"page{page_num+1:02d}-{title}.{image_ext}"
            filepath = os.path.join(output_dir, filename)

            with open(filepath, "wb") as f:
                f.write(image_bytes)
            total += 1

    print(f"✅ {total} images extraites avec titres associés.")

# === LANCEMENT ===
extract_images_with_titles(pdf_path)

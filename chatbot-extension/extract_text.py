from PyPDF2 import PdfReader

# Ouvre le fichier PDF
reader = PdfReader("lmobile.pdf")
with open("lmobile_extracted.txt", "w", encoding="utf-8") as f:
    for page in reader.pages:
        f.write(page.extract_text() + "\n")

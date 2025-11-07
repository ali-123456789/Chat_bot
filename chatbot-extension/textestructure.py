import re

with open("output_text.txt", "r", encoding="utf-8") as file:
    raw_text = file.read()

# Supprimer les lignes trop courtes ou vides
lines = [line.strip() for line in raw_text.split("\n") if len(line.strip()) > 2]

# Regrouper les lignes en un seul bloc de texte
clean_text = "\n".join(lines)

# Ajouter une structure hiérarchique
# Exemple : "1 Purpose" => "# 1. Purpose"
clean_text = re.sub(r"(?m)^(\d{1,2})([^\d].+)$", r"# \1.\2", clean_text)

# Sous-titres du style "2.1 Required Basic Knowledge" => "## 2.1 Required Basic Knowledge"
clean_text = re.sub(r"(?m)^# (\d{1,2})\.(\d{1,2}) (.+)$", r"## \1.\2 \3", clean_text)

# Titres principaux = niveau 1
clean_text = re.sub(r"(?m)^# (\d{1,2}) (.+)$", r"# \1. \2", clean_text)

# Ajouter des sauts de ligne entre sections
clean_text = re.sub(r"(#+ .+)", r"\n\1\n", clean_text)

# Sauvegarder le fichier structuré
with open("structured_output.txt", "w", encoding="utf-8") as file:
    file.write(clean_text)

print("✅ Texte structuré sauvegardé dans structured_output.txt")

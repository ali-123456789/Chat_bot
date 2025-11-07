# main.py

import os
from dotenv import load_dotenv
from openai import OpenAI

# -------------------------
# Étape 1 : Charger la clé API
# -------------------------
load_dotenv()
client = OpenAI(api_key="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")

# -------------------------
# Étape 2 : Charger le fichier texte
# -------------------------
try:
    with open("structured_output.txt", "r", encoding="utf-8") as f:
        contenu = f.read()
except FileNotFoundError:
    print("Erreur : le fichier 'mon_fichier.txt' est introuvable.")
    exit()

# -------------------------
# Étape 3 : Fonction pour poser une question
# -------------------------
def poser_question(question):
    prompt = f"Voici le texte :\n{contenu}\n\nQuestion : {question}\nRéponse :"
    try:
        response = client.chat.completions.create(
            model="openai/gpt-oss-20b:free",
            messages=[
                {"role": "system", "content": "Tu es un assistant qui répond aux questions sur le texte fourni."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2,
            max_tokens=200
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Erreur lors de la requête au modèle : {e}"

# -------------------------
# Étape 4 : Interface console simple
# -------------------------
if __name__ == "__main__":
    print("Chatbot prêt ! Pose tes questions (tape 'quit' pour sortir).")
    
    while True:
        question = input("Vous : ")
        if question.lower() == "quit":
            print("Au revoir !")
            break
        
        reponse = poser_question(question)
        print("Chatbot :", reponse)

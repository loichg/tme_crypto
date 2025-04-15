import subprocess
import base64

# La chaîne chiffrée en base64
ciphertext_base64 = "U2FsdGVkX19ryc2viZbJFbaOKrivnNerfoadR6oGKH8GFhh7XsY2JTsmXOs+/gY1X4WsCd4wvuwQFMjCvjTn3w=="

# Votre mot de passe pour AES
password = "ISECR0XX"

# Décoder la chaîne base64
ciphertext = base64.b64decode(ciphertext_base64)

# Sauvegarder le texte chiffré dans un fichier temporaire
with open("encrypted.bin", "wb") as f:
    f.write(ciphertext)

# Utiliser openssl pour déchiffrer avec le mot de passe fourni
command = [
    "openssl", "enc", "-d", "-aes-128-cbc", "-pbkdf2", "-pass", f"pass:{password}", "-in", "encrypted.bin"
]

# Exécuter la commande openssl et récupérer la sortie
result = subprocess.run(command, capture_output=True, text=True)

# Afficher le résultat du déchiffrement
if result.returncode == 0:
    print(result.stdout)
else:
    print(f"Erreur : {result.stderr}")

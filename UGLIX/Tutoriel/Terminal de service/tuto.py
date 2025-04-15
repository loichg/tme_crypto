import subprocess

# Le message à chiffrer
message = 'I got it!'

# Chemin vers la clé publique (assurez-vous qu'elle est accessible depuis le script)
public_key_path = 'pki_tutorial.pem'

# Créer un fichier temporaire pour stocker le message
with open("message.txt", "w") as f:
    f.write(message)

# Commande OpenSSL pour chiffrer le message avec la clé publique
command = [
    "openssl", "pkeyutl", "-encrypt", "-pubin", "-inkey", public_key_path, "-in", "message.txt", "-out", "encrypted_message.bin"
]

# Exécution de la commande
subprocess.run(command)

# Lire le fichier chiffré et afficher en hexadécimal (comme avec xxd -p)
with open("encrypted_message.bin", "rb") as f:
    encrypted_message = f.read()
    print(encrypted_message.hex())

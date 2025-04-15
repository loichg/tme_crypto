import subprocess

# Écrire le texte dans un fichier challenge.txt
message = "stand drops torso fungi rules"
with open("challenge.txt", "w") as f:
    f.write(message)

# Calculer la signature SHA-256 avec la clé privée (private_key.pem)
private_key_path = 'private_key.pem'
signature_path = 'signature.bin'

# Exécuter la commande OpenSSL pour générer la signature
command_sign = [
    "openssl", "dgst", "-sha256", "-sign", private_key_path, "-out", signature_path, "challenge.txt"
]

subprocess.run(command_sign)

# Lire la signature et l'afficher en hexadécimal (comme xxd -p)
with open(signature_path, "rb") as f:
    signature = f.read()
    print(signature.hex())

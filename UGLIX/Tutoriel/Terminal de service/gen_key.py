import subprocess

# Générer la clé privée RSA (2048 bits)
private_key_path = 'private_key.pem'
command_genpkey = [
    "openssl", "genpkey", "-algorithm", "RSA", "-pkeyopt", "rsa_keygen_bits:2048", "-out", private_key_path
]

# Exécution de la commande pour générer la clé privée
subprocess.run(command_genpkey)

# Extraire la clé publique à partir de la clé privée
public_key_path = 'public_key.pem'
command_pubout = [
    "openssl", "pkey", "-in", private_key_path, "-pubout", "-out", public_key_path
]

# Exécution de la commande pour extraire la clé publique
subprocess.run(command_pubout)

# Affichage des chemins vers les fichiers générés
print(f"Clé privée générée : {private_key_path}")
print(f"Clé publique générée : {public_key_path}")

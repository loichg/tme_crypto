import subprocess

# Chemin vers la clé privée
private_key_path = 'private_key.pem'

# Chemin pour la sortie du certificat
certificate_path = 'certificate.pem'

# Générer un certificat en utilisant la clé privée et un sujet personnalisé
command = [
    "openssl", "req", "-new", "-key", private_key_path, "-subj", "/CN=loichg9", "-out", certificate_path
]

# Exécution de la commande pour générer le certificat
subprocess.run(command)

# Affichage du chemin vers le certificat généré
print(f"Certificat généré : {certificate_path}")

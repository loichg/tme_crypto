import subprocess

# Challenge défini directement
challenge = "picas decoy dived posed uncsp"

# Passer le challenge directement à OpenSSL via stdin
cmd = "openssl dgst -sha256 -hex -sign sk_atrium.pem"
process = subprocess.run(cmd, input=challenge, shell=True, capture_output=True, text=True)

# Affichage du résultat
print("Signature:")
print(process.stdout)

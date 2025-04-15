import subprocess
import base64

# On commence par decoder +++ATRIUM+++ en base64 
atrium_b64_dec = base64.b64decode(b"+++ATRIUM+++")

# Ajoutez les octets de bourrage
atrium_b64_dec = atrium_b64_dec +b'\x01'

# On convertis ensuite en int
atrium_int = int.from_bytes(atrium_b64_dec,byteorder='big') + ((256)*10**100)

# On va utiliser cet int pour créer une clé public contenant +++ATRIUM+++
keygen = f"openssl genpkey -algorithm RSA -out sk_atrium.pem -outform PEM  -pkeyopt rsa_keygen_pubexp:{atrium_int} -pkeyopt rsa_keygen_bits:2048 -pkeyopt rsa_keygen_primes:2"
keygen_run = subprocess.run(keygen, capture_output=True, shell=True)

# On va maintenant extraire la clé publique de la clé privée
pkey_extrac = "openssl pkey -in sk_atrium.pem -pubout -out pk_atrium.pem"

pkey_extrac_run = subprocess.run(pkey_extrac,shell=True,capture_output=True)

print("ERREURS :",pkey_extrac_run.stderr)
print("Sortie :",pkey_extrac_run.stdout)

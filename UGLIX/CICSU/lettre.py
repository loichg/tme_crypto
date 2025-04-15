import hashlib
import random
from Crypto.PublicKey import RSA
from Crypto.Util.number import bytes_to_long, long_to_bytes, inverse

# Charger la clé publique du directeur 
with open("pk_dir.pem", "rb") as f:
    pubkey = RSA.import_key(f.read())

N = pubkey.n
e = pubkey.e
key_size_bytes = (N.bit_length() + 7) // 8

print("[✔] Clé publique chargée")
print("N =", hex(N))
print("e =", e)

# Encodage PKCS#1 v1.5 
def pkcs1_v1_5_encode(msg: bytes, total_length: int) -> bytes:
    asn1_prefix = bytes.fromhex("3031300d060960864801650304020105000420")
    digest = hashlib.sha256(msg).digest()
    padding_len = total_length - len(asn1_prefix) - len(digest) - 3
    if padding_len < 8:
        raise ValueError("Le padding est trop court")
    return b'\x00\x01' + b'\xff' * padding_len + b'\x00' + asn1_prefix + digest

message = b"I, the lab director, hereby grant loichg9 permission to take the BiblioDrone-NG."
encoded_message = pkcs1_v1_5_encode(message, key_size_bytes)
M = bytes_to_long(encoded_message)

print("\n[✔] Message encodé (PKCS#1 v1.5) prêt pour signature")

# Générer x et masquer le message 
while True:
    x = random.randrange(2, N)
    try:
        x_inv = inverse(x, N)
        break
    except ValueError:
        continue  # x n'a pas d'inverse mod N, on recommence

x_e = pow(x, e, N)
M_masked = (M * x_e) % N

hex_input = hex(M_masked)[2:]

print("\nINPUT À ENVOYER AU LAPTOP (hex) :\n")
print(hex_input)

# Récupérer la "signature" du laptop 
print("\nRéponse du laptop :\n")
laptop_response = input("Laptop output (hex) : ").strip()
S_masked = int(laptop_response, 16)

# Démasquer 
S = (S_masked * x_inv) % N
signature_bytes = long_to_bytes(S)

# Sauvegarde et affichage 
with open("signature.bin", "wb") as f:
    f.write(signature_bytes)

with open("message.txt", "wb") as f:
    f.write(message)

print("\nSignature sauvegardée dans 'signature.bin'")
print("Message sauvegardé dans 'message.txt'")

# Affichage final 
print("\n Signature hex :\n")
print(signature_bytes.hex())

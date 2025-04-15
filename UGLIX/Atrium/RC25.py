from Crypto.PublicKey import RSA
from Crypto.Util.number import inverse

# Messages chiffrés
c1 = 0x8ad214bb97249b836e140497abbce1fb59b2a9b8d794dd53c80452ced92b8fa6c0aeba03dc059904214f7d3a8b8cf50f89764f576c46dd26cc97eb10a3961d24202bc0ffc753338e13d45abb0d072eb17747d6f6e61b9074cd6937d3df8dd369f3f72c5c9d2185cb99bc7a844083971e96568044bdcaf9d64579e65e2a2bf0e39fee6ab7a81933c2772d342ac12f77fc122bb92b181fe28ed5dc55a6f3eef18f039abd0efb379fe3218c5aa341c83e7e72e554f58a404b3d0dea38e4ddff24750e2b57577d7a3b630a3a097c39e40041c7bfd02ac446775bfe41406a9df7ba4d0630494611b89776bbcfd507df4e0f03c6c13c9ed6d223a93d899e97368698de
c2 = 0xad58111a8173e4d46123aacb1be9f40e393775e2adf3b20548cf40e6780a9ddac67c897099f5dcaefb7ed3df70f4d89063256a7426d6a535e4833a90e908a5d5a36239a821741299b22529daba18007f0c531e8121d427089bdfe36d0f2d344997cea1a74cd1d0de9e7e7f93c20d7170c99da3110668c640790401f699a64b2c8e1b4b2364f35c90557f76b4e2c34122e163dfb536a84d0e88603b4e9d02e4f07653bf60c00a9d7f537a1a232869b07ec85297903de9e7fc57fe2e1535c505d410e56b76febbb89db04c5de8cb0babc973361a3c5249d627c78fd99bd27d6d101f25b2c60bd09fbfc303b07f50ae88b40da835c3d95c8cc2654933e3cfa3e0a8

# Récupérer les exposants publics et le module N
with open("pk_belljose.pem", "r") as f_key_1:
    pkey1 = RSA.import_key(f_key_1.read())
    e1 = pkey1.e
    N = pkey1.n

with open("pk_felliott.pem", "r") as f_key_2:
    pkey2 = RSA.import_key(f_key_2.read())
    e2 = pkey2.e

# Vérifier que les modules N sont identiques
assert pkey1.n == pkey2.n, "Les modules N ne sont pas identiques !"

# Trouver une relation de Bézout entre e1 et e2
def extended_euclid_gcd(a, b):
    s, old_s = 0, 1
    t, old_t = 1, 0
    r, old_r = b, a

    while r != 0:
        quotient = old_r // r
        old_r, r = r, old_r - quotient * r
        old_s, s = s, old_s - quotient * s
        old_t, t = t, old_t - quotient * t

    return [old_r, old_s, old_t]

gcd, u, v = extended_euclid_gcd(e1, e2)

# Vérifier que gcd(e1, e2) == 1
assert gcd == 1, "Les exposants ne sont pas premiers entre eux !"

# Calculer le message m
m = (pow(c1, u, N) * pow(c2, v, N)) % N

# Convertir le message en bytes
message_bytes = m.to_bytes((m.bit_length() + 7) // 8, 'big')

# Afficher le message déchiffré
print("Message déchiffré (hex) :")
print(message_bytes.hex())

# Essayer de décoder en UTF-8
try:
    print("\nMessage déchiffré (texte) :")
    print(message_bytes.decode('utf-8'))
except UnicodeDecodeError:
    print("\nLe message déchiffré n'est pas du texte UTF-8 valide.")
    print("Il peut s'agir de données binaires ou d'un autre format.")


result = (pow(c1, u, pkey2.n) * pow(c2, v, pkey2.n)) % pkey2.n
result_hex = "027e894ffc8963635a4622f1c79130a4989b6ce510f9fa0ad21e8411d55bd6e601271d8c7cf989ae598aa0ed50efb3e11c60b56d6645d55cfdc58153724bd556532821785d6d8444d60c48d979815f9b9274ea3c3152aa9a226d81a871b8246e45dd43aeecc79506e059e3564485b9f8a37b1fffbcf5cf4c6151175102ba680a640ba1e992698b972e1d556779e65dc762daca1a0c0fb3ab55b2315907fe5ba443804de9873c5719bf53e064d60ec39a3175298cce5d018f35004e6f75766561752064696769636f6465206465206c612073616c6c652052432d3235203a206362333135383930343965396661326261376637636131623739636663626263"
# Convertir le résultat en une représentation binaire
binary_data = result.to_bytes((result.bit_length() + 7) // 8, 'big')

# Convertir la représentation binaire en hexadécimal par parties
result_hex_parts = [binary_data[i:i+8].hex() for i in range(0, len(binary_data), 8)]

# Concaténer les parties hexadécimales pour obtenir le résultat complet
result_hex = ''.join(result_hex_parts)
bytes_hex = bytes.fromhex(result_hex)
print(bytes_hex)

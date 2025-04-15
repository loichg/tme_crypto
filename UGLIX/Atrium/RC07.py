import subprocess
import re
from Crypto.PublicKey import RSA
from Crypto.Util.number import inverse
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256

# Paramètres de la clé RSA
d1 = 0x5ba863d3a65ff7fec0bd400f0939cc57da81e84de98f398609cf4316d6c839814aeb9a2d12bbf380b734cb1131727a55a8f5f0fbe7294840d74175fbabbdbb433159d97a9168668dbc95707f3ef21561d92237a79127b3b9b7a8e8c6134199da6464c32bbf3003a6fbc41141781c75b0f86b59f2bfafb51fb7d8823a350226b13d09f098021eacac5f37d657a80494000a26791c75cb76fd9c4e88d0fe2e9f2d37e31c81571c300d8b4ea076ff8a5c9e01ddfab10f2a23f957f37635680b37ac53b679f15b14e9b0c976d0ce53f6bf22ae80a34c8f4e1d29a3c6b7be5f73af67e45f89a730abc54c47783c0b5f3c8f2ff873811f28fb4c8fb92c0f2e3fc79d81

# Récupération de N et e1
n = """
00:d5:6e:aa:cc:2c:de:0d:69:d5:5c:44:2e:cb:21:
0e:54:29:b5:1d:92:e3:7f:3a:ac:58:00:a4:19:5e:
7d:5d:d0:56:ff:19:f8:02:20:b1:f6:14:4b:e0:92:
e6:51:78:1d:73:86:18:3f:2b:ab:21:7d:5e:f0:47:
ba:dd:7e:cf:bc:4a:9b:46:30:2b:ed:5e:f0:f4:72:
b8:0c:7d:4f:dd:7d:ad:7c:7b:14:2a:11:b5:46:c9:
b6:71:04:a0:d3:35:90:69:54:58:43:1e:6b:8d:e5:
04:ca:1f:78:a4:b2:1b:09:ed:2c:db:75:28:16:69:
df:7f:1a:0a:e6:cb:3f:4d:49:e6:8d:e0:3b:21:43:
5b:73:ce:8a:ba:f7:31:22:6d:f0:83:2f:22:4f:6f:
a0:50:fe:59:f6:44:2a:ff:b0:67:65:8b:73:94:20:
de:a1:05:b2:b6:c0:bf:93:3a:43:a5:a5:b6:d0:0f:
84:b3:38:1a:b3:05:55:cc:1a:90:61:e3:8c:cf:3e:
dd:52:e9:65:c8:a2:be:9f:91:3a:5b:e1:45:27:e3:
d2:5c:c9:ec:d5:17:d5:cc:28:b2:3b:fb:63:98:0f:
bd:82:25:bb:d9:2c:1c:99:35:5b:90:3b:9c:c6:09:
c9:2e:0e:2b:a2:8a:87:3c:9d:22:ee:1f:1b:d1:97:
c8:5d
"""
hex_n = n.replace(":", "").replace("\n", "")
n_bytes = bytes.fromhex(hex_n)
n = int.from_bytes(n_bytes, byteorder="big")

e1 = """
00:d8:da:54:94:15:79:ba:d4:8a:81:8f:26:67:99:
60:03:00:00:00:00:00:00:3e:fb:e0:13:44:85:0c:
fb:ef:81
"""
hex_e1 = e1.replace(":", "").replace("\n", "")
e1_bytes = bytes.fromhex(hex_e1)
e1 = int.from_bytes(e1_bytes, byteorder='big')

# Factorisation de N
p = 156968060757818827265177531930705159229952770027782530961588407931417041072301652139585182730202726822366749899599693486372191868622630405264937575166949781285270733797193597315086158960572864794340610299237868609621291662180252122357433046477251776612798951223528942208726285851733459837684251331735730696403
q = 171648492356181927753703314961938758410712182153863812949142832315455471587001887067210300953057843004345887101227497941554963126862428595311516198158269909734896691597918961894447920993653899636567178216010708844617224520318434969249282759445374130433767011031476048633193321541207732997238472372077167862799

# Vérification de p et q
if p * q == n:
    print("p * q = n : succès")
else:
    print("Erreur : p * q != n")

# Récupération de e2
e2 = """
00:81:c4:33:59:4e:0b:42:dd:a1:d6:e6:4f:6f:c4:
8d:7f:00:00:00:00:00:00:3e:fb:e0:13:44:85:0c:
fb:ef:81
"""
hex_e2 = e2.replace(":", "").replace("\n", "")
e2_bytes = bytes.fromhex(hex_e2)
e2 = int.from_bytes(e2_bytes, byteorder='big')

# Calcul de d2
phi_n = (p - 1) * (q - 1)
d2 = inverse(e2, phi_n)

# Vérification de d2
if (e2 * d2) % phi_n == 1:
    print("d2 est correct")
else:
    print("Erreur : d2 est incorrect")

# Construction de la clé RSA
try:
    key2 = RSA.construct((n, e2, d2, p, q), consistency_check=True)
    print("Clé RSA valide")
except ValueError as e:
    print("Erreur dans la clé RSA :", e)

# Message à signer
message = b"lists taxer wrack buxom pipes"

# Calcul du hachage SHA-256
hash_obj = SHA256.new(message)

# Signature du message
signature = pkcs1_15.new(key2).sign(hash_obj)

# Vérification de la signature
try:
    pkcs1_15.new(key2.publickey()).verify(hash_obj, signature)
    print("Signature valide")
    print("Signature générée :", signature.hex())
except (ValueError, TypeError) as e:
    print("Signature invalide :", e)
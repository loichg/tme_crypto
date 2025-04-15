import subprocess

# Texte clair attendu 
clair = "crams ports foamy revue wryer"

# Charger le dictionnaire de mots de passe
with open("Dictionnaire.txt", "r") as fichier:
    for ligne in fichier:
        mot_de_passe = ligne.strip()  # Nettoyer le mot de passe

        # Déchiffrer le texte avec OpenSSL
        commande = f"echo \"U2FsdGVkX18h7nibLTqQ6h+DCzx/Bl6Q+vfs4XJpIsT4PpXks4cTtJoYkZKbfC9o\" | openssl enc -aes-128-cbc -d -a -pbkdf2 -pass pass:{mot_de_passe}"
        
        # Lancer la commande
        process = subprocess.run(commande, shell=True, capture_output=True)

        # Vérifier si le texte déchiffré correspond au texte clair attendu
        if process.returncode == 0:
            # Comparer le texte déchiffré avec le texte attendu (en binaire)
            decrypted_text = process.stdout.strip()  # Retirer les espaces
            if decrypted_text.decode(errors="ignore") == clair:
                print(f"Mot de passe trouvé : {mot_de_passe}")
                break  # Sortir dès que le mot de passe est trouvé
        else:
            # Afficher l'erreur si le déchiffrement échoue
            print(f"Erreur de déchiffrement avec le mot de passe : {mot_de_passe}")
            print(f"Erreur OpenSSL : {process.stderr.decode(errors='ignore')}")

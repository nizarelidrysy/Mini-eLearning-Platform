import time
import data
import ui

def generer_id_specifique(liste):
    """Finds the max ID in a specific list and returns max + 1."""
    if not liste:
        return 1
    ids = [list(item.keys())[0] for item in liste]
    return max(ids) + 1

def chercher_utilisateur(email, password, liste, role_name):
    for utilisateur in liste:
        for u_id, info in utilisateur.items():
            if info["email"] == email and info["password"] == password:
                return role_name, u_id
    return None, None

def connexion():
    for i in range(3):
        ui.clear_screen()
        ui.draw_header("AUTHENTIFICATION")
        email = input(" Email : ").strip()
        pw = input(" Mot de passe : ").strip()
        
        for liste, role in [(data.administrateurs, "admin"), 
                           (data.enseignants, "responsable"), 
                           (data.etudiants, "utilisateur")]:
            found_role, u_id = chercher_utilisateur(email, pw, liste, role)
            if found_role: return found_role, u_id
            
        print(f"\n{ui.Colors.FAIL}✖ Identifiants invalides.{ui.Colors.RESET}")
        time.sleep(1)
    return None, None

def inscription():
    ui.clear_screen()
    ui.draw_header("INSCRIPTION")
    print(" [1] Étudiant | [2] Professeur")
    choix = input("\n Votre choix : ").strip()
    
    if choix not in ["1", "2"]: return
    
    nom = input(" Nom complet : ").strip()
    email = input(" Email : ").strip()
    pw = input(" Mot de passe : ").strip()

    if choix == "1":
        n_id = generer_id_specifique(data.etudiants)
        data.etudiants.append({n_id: {"nom": nom, "email": email, "password": pw}})
    else:
        n_id = generer_id_specifique(data.enseignants)
        data.enseignants.append({n_id: {"nom": nom, "email": email, "password": pw}})
    
    data.sauvegarder()
    print(f"\n{ui.Colors.GREEN}✔ Compte créé ! ID : {n_id}{ui.Colors.RESET}")
    time.sleep(1.5)
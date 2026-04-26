import time
import data
import ui
import authentification

def consulter_tout_le_monde():
    ui.clear_screen()
    ui.draw_header("BASE DE DONNÉES")
    for label, liste in [("PROFS", data.enseignants), ("ÉLÈVES", data.etudiants)]:
        print(f"\n {ui.Colors.BOLD}{label}{ui.Colors.RESET}")
        for user in liste:
            for u_id, info in user.items():
                print(f"  ID: {u_id:02d} | {info['nom']} ({info['email']})")
    ui.pause()

def supprimer_utilisateur():
    ui.clear_screen()
    ui.draw_header("SUPPRIMER UN COMPTE", color=ui.Colors.FAIL)
    print(" [1] Étudiant | [2] Professeur")
    cat = input(" Catégorie : ").strip()
    try:
        u_id = int(input(" ID à supprimer : "))
        liste = data.etudiants if cat == "1" else data.enseignants
        for i, user in enumerate(liste):
            if u_id in user:
                del liste[i]
                data.sauvegarder()
                print(f"{ui.Colors.GREEN}✔ Supprimé.{ui.Colors.RESET}")
                time.sleep(1.5)
                return
    except ValueError: pass
    time.sleep(1.5)

def menu_admin(id_admin):
    while True:
        ui.clear_screen()
        ui.draw_header("ADMINISTRATION")
        print(" [1] Voir tout le monde | [2] Supprimer | [3] Déconnexion")
        choix = input("\n Action > ").strip()
        if choix == "1": consulter_tout_le_monde()
        elif choix == "2": supprimer_utilisateur()
        elif choix == "3": break
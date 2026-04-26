import data
import ui

def consulter_catalogue():
    ui.clear_screen()
    ui.draw_header("CATALOGUE DES COURS")
    
    if not data.cours:
        print(f"  {ui.Colors.WARNING}La base de données des cours est vide.{ui.Colors.RESET}")
    else:
        for cours in data.cours:
            for c_id, info in cours.items():
                print(f" {ui.Colors.BLUE}■ {info['titre'].upper()}{ui.Colors.RESET}")
                print(f"   {info['description']}")
                print(f"   {ui.Colors.CYAN}(Réf: {c_id:03d}){ui.Colors.RESET}\n")
    
    ui.pause()

def menu_utilisateur(id_etudiant):
    while True:
        ui.clear_screen()
        ui.draw_header("ESPACE ÉTUDIANT", color=ui.Colors.BLUE)
        print(f"  {ui.Colors.BOLD}[1]{ui.Colors.RESET}  Parcourir le catalogue")
        print(f"  {ui.Colors.BOLD}[2]{ui.Colors.RESET}  Déconnexion")
        print(f"{ui.Colors.BLUE}={'=' * 48}={ui.Colors.RESET}")
        
        choix = input(f" {ui.Colors.BOLD}Exécuter > {ui.Colors.RESET}")
        if choix == "1": consulter_catalogue()
        elif choix == "2": break
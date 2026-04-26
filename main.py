2
import time
import ui
import authentification
import responsable
import admin
import utilisateur

def main():
    while True:
        ui.clear_screen()
        ui.draw_header("NEXUS LEARN - TERMINAL GATEWAY", color=ui.Colors.BLUE)
        
        print(f"  {ui.Colors.BOLD}[1]{ui.Colors.RESET}  Se connecter")
        print(f"  {ui.Colors.BOLD}[2]{ui.Colors.RESET}  S'inscrire")
        print(f"  {ui.Colors.BOLD}[3]{ui.Colors.RESET}  Quitter")
        print(f"{ui.Colors.BLUE}={'=' * 48}={ui.Colors.RESET}")
        
        choix = input(f" {ui.Colors.BOLD}Action (1-3) > {ui.Colors.RESET}").strip()
        
        try:
            if choix == "1":
                role, user_id = authentification.connexion()
                if role and user_id:
                    ui.loading("Authentification en cours")
                    if role == "admin":
                        admin.menu_admin(user_id)
                    elif role == "responsable":
                        responsable.menu_responsable(user_id)
                    elif role == "utilisateur":
                        utilisateur.menu_utilisateur(user_id)
            elif choix == "2":
                authentification.inscription()
            elif choix == "3":
                ui.clear_screen()
                ui.loading("Fermeture du système", 1)
                print(f"{ui.Colors.GREEN}Système hors ligne. Au revoir.{ui.Colors.RESET}\n")
                break
            else:
                print(f"{ui.Colors.FAIL} Commande non reconnue.{ui.Colors.RESET}")
                time.sleep(1)
        except Exception as e:
            print(f"\n{ui.Colors.FAIL}Erreur critique: {e}{ui.Colors.RESET}")
            time.sleep(3)

if __name__ == "__main__":
    main()
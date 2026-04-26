import time
import data
import ui

def generer_id_cours():
    if not data.cours: return 1
    return max([list(c.keys())[0] for c in data.cours]) + 1

def ajouter_cours(id_prof):
    ui.draw_header("NOUVEAU COURS")
    titre = input(" Titre du cours : ").strip()
    desc = input(" Description : ").strip()
    
    if titre and desc:
        c_id = generer_id_cours()
        data.cours.append({c_id: {"titre": titre, "description": desc, "enseignant_id": id_prof}})
        data.sauvegarder()
        print(f"\n{ui.Colors.GREEN}✔ Cours ajouté.{ui.Colors.RESET}")
    time.sleep(1.5)

def modifier_cours(id_prof):
    try:
        c_id = int(input("\n ID du cours à modifier : "))
        for cours_dict in data.cours:
            if c_id in cours_dict:
                info = cours_dict[c_id]
                if info["enseignant_id"] == id_prof:
                    print(f" Modif : {info['titre']}")
                    n_titre = input(" Nouveau titre (entrée pour ignorer) : ").strip()
                    n_desc = input(" Nouvelle description (entrée pour ignorer) : ").strip()
                    if n_titre: info["titre"] = n_titre
                    if n_desc: info["description"] = n_desc
                    data.sauvegarder()
                    print(f"{ui.Colors.GREEN}✔ Mis à jour.{ui.Colors.RESET}")
                    return
        print(f"{ui.Colors.FAIL}✖ Non autorisé ou ID inconnu.{ui.Colors.RESET}")
    except ValueError: pass
    time.sleep(1.5)

def supprimer_cours(id_prof):
    try:
        c_id = int(input("\n ID du cours à supprimer : "))
        for i, cours_dict in enumerate(data.cours):
            if c_id in cours_dict and cours_dict[c_id]["enseignant_id"] == id_prof:
                del data.cours[i]
                data.sauvegarder()
                print(f"{ui.Colors.GREEN}✔ Supprimé.{ui.Colors.RESET}")
                return
    except ValueError: pass
    time.sleep(1.5)

def menu_gerer_cours(id_prof):
    while True:
        ui.clear_screen()
        ui.draw_header("GESTION DES COURS")
        trouve = False
        for cours in data.cours:
            for c_id, info in cours.items():
                if info["enseignant_id"] == id_prof:
                    print(f" [{c_id:02d}] {info['titre']}")
                    trouve = True
        if not trouve: print(" Aucun cours créé.")

        print("\n [1] Ajouter | [2] Modifier | [3] Supprimer | [4] Retour")
        choix = input("\n Action > ").strip()
        if choix == "1": ajouter_cours(id_prof)
        elif choix == "2": modifier_cours(id_prof)
        elif choix == "3": supprimer_cours(id_prof)
        elif choix == "4": break

def menu_responsable(id_prof):
    while True:
        ui.clear_screen()
        ui.draw_header("ESPACE PROFESSEUR")
        print(" [1] Gérer mes cours")
        print(" [2] Déconnexion")
        choix = input("\n Sélection > ").strip()
        if choix == "1": menu_gerer_cours(id_prof)
        elif choix == "2": break
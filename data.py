import json
import os

DB_FILE = "nexus_db.json"

# Memory storage
administrateurs = [{1: {"nom": "Admin Principal", "email": "admin@emsi.ma", "password": "admin"}}]
enseignants = []
etudiants = []
cours = []

def sauvegarder():
    """Saves the current state of lists to the JSON file."""
    db = {
        "administrateurs": administrateurs,
        "enseignants": enseignants,
        "etudiants": etudiants,
        "cours": cours
    }
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(db, f, indent=4, ensure_ascii=False)

def charger_donnees():
    """Loads data from JSON and converts keys back to integers."""
    global administrateurs, enseignants, etudiants, cours
    if not os.path.exists(DB_FILE):
        sauvegarder()
        return

    try:
        with open(DB_FILE, "r", encoding="utf-8") as f:
            db = json.load(f)
            
            # Helper to convert {"1": {}} -> {1: {}}
            def to_int_keys(data_list):
                return [{int(k): v} for item in data_list for k, v in item.items()]

            if db.get("administrateurs"):
                administrateurs = to_int_keys(db["administrateurs"])
            enseignants = to_int_keys(db.get("enseignants", []))
            etudiants = to_int_keys(db.get("etudiants", []))
            cours = to_int_keys(db.get("cours", []))
    except Exception as e:
        print(f"Erreur de base de données : {e}")

# Load automatically when the program starts
charger_donnees()
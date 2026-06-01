"""
Script de données initiales pour Nexus Learn.
Crée : admin, enseignants, étudiants, cours, leçons, quiz avec questions.
"""

import os
import sys
import django

# Setup Django
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nexus_django.settings')
django.setup()

from django.contrib.auth.models import User
from plateforme.models import ProfilUtilisateur, Cours, Lecon, Inscription, Quiz, Question, Choix

def creer_utilisateur(username, password, first_name, last_name, email, role):
    if User.objects.filter(username=username).exists():
        print(f"  → {username} existe déjà.")
        return User.objects.get(username=username)
    user = User.objects.create_user(
        username=username, password=password,
        first_name=first_name, last_name=last_name, email=email
    )
    ProfilUtilisateur.objects.create(utilisateur=user, role=role)
    print(f"  ✓ {role.capitalize()} '{username}' créé.")
    return user

print("\n=== Nexus Learn — Initialisation des données ===\n")

# ── Administrateur ─────────────────────────────────────────────────────────────
print("Création des administrateurs :")
admin = creer_utilisateur('admin', 'admin123', 'Admin', 'Principal', 'admin@emsi.ma', 'admin')

# ── Enseignants ────────────────────────────────────────────────────────────────
print("\nCréation des enseignants :")
prof1 = creer_utilisateur('reem', '1234', 'Reem', 'Benali', 'reem@emsi.ma', 'enseignant')
prof2 = creer_utilisateur('nizar_prof', 'azerty', 'Nizar', 'El Idrysy', 'nizar@emsi.ma', 'enseignant')

# ── Étudiants ──────────────────────────────────────────────────────────────────
print("\nCréation des étudiants :")
etud1 = creer_utilisateur('rim', 'rim1234', 'Rim', 'Charai', 'rim@emsi.ma', 'etudiant')
etud2 = creer_utilisateur('israe', 'israe1234', 'Israe', 'Zahaar', 'israe@emsi.ma', 'etudiant')

# ── Cours ──────────────────────────────────────────────────────────────────────
print("\nCréation des cours :")

def creer_cours(titre, description, enseignant):
    cours, created = Cours.objects.get_or_create(
        titre=titre,
        defaults={'description': description, 'enseignant': enseignant, 'est_publie': True}
    )
    if created:
        print(f"  ✓ Cours '{titre}' créé.")
    return cours

c1 = creer_cours(
    "Introduction à Python",
    "Apprenez les bases du langage Python : variables, conditions, boucles, fonctions et modules. "
    "Ce cours est idéal pour les débutants souhaitant se lancer dans la programmation.",
    prof1
)

c2 = creer_cours(
    "Développement Web avec Django",
    "Maîtrisez le framework Django pour créer des applications web robustes et sécurisées. "
    "Vous apprendrez les modèles, vues, templates, formulaires et l'ORM Django.",
    prof1
)

c3 = creer_cours(
    "Bases de données relationnelles",
    "Découvrez le SQL et les concepts fondamentaux des bases de données relationnelles : "
    "tables, requêtes SELECT, jointures, transactions et normalisation.",
    prof2
)

c4 = creer_cours(
    "Algorithmique et structures de données",
    "Étudiez les algorithmes classiques (tri, recherche, graphes) et les structures de données "
    "(listes, piles, files, arbres) pour résoudre efficacement des problèmes informatiques.",
    prof2
)

# ── Leçons ─────────────────────────────────────────────────────────────────────
print("\nCréation des leçons :")

def creer_lecon(cours, titre, contenu, ordre):
    lecon, created = Lecon.objects.get_or_create(
        cours=cours, ordre=ordre,
        defaults={'titre': titre, 'contenu': contenu}
    )
    if created:
        print(f"  ✓ Leçon '{titre}' ajoutée à '{cours.titre}'.")
    return lecon

# Leçons Python
creer_lecon(c1, "Les variables et types de données", 
"""En Python, une variable est un nom qui désigne une valeur stockée en mémoire.

Types de base :
- int    : nombres entiers (ex: 42, -5)
- float  : nombres décimaux (ex: 3.14)
- str    : chaînes de caractères (ex: "Bonjour")
- bool   : valeurs booléennes (True / False)

Exemples :
    age = 20
    nom = "Rim"
    pi = 3.14159
    est_etudiant = True

Python est un langage à typage dynamique : le type est déterminé automatiquement à l'assignation.
""", 1)

creer_lecon(c1, "Les structures conditionnelles",
"""Les structures conditionnelles permettent d'exécuter du code selon des conditions.

Syntaxe de base :
    if condition:
        # bloc exécuté si condition est vraie
    elif autre_condition:
        # bloc exécuté si autre_condition est vraie
    else:
        # bloc exécuté dans tous les autres cas

Exemple :
    note = 15
    if note >= 16:
        print("Très bien")
    elif note >= 12:
        print("Bien")
    else:
        print("Passable")

Opérateurs de comparaison : ==, !=, <, >, <=, >=
Opérateurs logiques : and, or, not
""", 2)

creer_lecon(c1, "Les boucles for et while",
"""Python offre deux types de boucles pour répéter des instructions.

La boucle for :
    for i in range(5):
        print(i)  # affiche 0, 1, 2, 3, 4

    for lettre in "Python":
        print(lettre)

La boucle while :
    compteur = 0
    while compteur < 5:
        print(compteur)
        compteur += 1

Instructions de contrôle :
- break    : quitte la boucle immédiatement
- continue : passe à l'itération suivante
- else     : s'exécute si la boucle se termine normalement
""", 3)

# Leçons Django
creer_lecon(c2, "Architecture MTV de Django",
"""Django utilise le pattern MTV (Model-Template-View), similaire au MVC.

- Model   : définit la structure des données (ORM)
- Template : gère l'affichage HTML
- View    : contient la logique métier

Flux d'une requête Django :
1. L'utilisateur envoie une requête HTTP
2. Django vérifie les URLs (urls.py)
3. La vue correspondante est appelée
4. La vue interroge les modèles si nécessaire
5. Le template est rendu avec les données
6. La réponse HTML est envoyée au navigateur

Commandes essentielles :
    django-admin startproject mon_projet
    python manage.py startapp mon_app
    python manage.py runserver
    python manage.py makemigrations
    python manage.py migrate
""", 1)

creer_lecon(c2, "Les modèles et l'ORM",
"""L'ORM (Object-Relational Mapping) de Django permet de manipuler la base de données en Python.

Définir un modèle :
    from django.db import models

    class Article(models.Model):
        titre = models.CharField(max_length=200)
        contenu = models.TextField()
        date = models.DateTimeField(auto_now_add=True)

        def __str__(self):
            return self.titre

Opérations CRUD avec l'ORM :
    # Créer
    article = Article.objects.create(titre="Bonjour", contenu="...")

    # Lire
    tous = Article.objects.all()
    un   = Article.objects.get(pk=1)
    filtre = Article.objects.filter(titre__contains="Python")

    # Mettre à jour
    article.titre = "Nouveau titre"
    article.save()

    # Supprimer
    article.delete()
""", 2)

# Leçons SQL
creer_lecon(c3, "Introduction aux bases de données relationnelles",
"""Une base de données relationnelle organise les données en tables (relations).

Concepts fondamentaux :
- Table    : ensemble de lignes et colonnes (comme un tableau)
- Colonne  : attribut (ex: nom, age, email)
- Ligne    : enregistrement (tuple)
- Clé primaire (PK) : identifiant unique de chaque ligne
- Clé étrangère (FK) : référence vers une autre table

Exemple de table ETUDIANTS :
    +----+----------+---------+--------------------+
    | id | nom      | prénom  | email              |
    +----+----------+---------+--------------------+
    |  1 | Charai   | Rim     | rim@emsi.ma        |
    |  2 | El Idrysy| Nizar   | nizar@emsi.ma      |
    +----+----------+---------+--------------------+

Types de relations :
- 1:1  (One-to-One)
- 1:N  (One-to-Many)
- N:M  (Many-to-Many)
""", 1)

creer_lecon(c3, "Requêtes SQL fondamentales",
"""SQL (Structured Query Language) est le langage standard pour les bases de données relationnelles.

SELECT — Lire des données :
    SELECT * FROM etudiants;
    SELECT nom, email FROM etudiants WHERE id = 1;
    SELECT * FROM etudiants ORDER BY nom ASC;

INSERT — Insérer des données :
    INSERT INTO etudiants (nom, prenom, email)
    VALUES ('Zahaar', 'Israe', 'israe@emsi.ma');

UPDATE — Modifier des données :
    UPDATE etudiants SET email = 'nouveau@mail.ma' WHERE id = 1;

DELETE — Supprimer des données :
    DELETE FROM etudiants WHERE id = 3;

Jointures (JOIN) :
    SELECT e.nom, c.titre
    FROM etudiants e
    JOIN inscriptions i ON e.id = i.etudiant_id
    JOIN cours c ON i.cours_id = c.id;
""", 2)

# ── Quiz ───────────────────────────────────────────────────────────────────────
print("\nCréation des quiz :")

def creer_quiz_complet(cours, titre, questions_data):
    quiz, created = Quiz.objects.get_or_create(cours=cours, defaults={'titre': titre})
    if created:
        print(f"  ✓ Quiz '{titre}' créé.")
        for i, (q_texte, choix_list) in enumerate(questions_data, 1):
            question = Question.objects.create(quiz=quiz, texte=q_texte, ordre=i)
            for c_texte, est_correct in choix_list:
                Choix.objects.create(question=question, texte=c_texte, est_correct=est_correct)
    return quiz

creer_quiz_complet(c1, "Quiz Python — Bases", [
    ("Quel est le type de la valeur 3.14 en Python ?", [
        ("int", False), ("float", True), ("str", False), ("bool", False)
    ]),
    ("Quelle instruction permet de répéter une action un nombre déterminé de fois ?", [
        ("while", False), ("if", False), ("for", True), ("def", False)
    ]),
    ("Comment déclare-t-on une variable en Python ?", [
        ("var x = 5", False), ("x = 5", True), ("int x = 5", False), ("declare x = 5", False)
    ]),
    ("Que renvoie 10 % 3 en Python ?", [
        ("3", False), ("1", True), ("0", False), ("30", False)
    ]),
])

creer_quiz_complet(c2, "Quiz Django — Architecture", [
    ("Que signifie MTV dans Django ?", [
        ("Model-Template-View", True), ("Model-Table-Vue", False), ("Module-Template-Validation", False), ("Multi-Thread-View", False)
    ]),
    ("Quelle commande crée les tables en base de données ?", [
        ("python manage.py makemigrations", False), ("python manage.py migrate", True),
        ("python manage.py createdb", False), ("python manage.py syncdb", False)
    ]),
    ("Dans Django, quel fichier gère le routage des URLs ?", [
        ("views.py", False), ("models.py", False), ("urls.py", True), ("settings.py", False)
    ]),
])

creer_quiz_complet(c3, "Quiz SQL — Fondamentaux", [
    ("Quelle commande SQL lit toutes les lignes d'une table ?", [
        ("GET * FROM table", False), ("SELECT * FROM table", True), ("READ * FROM table", False), ("FETCH * FROM table", False)
    ]),
    ("Quel mot-clé filtre les résultats d'une requête SELECT ?", [
        ("FILTER", False), ("WHERE", True), ("HAVING", False), ("LIMIT", False)
    ]),
    ("Quelle est la clé qui identifie de manière unique chaque ligne ?", [
        ("Clé étrangère", False), ("Clé secondaire", False), ("Clé primaire", True), ("Clé alternative", False)
    ]),
])

# ── Inscriptions ────────────────────────────────────────────────────────────────
print("\nCréation des inscriptions :")

def inscrire(etudiant, cours, progression=0):
    inscription, created = Inscription.objects.get_or_create(
        etudiant=etudiant, cours=cours,
        defaults={'progression': progression}
    )
    if created:
        print(f"  ✓ {etudiant.first_name} inscrit à '{cours.titre}' ({progression}%)")

inscrire(etud1, c1, 67)
inscrire(etud1, c3, 33)
inscrire(etud2, c1, 100)
inscrire(etud2, c2, 50)

print("\n=== ✅ Données initiales créées avec succès ! ===")
print("\nComptes disponibles :")
print("  Admin     : admin / admin123")
print("  Enseignant: reem / 1234")
print("  Enseignant: nizar_prof / azerty")
print("  Étudiant  : rim / rim1234")
print("  Étudiant  : israe / israe1234")
print("\nDémarrez le serveur : python manage.py runserver")

from django.urls import path
from . import views

urlpatterns = [
    # ── Auth ────────────────────────────────────────────────────────────────
    path('', views.vue_accueil, name='accueil'),
    path('connexion/', views.vue_connexion, name='connexion'),
    path('inscription/', views.vue_inscription, name='inscription'),
    path('deconnexion/', views.vue_deconnexion, name='deconnexion'),
    path('profil/', views.vue_profil, name='profil'),

    # ── Admin ────────────────────────────────────────────────────────────────
    path('administration/', views.vue_tableau_bord_admin, name='tableau_bord_admin'),
    path('administration/utilisateurs/', views.vue_admin_utilisateurs, name='admin_utilisateurs'),
    path('administration/utilisateurs/creer/', views.vue_admin_creer_utilisateur, name='admin_creer_utilisateur'),
    path('administration/utilisateurs/<int:pk>/modifier/', views.vue_admin_modifier_utilisateur, name='admin_modifier_utilisateur'),
    path('administration/utilisateurs/<int:pk>/supprimer/', views.vue_admin_supprimer_utilisateur, name='admin_supprimer_utilisateur'),
    path('administration/cours/', views.vue_admin_cours, name='admin_cours'),
    path('administration/cours/<int:pk>/supprimer/', views.vue_admin_supprimer_cours, name='admin_supprimer_cours'),

    # ── Enseignant ───────────────────────────────────────────────────────────
    path('enseignant/', views.vue_tableau_bord_enseignant, name='tableau_bord_enseignant'),
    path('enseignant/cours/creer/', views.vue_creer_cours, name='creer_cours'),
    path('enseignant/cours/<int:pk>/', views.vue_detail_cours_enseignant, name='detail_cours_enseignant'),
    path('enseignant/cours/<int:pk>/modifier/', views.vue_modifier_cours, name='modifier_cours'),
    path('enseignant/cours/<int:pk>/supprimer/', views.vue_supprimer_cours, name='supprimer_cours'),
    path('enseignant/cours/<int:cours_pk>/lecon/ajouter/', views.vue_ajouter_lecon, name='ajouter_lecon'),
    path('enseignant/lecon/<int:pk>/modifier/', views.vue_modifier_lecon, name='modifier_lecon'),
    path('enseignant/lecon/<int:pk>/supprimer/', views.vue_supprimer_lecon, name='supprimer_lecon'),
    path('enseignant/cours/<int:cours_pk>/quiz/', views.vue_creer_quiz, name='creer_quiz'),
    path('enseignant/quiz/<int:pk>/gerer/', views.vue_gerer_quiz, name='gerer_quiz'),
    path('enseignant/quiz/<int:quiz_pk>/question/ajouter/', views.vue_ajouter_question, name='ajouter_question'),
    path('enseignant/question/<int:question_pk>/choix/ajouter/', views.vue_ajouter_choix, name='ajouter_choix'),
    path('enseignant/question/<int:pk>/supprimer/', views.vue_supprimer_question, name='supprimer_question'),

    # ── Étudiant ─────────────────────────────────────────────────────────────
    path('etudiant/', views.vue_tableau_bord_etudiant, name='tableau_bord_etudiant'),
    path('catalogue/', views.vue_catalogue, name='catalogue'),
    path('cours/<int:pk>/', views.vue_detail_cours_etudiant, name='detail_cours_etudiant'),
    path('cours/<int:pk>/sinscrire/', views.vue_sinscrire_cours, name='sinscrire_cours'),
    path('lecon/<int:pk>/', views.vue_lecon, name='lecon'),
    path('quiz/<int:pk>/passer/', views.vue_passer_quiz, name='passer_quiz'),
    path('mes-resultats/', views.vue_mes_resultats, name='mes_resultats'),
]

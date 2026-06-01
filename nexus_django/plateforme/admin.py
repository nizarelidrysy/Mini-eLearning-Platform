from django.contrib import admin
from .models import ProfilUtilisateur, Cours, Lecon, Inscription, Quiz, Question, Choix, ResultatQuiz

@admin.register(ProfilUtilisateur)
class ProfilAdmin(admin.ModelAdmin):
    list_display = ['utilisateur', 'role', 'date_creation']
    list_filter = ['role']

@admin.register(Cours)
class CoursAdmin(admin.ModelAdmin):
    list_display = ['titre', 'enseignant', 'est_publie', 'date_creation']
    list_filter = ['est_publie']

@admin.register(Lecon)
class LeconAdmin(admin.ModelAdmin):
    list_display = ['titre', 'cours', 'ordre']

@admin.register(Inscription)
class InscriptionAdmin(admin.ModelAdmin):
    list_display = ['etudiant', 'cours', 'progression', 'date_inscription']

admin.site.register(Quiz)
admin.site.register(Question)
admin.site.register(Choix)
admin.site.register(ResultatQuiz)

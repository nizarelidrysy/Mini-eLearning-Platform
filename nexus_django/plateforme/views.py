from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Avg, Count
from functools import wraps

from .models import (
    ProfilUtilisateur, Cours, Lecon, Inscription,
    Quiz, Question, Choix, ResultatQuiz
)
from .forms import (
    FormulaireConnexion, FormulaireInscription, FormulaireProfil,
    FormulaireCours, FormulaireLecon, FormulaireQuiz,
    FormulaireQuestion, FormulaireChoix, FormulaireUtilisateurAdmin
)


# ─── Décorateurs de rôles ─────────────────────────────────────────────────────

def role_requis(*roles):
    """Décorateur : redirige si l'utilisateur n'a pas le bon rôle."""
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('connexion')
            try:
                if request.user.profil.role not in roles:
                    messages.error(request, "Accès refusé : vous n'avez pas les droits nécessaires.")
                    return redirect('accueil')
            except ProfilUtilisateur.DoesNotExist:
                return redirect('connexion')
            return view_func(request, *args, **kwargs)
        return _wrapped
    return decorator


# ─── Authentification ─────────────────────────────────────────────────────────

def vue_connexion(request):
    """Page de connexion."""
    if request.user.is_authenticated:
        return redirect('accueil')
    form = FormulaireConnexion(request, data=request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.get_user()
        login(request, user)
        messages.success(request, f"Bienvenue, {user.get_full_name() or user.username} !")
        return redirect('accueil')
    return render(request, 'plateforme/connexion.html', {'form': form})


def vue_inscription(request):
    """Page d'inscription."""
    if request.user.is_authenticated:
        return redirect('accueil')
    form = FormulaireInscription(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, "Compte créé avec succès ! Bienvenue sur Nexus Learn.")
        return redirect('accueil')
    return render(request, 'plateforme/inscription.html', {'form': form})


@login_required
def vue_deconnexion(request):
    """Déconnexion."""
    logout(request)
    messages.info(request, "Vous avez été déconnecté.")
    return redirect('connexion')


# ─── Accueil & Tableau de bord ────────────────────────────────────────────────

@login_required
def vue_accueil(request):
    """Redirige vers le bon tableau de bord selon le rôle."""
    try:
        role = request.user.profil.role
    except ProfilUtilisateur.DoesNotExist:
        return redirect('connexion')

    if role == 'admin':
        return redirect('tableau_bord_admin')
    elif role == 'enseignant':
        return redirect('tableau_bord_enseignant')
    else:
        return redirect('tableau_bord_etudiant')


# ─── Profil ───────────────────────────────────────────────────────────────────

@login_required
def vue_profil(request):
    """Page de profil utilisateur."""
    profil = get_object_or_404(ProfilUtilisateur, utilisateur=request.user)
    form = FormulaireProfil(
        request.POST or None,
        request.FILES or None,
        instance=profil,
        initial={
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'email': request.user.email,
        }
    )
    if request.method == 'POST' and form.is_valid():
        request.user.first_name = form.cleaned_data['first_name']
        request.user.last_name = form.cleaned_data['last_name']
        request.user.email = form.cleaned_data['email']
        request.user.save()
        form.save()
        messages.success(request, "Profil mis à jour avec succès.")
        return redirect('profil')
    return render(request, 'plateforme/profil.html', {'form': form, 'profil': profil})


# ─── Admin ────────────────────────────────────────────────────────────────────

@role_requis('admin')
def vue_tableau_bord_admin(request):
    """Tableau de bord administrateur."""
    nb_enseignants = ProfilUtilisateur.objects.filter(role='enseignant').count()
    nb_etudiants = ProfilUtilisateur.objects.filter(role='etudiant').count()
    nb_cours = Cours.objects.count()
    nb_inscriptions = Inscription.objects.count()
    cours_recents = Cours.objects.order_by('-date_creation')[:5]
    utilisateurs_recents = User.objects.order_by('-date_joined')[:5]

    context = {
        'nb_enseignants': nb_enseignants,
        'nb_etudiants': nb_etudiants,
        'nb_cours': nb_cours,
        'nb_inscriptions': nb_inscriptions,
        'cours_recents': cours_recents,
        'utilisateurs_recents': utilisateurs_recents,
    }
    return render(request, 'plateforme/tableau_bord_admin.html', context)


@role_requis('admin')
def vue_admin_utilisateurs(request):
    """Liste de tous les utilisateurs."""
    utilisateurs = User.objects.select_related('profil').order_by('date_joined')
    return render(request, 'plateforme/admin_utilisateurs.html', {'utilisateurs': utilisateurs})


@role_requis('admin')
def vue_admin_creer_utilisateur(request):
    """Créer un utilisateur (admin)."""
    form = FormulaireUtilisateurAdmin(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save(commit=False)
        user.set_password('nexus2024')
        user.save()
        ProfilUtilisateur.objects.create(utilisateur=user, role=form.cleaned_data['role'])
        messages.success(request, f"Utilisateur '{user.username}' créé. Mot de passe provisoire : nexus2024")
        return redirect('admin_utilisateurs')
    return render(request, 'plateforme/admin_utilisateur_form.html', {'form': form, 'titre': 'Créer un utilisateur'})


@role_requis('admin')
def vue_admin_modifier_utilisateur(request, pk):
    """Modifier un utilisateur (admin)."""
    user = get_object_or_404(User, pk=pk)
    profil, _ = ProfilUtilisateur.objects.get_or_create(utilisateur=user)
    form = FormulaireUtilisateurAdmin(request.POST or None, instance=user, initial={'role': profil.role})
    if request.method == 'POST' and form.is_valid():
        form.save()
        profil.role = form.cleaned_data['role']
        profil.save()
        messages.success(request, "Utilisateur mis à jour.")
        return redirect('admin_utilisateurs')
    return render(request, 'plateforme/admin_utilisateur_form.html', {'form': form, 'titre': 'Modifier un utilisateur', 'user_cible': user})


@role_requis('admin')
def vue_admin_supprimer_utilisateur(request, pk):
    """Supprimer un utilisateur (admin)."""
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        nom = user.get_full_name() or user.username
        user.delete()
        messages.success(request, f"Utilisateur '{nom}' supprimé.")
        return redirect('admin_utilisateurs')
    return render(request, 'plateforme/confirmer_suppression.html', {
        'objet': user.get_full_name() or user.username,
        'url_retour': 'admin_utilisateurs',
    })


@role_requis('admin')
def vue_admin_cours(request):
    """Liste de tous les cours (admin)."""
    cours = Cours.objects.select_related('enseignant').order_by('-date_creation')
    return render(request, 'plateforme/admin_cours.html', {'cours': cours})


@role_requis('admin')
def vue_admin_supprimer_cours(request, pk):
    """Supprimer un cours (admin)."""
    cours = get_object_or_404(Cours, pk=pk)
    if request.method == 'POST':
        cours.delete()
        messages.success(request, "Cours supprimé.")
        return redirect('admin_cours')
    return render(request, 'plateforme/confirmer_suppression.html', {
        'objet': cours.titre,
        'url_retour': 'admin_cours',
    })


# ─── Enseignant ───────────────────────────────────────────────────────────────

@role_requis('enseignant')
def vue_tableau_bord_enseignant(request):
    """Tableau de bord enseignant."""
    mes_cours = Cours.objects.filter(enseignant=request.user).annotate(
        nb_inscrits=Count('inscriptions')
    )
    total_inscrits = sum(c.nb_inscrits for c in mes_cours)
    context = {
        'mes_cours': mes_cours,
        'total_inscrits': total_inscrits,
    }
    return render(request, 'plateforme/tableau_bord_enseignant.html', context)


@role_requis('enseignant')
def vue_creer_cours(request):
    """Créer un nouveau cours."""
    form = FormulaireCours(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        cours = form.save(commit=False)
        cours.enseignant = request.user
        cours.save()
        messages.success(request, f"Cours '{cours.titre}' créé avec succès !")
        return redirect('detail_cours_enseignant', pk=cours.pk)
    return render(request, 'plateforme/cours_form.html', {'form': form, 'titre': 'Créer un cours'})


@role_requis('enseignant')
def vue_modifier_cours(request, pk):
    """Modifier un cours existant."""
    cours = get_object_or_404(Cours, pk=pk, enseignant=request.user)
    form = FormulaireCours(request.POST or None, request.FILES or None, instance=cours)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, "Cours mis à jour.")
        return redirect('detail_cours_enseignant', pk=cours.pk)
    return render(request, 'plateforme/cours_form.html', {'form': form, 'titre': 'Modifier le cours', 'cours': cours})


@role_requis('enseignant')
def vue_supprimer_cours(request, pk):
    """Supprimer un cours."""
    cours = get_object_or_404(Cours, pk=pk, enseignant=request.user)
    if request.method == 'POST':
        cours.delete()
        messages.success(request, "Cours supprimé.")
        return redirect('tableau_bord_enseignant')
    return render(request, 'plateforme/confirmer_suppression.html', {
        'objet': cours.titre,
        'url_retour': 'tableau_bord_enseignant',
    })


@role_requis('enseignant')
def vue_detail_cours_enseignant(request, pk):
    """Vue détail cours pour l'enseignant (leçons, quiz, inscrits)."""
    cours = get_object_or_404(Cours, pk=pk, enseignant=request.user)
    lecons = cours.lecons.all()
    inscrits = cours.inscriptions.select_related('etudiant')
    quiz = getattr(cours, 'quiz', None)
    return render(request, 'plateforme/detail_cours_enseignant.html', {
        'cours': cours,
        'lecons': lecons,
        'inscrits': inscrits,
        'quiz': quiz,
    })


@role_requis('enseignant')
def vue_ajouter_lecon(request, cours_pk):
    """Ajouter une leçon à un cours."""
    cours = get_object_or_404(Cours, pk=cours_pk, enseignant=request.user)
    form = FormulaireLecon(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        lecon = form.save(commit=False)
        lecon.cours = cours
        lecon.save()
        messages.success(request, f"Leçon '{lecon.titre}' ajoutée.")
        return redirect('detail_cours_enseignant', pk=cours.pk)
    return render(request, 'plateforme/lecon_form.html', {'form': form, 'cours': cours, 'titre': 'Ajouter une leçon'})


@role_requis('enseignant')
def vue_modifier_lecon(request, pk):
    """Modifier une leçon."""
    lecon = get_object_or_404(Lecon, pk=pk, cours__enseignant=request.user)
    form = FormulaireLecon(request.POST or None, request.FILES or None, instance=lecon)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, "Leçon mise à jour.")
        return redirect('detail_cours_enseignant', pk=lecon.cours.pk)
    return render(request, 'plateforme/lecon_form.html', {'form': form, 'cours': lecon.cours, 'titre': 'Modifier la leçon'})


@role_requis('enseignant')
def vue_supprimer_lecon(request, pk):
    """Supprimer une leçon."""
    lecon = get_object_or_404(Lecon, pk=pk, cours__enseignant=request.user)
    cours_pk = lecon.cours.pk
    if request.method == 'POST':
        lecon.delete()
        messages.success(request, "Leçon supprimée.")
        return redirect('detail_cours_enseignant', pk=cours_pk)
    return render(request, 'plateforme/confirmer_suppression.html', {
        'objet': lecon.titre,
        'url_retour': 'detail_cours_enseignant',
        'url_retour_pk': cours_pk,
    })


@role_requis('enseignant')
def vue_creer_quiz(request, cours_pk):
    """Créer ou accéder au quiz d'un cours."""
    cours = get_object_or_404(Cours, pk=cours_pk, enseignant=request.user)
    quiz, created = Quiz.objects.get_or_create(cours=cours, defaults={'titre': f'Quiz — {cours.titre}'})
    return redirect('gerer_quiz', pk=quiz.pk)


@role_requis('enseignant')
def vue_gerer_quiz(request, pk):
    """Gérer un quiz (questions et réponses)."""
    quiz = get_object_or_404(Quiz, pk=pk, cours__enseignant=request.user)
    form_quiz = FormulaireQuiz(request.POST or None, instance=quiz, prefix='quiz')
    form_question = FormulaireQuestion(request.POST or None, prefix='question')
    form_choix = FormulaireChoix(request.POST or None, prefix='choix')

    if request.method == 'POST':
        if 'save_quiz' in request.POST and form_quiz.is_valid():
            form_quiz.save()
            messages.success(request, "Quiz mis à jour.")
        return redirect('gerer_quiz', pk=quiz.pk)

    questions = quiz.questions.prefetch_related('choix').all()
    return render(request, 'plateforme/gerer_quiz.html', {
        'quiz': quiz,
        'form_quiz': form_quiz,
        'questions': questions,
    })


@role_requis('enseignant')
def vue_ajouter_question(request, quiz_pk):
    """Ajouter une question au quiz."""
    quiz = get_object_or_404(Quiz, pk=quiz_pk, cours__enseignant=request.user)
    form = FormulaireQuestion(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        question = form.save(commit=False)
        question.quiz = quiz
        question.save()
        messages.success(request, "Question ajoutée.")
        return redirect('gerer_quiz', pk=quiz.pk)
    return render(request, 'plateforme/question_form.html', {'form': form, 'quiz': quiz})


@role_requis('enseignant')
def vue_ajouter_choix(request, question_pk):
    """Ajouter un choix à une question."""
    question = get_object_or_404(Question, pk=question_pk, quiz__cours__enseignant=request.user)
    form = FormulaireChoix(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        choix = form.save(commit=False)
        choix.question = question
        choix.save()
        messages.success(request, "Choix ajouté.")
        return redirect('gerer_quiz', pk=question.quiz.pk)
    return render(request, 'plateforme/choix_form.html', {'form': form, 'question': question})


@role_requis('enseignant')
def vue_supprimer_question(request, pk):
    """Supprimer une question."""
    question = get_object_or_404(Question, pk=pk, quiz__cours__enseignant=request.user)
    quiz_pk = question.quiz.pk
    question.delete()
    messages.success(request, "Question supprimée.")
    return redirect('gerer_quiz', pk=quiz_pk)


# ─── Étudiant ─────────────────────────────────────────────────────────────────

@role_requis('etudiant')
def vue_tableau_bord_etudiant(request):
    """Tableau de bord étudiant."""
    inscriptions = Inscription.objects.filter(
        etudiant=request.user
    ).select_related('cours', 'cours__enseignant')
    resultats = ResultatQuiz.objects.filter(etudiant=request.user).select_related('quiz__cours')
    context = {
        'inscriptions': inscriptions,
        'resultats': resultats,
    }
    return render(request, 'plateforme/tableau_bord_etudiant.html', context)


@role_requis('etudiant')
def vue_catalogue(request):
    """Catalogue des cours disponibles."""
    cours = Cours.objects.filter(est_publie=True).select_related('enseignant').annotate(
        nb_inscrits=Count('inscriptions')
    )
    mes_inscriptions = Inscription.objects.filter(etudiant=request.user).values_list('cours_id', flat=True)
    return render(request, 'plateforme/catalogue.html', {
        'cours': cours,
        'mes_inscriptions': list(mes_inscriptions),
    })


@role_requis('etudiant')
def vue_sinscrire_cours(request, pk):
    """S'inscrire à un cours."""
    cours = get_object_or_404(Cours, pk=pk, est_publie=True)
    inscription, created = Inscription.objects.get_or_create(
        etudiant=request.user, cours=cours
    )
    if created:
        messages.success(request, f"Vous êtes inscrit au cours '{cours.titre}' !")
    else:
        messages.info(request, "Vous êtes déjà inscrit à ce cours.")
    return redirect('detail_cours_etudiant', pk=cours.pk)


@role_requis('etudiant')
def vue_detail_cours_etudiant(request, pk):
    """Vue détail cours pour un étudiant."""
    cours = get_object_or_404(Cours, pk=pk, est_publie=True)
    inscription = Inscription.objects.filter(etudiant=request.user, cours=cours).first()
    lecons = cours.lecons.all()
    quiz = getattr(cours, 'quiz', None)
    resultat = None
    if quiz:
        resultat = ResultatQuiz.objects.filter(etudiant=request.user, quiz=quiz).order_by('-date').first()
    return render(request, 'plateforme/detail_cours_etudiant.html', {
        'cours': cours,
        'inscription': inscription,
        'lecons': lecons,
        'quiz': quiz,
        'resultat': resultat,
    })


@role_requis('etudiant')
def vue_lecon(request, pk):
    """Afficher le contenu d'une leçon."""
    lecon = get_object_or_404(Lecon, pk=pk)
    inscription = get_object_or_404(Inscription, etudiant=request.user, cours=lecon.cours)

    # Mettre à jour la progression
    total_lecons = lecon.cours.lecons.count()
    if total_lecons > 0:
        lecon_ordre = lecon.ordre
        progression = min(int((lecon_ordre / total_lecons) * 100), 100)
        if progression > inscription.progression:
            inscription.progression = progression
            inscription.save()

    return render(request, 'plateforme/lecon_detail.html', {
        'lecon': lecon,
        'inscription': inscription,
    })


@role_requis('etudiant')
def vue_passer_quiz(request, pk):
    """Passer un quiz."""
    quiz = get_object_or_404(Quiz, pk=pk)
    cours = quiz.cours
    inscription = get_object_or_404(Inscription, etudiant=request.user, cours=cours)
    questions = quiz.questions.prefetch_related('choix').all()

    if request.method == 'POST':
        score = 0
        total = questions.count()
        for question in questions:
            choix_id = request.POST.get(f'question_{question.pk}')
            if choix_id:
                try:
                    choix = Choix.objects.get(pk=int(choix_id), question=question)
                    if choix.est_correct:
                        score += 1
                except (Choix.DoesNotExist, ValueError):
                    pass

        pourcentage = int((score / total) * 100) if total > 0 else 0
        ResultatQuiz.objects.create(etudiant=request.user, quiz=quiz, score=pourcentage)

        # Mettre à jour la progression à 100% si quiz réussi
        if pourcentage >= 50 and inscription.progression < 100:
            inscription.progression = 100
            inscription.save()

        messages.success(request, f"Quiz terminé ! Votre score : {score}/{total} ({pourcentage}%)")
        return redirect('detail_cours_etudiant', pk=cours.pk)

    return render(request, 'plateforme/quiz.html', {'quiz': quiz, 'questions': questions, 'cours': cours})


@role_requis('etudiant')
def vue_mes_resultats(request):
    """Voir tous les résultats de quiz de l'étudiant."""
    resultats = ResultatQuiz.objects.filter(etudiant=request.user).select_related('quiz__cours').order_by('-date')
    return render(request, 'plateforme/mes_resultats.html', {'resultats': resultats})

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class ProfilUtilisateur(models.Model):
    """Extension du modèle User Django avec le rôle."""
    ROLE_CHOICES = [
        ('admin', 'Administrateur'),
        ('enseignant', 'Enseignant'),
        ('etudiant', 'Étudiant'),
    ]
    utilisateur = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profil')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='etudiant')
    bio = models.TextField(blank=True, null=True, verbose_name='Biographie')
    photo = models.ImageField(upload_to='photos/', blank=True, null=True, verbose_name='Photo de profil')
    date_creation = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = 'Profil Utilisateur'
        verbose_name_plural = 'Profils Utilisateurs'

    def __str__(self):
        return f"{self.utilisateur.get_full_name() or self.utilisateur.username} ({self.get_role_display()})"

    def est_admin(self):
        return self.role == 'admin'

    def est_enseignant(self):
        return self.role == 'enseignant'

    def est_etudiant(self):
        return self.role == 'etudiant'


class Cours(models.Model):
    """Un cours créé par un enseignant."""
    titre = models.CharField(max_length=200, verbose_name='Titre du cours')
    description = models.TextField(verbose_name='Description')
    enseignant = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='cours_enseignes',
        limit_choices_to={'profil__role': 'enseignant'}
    )
    image = models.ImageField(upload_to='cours/', blank=True, null=True, verbose_name='Image de couverture')
    date_creation = models.DateTimeField(default=timezone.now)
    est_publie = models.BooleanField(default=True, verbose_name='Publié')

    class Meta:
        verbose_name = 'Cours'
        verbose_name_plural = 'Cours'
        ordering = ['-date_creation']

    def __str__(self):
        return self.titre

    def nombre_inscrits(self):
        return self.inscriptions.count()

    def nombre_lecons(self):
        return self.lecons.count()


class Lecon(models.Model):
    """Une leçon appartenant à un cours."""
    cours = models.ForeignKey(Cours, on_delete=models.CASCADE, related_name='lecons')
    titre = models.CharField(max_length=200, verbose_name='Titre de la leçon')
    contenu = models.TextField(verbose_name='Contenu de la leçon')
    fichier = models.FileField(upload_to='lecons/', blank=True, null=True, verbose_name='Fichier PDF')
    ordre = models.PositiveIntegerField(default=1, verbose_name='Ordre')
    date_creation = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = 'Leçon'
        verbose_name_plural = 'Leçons'
        ordering = ['ordre']

    def __str__(self):
        return f"{self.cours.titre} — {self.titre}"


class Inscription(models.Model):
    """Inscription d'un étudiant à un cours."""
    etudiant = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='inscriptions'
    )
    cours = models.ForeignKey(Cours, on_delete=models.CASCADE, related_name='inscriptions')
    date_inscription = models.DateTimeField(default=timezone.now)
    progression = models.PositiveIntegerField(default=0, verbose_name='Progression (%)')

    class Meta:
        verbose_name = 'Inscription'
        verbose_name_plural = 'Inscriptions'
        unique_together = ('etudiant', 'cours')

    def __str__(self):
        return f"{self.etudiant.username} → {self.cours.titre}"


class Quiz(models.Model):
    """Un quiz associé à un cours."""
    cours = models.OneToOneField(Cours, on_delete=models.CASCADE, related_name='quiz')
    titre = models.CharField(max_length=200, verbose_name='Titre du quiz')
    date_creation = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = 'Quiz'
        verbose_name_plural = 'Quiz'

    def __str__(self):
        return f"Quiz — {self.cours.titre}"

    def nombre_questions(self):
        return self.questions.count()


class Question(models.Model):
    """Une question QCM d'un quiz."""
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    texte = models.TextField(verbose_name='Texte de la question')
    ordre = models.PositiveIntegerField(default=1)

    class Meta:
        verbose_name = 'Question'
        verbose_name_plural = 'Questions'
        ordering = ['ordre']

    def __str__(self):
        return self.texte[:80]


class Choix(models.Model):
    """Un choix de réponse pour une question QCM."""
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='choix')
    texte = models.CharField(max_length=300, verbose_name='Texte du choix')
    est_correct = models.BooleanField(default=False, verbose_name='Réponse correcte')

    class Meta:
        verbose_name = 'Choix'
        verbose_name_plural = 'Choix'

    def __str__(self):
        return self.texte


class ResultatQuiz(models.Model):
    """Résultat d'un étudiant pour un quiz."""
    etudiant = models.ForeignKey(User, on_delete=models.CASCADE, related_name='resultats_quiz')
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='resultats')
    score = models.PositiveIntegerField(default=0, verbose_name='Score (%)')
    date = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = 'Résultat Quiz'
        verbose_name_plural = 'Résultats Quiz'

    def __str__(self):
        return f"{self.etudiant.username} — {self.quiz} — {self.score}%"

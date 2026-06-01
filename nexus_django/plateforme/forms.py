from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from .models import ProfilUtilisateur, Cours, Lecon, Quiz, Question, Choix


class FormulaireConnexion(AuthenticationForm):
    """Formulaire de connexion personnalisé."""
    username = forms.CharField(
        label='Identifiant',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Votre identifiant',
            'autofocus': True,
        })
    )
    password = forms.CharField(
        label='Mot de passe',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': '••••••••',
        })
    )


class FormulaireInscription(UserCreationForm):
    """Formulaire d'inscription pour les nouveaux utilisateurs."""
    ROLE_CHOICES = [
        ('etudiant', 'Étudiant'),
        ('enseignant', 'Enseignant'),
    ]

    first_name = forms.CharField(
        label='Prénom',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Votre prénom'})
    )
    last_name = forms.CharField(
        label='Nom',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Votre nom'})
    )
    email = forms.EmailField(
        label='Adresse e-mail',
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'exemple@emsi.ma'})
    )
    role = forms.ChoiceField(
        label='Rôle',
        choices=ROLE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
        labels = {
            'username': 'Nom d\'utilisateur',
        }
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom d\'utilisateur unique'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({'class': 'form-control', 'placeholder': '••••••••'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control', 'placeholder': '••••••••'})
        self.fields['password1'].label = 'Mot de passe'
        self.fields['password2'].label = 'Confirmer le mot de passe'

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            ProfilUtilisateur.objects.create(
                utilisateur=user,
                role=self.cleaned_data['role']
            )
        return user


class FormulaireProfil(forms.ModelForm):
    """Formulaire de modification du profil."""
    first_name = forms.CharField(
        label='Prénom',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    last_name = forms.CharField(
        label='Nom',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    email = forms.EmailField(
        label='Adresse e-mail',
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = ProfilUtilisateur
        fields = ['bio', 'photo']
        labels = {'bio': 'Biographie', 'photo': 'Photo de profil'}
        widgets = {
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'photo': forms.FileInput(attrs={'class': 'form-control'}),
        }


class FormulaireCours(forms.ModelForm):
    """Formulaire de création/modification de cours."""
    class Meta:
        model = Cours
        fields = ['titre', 'description', 'image', 'est_publie']
        labels = {
            'titre': 'Titre du cours',
            'description': 'Description',
            'image': 'Image de couverture',
            'est_publie': 'Publier le cours',
        }
        widgets = {
            'titre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Titre du cours'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Description détaillée du cours...'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'est_publie': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class FormulaireLecon(forms.ModelForm):
    """Formulaire d'ajout/modification de leçon."""
    class Meta:
        model = Lecon
        fields = ['titre', 'contenu', 'fichier', 'ordre']
        labels = {
            'titre': 'Titre de la leçon',
            'contenu': 'Contenu',
            'fichier': 'Fichier PDF (optionnel)',
            'ordre': 'Ordre',
        }
        widgets = {
            'titre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Titre de la leçon'}),
            'contenu': forms.Textarea(attrs={'class': 'form-control', 'rows': 8, 'placeholder': 'Contenu de la leçon...'}),
            'fichier': forms.FileInput(attrs={'class': 'form-control'}),
            'ordre': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
        }


class FormulaireQuiz(forms.ModelForm):
    """Formulaire de création de quiz."""
    class Meta:
        model = Quiz
        fields = ['titre']
        labels = {'titre': 'Titre du quiz'}
        widgets = {
            'titre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Titre du quiz'}),
        }


class FormulaireQuestion(forms.ModelForm):
    """Formulaire d'ajout de question."""
    class Meta:
        model = Question
        fields = ['texte', 'ordre']
        labels = {'texte': 'Question', 'ordre': 'Ordre'}
        widgets = {
            'texte': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'ordre': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
        }


class FormulaireChoix(forms.ModelForm):
    """Formulaire d'ajout de choix de réponse."""
    class Meta:
        model = Choix
        fields = ['texte', 'est_correct']
        labels = {'texte': 'Texte du choix', 'est_correct': 'Réponse correcte ?'}
        widgets = {
            'texte': forms.TextInput(attrs={'class': 'form-control'}),
            'est_correct': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class FormulaireUtilisateurAdmin(forms.ModelForm):
    """Formulaire pour qu'un admin crée/modifie un utilisateur."""
    ROLE_CHOICES = [
        ('admin', 'Administrateur'),
        ('enseignant', 'Enseignant'),
        ('etudiant', 'Étudiant'),
    ]
    role = forms.ChoiceField(
        label='Rôle',
        choices=ROLE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
        labels = {
            'username': 'Identifiant',
            'first_name': 'Prénom',
            'last_name': 'Nom',
            'email': 'Adresse e-mail',
        }
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

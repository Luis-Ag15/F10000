from .forms import UserCreationFormWithEmail, ProfileForm, EmailForm, UsernameForm
from django.views.generic import CreateView
from django.views.generic.edit import UpdateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django import forms
from .models import Profile
from django.shortcuts import render
from django.conf import settings

import os
import uuid
import qrcode


# =========================
# REGISTRO
# =========================

class SignUpView(CreateView):
    form_class = UserCreationFormWithEmail
    template_name = 'registration/signup.html'

    def get_success_url(self):
        return reverse_lazy('login') + '?register'

    def get_form(self, form_class=None):
        form = super().get_form(form_class)

        # Código sugerido automático
        codigo = uuid.uuid4().hex[:8].upper()

        form.fields['username'].widget = forms.TextInput(attrs={
            'class': 'form-control mb-2',
            'placeholder': 'Nombre de usuario'
        })

        form.fields['first_name'].widget = forms.TextInput(attrs={
            'class': 'form-control mb-2',
            'placeholder': 'Nombre'
        })

        form.fields['last_name'].widget = forms.TextInput(attrs={
            'class': 'form-control mb-2',
            'placeholder': 'Código',
            'id': 'codigo',
            'value': codigo
        })

        form.fields['email'].widget = forms.EmailInput(attrs={
            'class': 'form-control mb-2',
            'placeholder': 'Dirección email'
        })

        form.fields['password1'].widget = forms.PasswordInput(attrs={
            'class': 'form-control mb-2',
            'placeholder': 'Contraseña'
        })

        form.fields['password2'].widget = forms.PasswordInput(attrs={
            'class': 'form-control mb-2',
            'placeholder': 'Repetir contraseña'
        })

        return form


# =========================
# PERFIL
# =========================

@method_decorator(login_required, name='dispatch')
class ProfileUpdate(UpdateView):
    form_class = ProfileForm
    success_url = reverse_lazy('profile')
    template_name = 'registration/profile_form.html'

    def get_object(self):
        profile, created = Profile.objects.get_or_create(user=self.request.user)
        return profile


@method_decorator(login_required, name='dispatch')
class EmailUpdate(UpdateView):
    form_class = EmailForm
    success_url = reverse_lazy('profile')
    template_name = 'registration/profile_email_form.html'

    def get_object(self):
        return self.request.user

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['email'].widget = forms.EmailInput(attrs={
            'class': 'form-control mb-2',
            'placeholder': 'Email'
        })
        return form


@method_decorator(login_required, name='dispatch')
class UsernameUpdate(UpdateView):
    form_class = UsernameForm
    success_url = reverse_lazy('profile')
    template_name = 'registration/profile_username_form.html'

    def get_object(self):
        return self.request.user

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['username'].widget = forms.TextInput(attrs={
            'class': 'form-control mb-2',
            'placeholder': 'Nombre de usuario'
        })
        return form


# =========================
# QR DEL CÓDIGO
# =========================

@login_required
def profile_qr(request):
    texto = request.user.last_name or request.user.username

    img = qrcode.make(texto)

    nombreQR = f"{uuid.uuid4().hex}.png"
    basepath = os.path.join(settings.MEDIA_ROOT, 'qrs')
    os.makedirs(basepath, exist_ok=True)

    img.save(os.path.join(basepath, nombreQR))

    ruta_imagen = f"{settings.MEDIA_URL}qrs/{nombreQR}"

    return render(request, 'registration/profile_qr.html', {
        'ruta_imagen': ruta_imagen,
        'texto': texto,
    })

from django import forms
from .models import Alumno
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

# ===============================
# Formulario Alumno
# ===============================

class AlumnoForm(forms.ModelForm):

    class Meta:
        model = Alumno
        fields = [
            'id',
            'nombre',
            'email',
            'telefono',
            'fecha',
            'foto_perfil',
            'foto_resultado'
        ]

        labels = {
            'id': 'ID Resultado',
        }

        widgets = {
            'id': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'ID / Código QR'
            }),
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre completo'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Correo electrónico'
            }),
            'telefono': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '55-4587-4578'
            }),
            'fecha': forms.DateInput(
                format='%d-%m-%Y',
                attrs={
                    'class': 'form-control',
                    'placeholder': 'DD-MM-AAAA'
                }
            ),
            'foto_perfil': forms.ClearableFileInput(attrs={
                'class': 'form-control-file'
            }),
            'foto_resultado': forms.ClearableFileInput(attrs={
                'class': 'form-control-file'
            }),
        }

    # ===============================
    # Formatos aceptados
    # ===============================

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['fecha'].input_formats = ['%d-%m-%Y']

    # ===============================
    # Validaciones
    # ===============================

    def clean_telefono(self):
        telefono = self.cleaned_data.get('telefono')

        if telefono:
            solo_numeros = ''.join(filter(str.isdigit, telefono))

            if len(solo_numeros) != 10:
                raise ValidationError(
                    "El teléfono debe contener 10 dígitos."
                )

            # Formato final obligatorio
            telefono = (
                f"{solo_numeros[:2]}-"
                f"{solo_numeros[2:6]}-"
                f"{solo_numeros[6:]}"
            )

        return telefono

    def clean_fecha(self):
        fecha = self.cleaned_data.get('fecha')
        return fecha

from django.db import models
import uuid
import os
from django.core.validators import RegexValidator

# ===============================
# Funciones para rutas de imágenes
# ===============================

def ruta_foto_perfil(instance, filename):
    ext = filename.split('.')[-1]
    nombre_archivo = f"{uuid.uuid4()}.{ext}"
    return os.path.join('images/perfil', nombre_archivo)

def ruta_foto_resultado(instance, filename):
    ext = filename.split('.')[-1]
    nombre_archivo = f"{uuid.uuid4()}.{ext}"
    return os.path.join('results/resultado', nombre_archivo)

# ===============================
# Modelo Alumno
# ===============================

class Alumno(models.Model):
    id = models.CharField(
        primary_key=True,
        max_length=50,
        verbose_name="ID Resultado"
    )

    nombre = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        verbose_name="Nombre"
    )

    email = models.EmailField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name="Correo electrónico"
    )

    # 🔹 TELÉFONO: 55-4587-4578
    telefono = models.CharField(
        max_length=12,
        null=True,
        blank=True,
        verbose_name="Teléfono",
        validators=[
            RegexValidator(
                regex=r'^\d{2}-\d{4}-\d{4}$',
                message="El teléfono debe tener el formato 55-4587-4578."
            )
        ]
    )

    # 🔹 FECHA REAL (DD-MM-AAAA en formulario)
    fecha = models.DateField(
        null=True,
        blank=True,
        verbose_name="Fecha"
    )

    foto_perfil = models.ImageField(
        upload_to=ruta_foto_perfil,
        null=True,
        blank=True,
        verbose_name="Foto de perfil"
    )

    foto_resultado = models.ImageField(
        upload_to=ruta_foto_resultado,
        null=True,
        blank=True,
        verbose_name="Foto de resultado"
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Creado"
    )

    updated = models.DateTimeField(
        auto_now=True,
        verbose_name="Actualizado"
    )

    def __str__(self):
        return f"{self.nombre} - {self.telefono}"

    class Meta:
        db_table = 'alumnos'
        ordering = ['-created_at']
        verbose_name = "Alumno"
        verbose_name_plural = "Alumnos"

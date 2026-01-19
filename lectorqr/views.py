from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.views.generic import CreateView, TemplateView
from django.http import JsonResponse
from django.contrib import messages

from . import models
from .models import Alumno
from .forms import AlumnoForm


# ======================================================
# REGISTRO DE RESULTADOS (SOLO STAFF Y SUPERUSERS)
# ======================================================
class AlumnoCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Alumno
    form_class = AlumnoForm
    template_name = 'lectorqr/alumno_form.html'
    login_url = reverse_lazy('login')

    # 🔐 Validación de permisos
    def test_func(self):
        return self.request.user.is_staff or self.request.user.is_superuser

    def form_valid(self, form):
        self.object = form.save()
        messages.success(
            self.request,
            "Resultados registrados exitosamente"
        )
        return redirect('alumno_create')


# ======================================================
# PÁGINA DEL SCANNER (SOLO STAFF Y SUPERUSERS)
# ======================================================
class ScannerPageView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = "lectorqr/scanner.html"
    login_url = reverse_lazy('admin:login')

    # 🔐 Validación de permisos
    def test_func(self):
        return self.request.user.is_staff or self.request.user.is_superuser


# ======================================================
# CONSULTA POR QR (SOLO STAFF Y SUPERUSERS)
# ======================================================
def view_detalles_alumno(request):
    if not request.user.is_authenticated or not (
        request.user.is_staff or request.user.is_superuser
    ):
        return JsonResponse({'error': 'Acceso no autorizado'}, status=403)

    if request.method == 'POST':
        result_qr = request.POST.get('datoqr')

        try:
            alumnoBD = models.Alumno.objects.get(id=result_qr)
            return JsonResponse({'id_alumno': alumnoBD.id})

        except models.Alumno.DoesNotExist:
            return JsonResponse({'id_alumno': 0})

    return JsonResponse({'error': 'Solicitud no válida'}, status=400)


# ======================================================
# DETALLES DEL ALUMNO (SOLO STAFF Y SUPERUSERS)
# ======================================================
def detalles_alumno(request):
    if not request.user.is_authenticated or not (
        request.user.is_staff or request.user.is_superuser
    ):
        return render(
            request,
            "error.html",
            {"error_message": "No tienes permisos para acceder a esta sección"}
        )

    id_alumno = request.GET.get('id')

    if id_alumno:
        try:
            alumno = models.Alumno.objects.get(id=id_alumno)
            return render(
                request,
                "lectorqr/detalles_busqueda.html",
                {"alumno": alumno}
            )

        except models.Alumno.DoesNotExist:
            return render(
                request,
                "error.html",
                {
                    "error_message": (
                        f"No existe ningún registro para el ID de alumno: {id_alumno}"
                    )
                }
            )

    return JsonResponse(
        {"error": "No se proporcionó el parámetro 'id' en la URL."},
        status=400
    )


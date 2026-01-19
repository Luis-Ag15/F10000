from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.views.generic.base import TemplateView
from django.http import JsonResponse
from django.views.generic import CreateView
from django.contrib import messages
from . import models
from .models import Alumno
from .forms import AlumnoForm


class AlumnoCreateView(LoginRequiredMixin, CreateView):
    model = Alumno
    form_class = AlumnoForm
    template_name = 'lectorqr/alumno_form.html'
    login_url = reverse_lazy('login')

    def form_valid(self, form):
        self.object = form.save()
        messages.success(
            self.request,
            "Resultados registrados exitosamente"
        )
        # 🔹 REDIRIGE A /resultados/
        return redirect('alumno_create')


class ScannerPageView(LoginRequiredMixin, TemplateView):
    template_name = "lectorqr/scanner.html"
    login_url = reverse_lazy('admin:login')


def view_detalles_alumno(request):
    if request.method == 'POST':
        result_qr = request.POST.get('datoqr')

        try:
            alumnoBD = models.Alumno.objects.get(id=result_qr)
            return JsonResponse({'id_alumno': alumnoBD.id})

        except models.Alumno.DoesNotExist:
            return JsonResponse({'id_alumno': 0})

    return JsonResponse({'error': 'Solicitud no válida'})


def detalles_alumno(request):
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
        {"error": "No se proporcionó el parámetro 'id' en la URL."}
    )

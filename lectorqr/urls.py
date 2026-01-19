from django.urls import path
from . import views
from .views import ScannerPageView

urlpatterns = [

    path('scanner/', ScannerPageView.as_view(), name='scanner'),
    path('buscar-alumno/', views.view_detalles_alumno, name='view_detalles_alumno'),
    path('detalles-busqueda/', views.detalles_alumno, name='detalles_alumno'),
    path('resultados/', views.AlumnoCreateView.as_view(), name='alumno_create'),

]


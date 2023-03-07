from django.urls import path
from . import views
from django.conf.urls import handler403
from .views import error_403

handler403 = error_403


urlpatterns = [
    path("", views.Home, name="Home"),
    path('Solicitud', views.FormSolicitud, name='solicitud'),
    path('login/', views.login_view, name='login'),
    path('salir', views.salir, name='salir'),
    path('error_403', error_403, name='error_403'),
    path('listadoSolicitudes', views.listaSolicitudes, name='listaSolicitudes'),
    path('editarSolicitud/<codigo>', views.editarSolicitud, name='editarSolicitud'),
    path('modificarSolicitud/', views.modificarSolicitud, name='modificarSolicitud'),
    path('eliminarSolicitud/<codigo>/', views.eliminarSolicitud, name='eliminarSolicitud')
]

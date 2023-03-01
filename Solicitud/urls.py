from django.urls import path
from . import views

urlpatterns = [
    path("", views.Home, name="Home"),
    path('Solicitud', views.FormSolicitud, name='solicitud'),
    path('login/', views.login_view, name='login'),
    path('salir', views.salir, name='salir')
]

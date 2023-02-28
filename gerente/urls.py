from django.urls import path
from . import views

urlpatterns = [
    path('Gerencia', views.Inicio, name='gerente')
]

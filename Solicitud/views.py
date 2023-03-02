from django.shortcuts import render
from django.core.exceptions import PermissionDenied
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import permission_required, login_required

from .forms import AgregarSolicitud
from .models import Solicitud
import pdb

def error_403(request, exception):
    return render(request, '403.html', {'message': 'No tienes permisos para acceder a esta página.'})

@permission_required('Solicitud.add_solicitud', login_url='login/', raise_exception=True)
@login_required
def FormSolicitud(request):
    if not request.user.has_perm('Solicitud.add_solicitud'):
        raise PermissionDenied('No tiene permiso para realizar la accion')
    form = AgregarSolicitud(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        miSolicitud = Solicitud(
        titulo = form.cleaned_data.get('titulo'),
        detalle = form.cleaned_data.get('detalle'),
        fecha_Fin = form.cleaned_data.get('fechaLimite'),
        usuario = request.user,
        departamento = form.cleaned_data['departamento'],
        etapa = form.cleaned_data.get('etapa'))
        print(form.cleaned_data.get('departamento'))
        print(form.cleaned_data.get('fechaLimite'))

        miSolicitud.save()
        return redirect('Home')
    return render(request, 'Solicitud.html', {'form': form})

        

def envioSolicitud(request):
    pass

def login_view(request):
    username = request.POST.get('username')
    password = request.POST.get('Password')

    if request.method == 'POST':
        #pdb.set_trace()
        username = request.POST.get('username')
        password = request.POST.get('Password')
        usuario = authenticate(username=username, password=password)
        if usuario:
            login(request,usuario)
            return redirect('Home')
        else:
            messages.error(request, 'Nombre de usuario o contraseña incorrectos')
    return render(request, 'login.html')


def salir(request):
    logout(request)
    return redirect('Home')

def Home(request):
    return render(request, 'home.html', {
        'Jefe': 'Area'
    })
from django.shortcuts import render


from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import permission_required, login_required
import pdb

#@permission_required('Solicitud.add_Solicitud')
@login_required
def FormSolicitud(request):
    return render(request, 'solicitud.html')

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
            return redirect('solicitud')
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
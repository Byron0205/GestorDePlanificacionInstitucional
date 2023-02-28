from django.shortcuts import render


def Home(request):
    return render(request, 'home.html', {
        'Jefe': 'Area'
    })
# Create your views here.
def FormSolicitud(request):
    return render(request, 'solicitud.html')
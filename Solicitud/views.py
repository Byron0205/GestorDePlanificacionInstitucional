from django.shortcuts import render, get_object_or_404
from django.core.exceptions import PermissionDenied
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import permission_required, login_required

#redirigir a pdf
from django.http import FileResponse

#generar reporte
from reportlab.lib.pagesizes import LETTER
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
import pandas as pd
import matplotlib.pyplot as plt

from django.contrib import messages

from .forms import AgregarSolicitud #revisarSolicitud
from .models import Solicitud, Departamento, estado,Etapa
import pdb

def error_403(request, exception):
    return render(request, '403.html', {'message': 'No tienes permisos para acceder a esta página.'})

@login_required
@permission_required('Solicitud.add_solicitud', login_url='login/', raise_exception=True)
def FormSolicitud(request):
    #validar si el usuario tiene el permiso
    if not request.user.has_perm('Solicitud.add_solicitud'):
        raise PermissionDenied('No tiene permiso para realizar la accion')
    form = AgregarSolicitud(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        miSolicitud = Solicitud(
        titulo = form.cleaned_data.get('titulo'),
        detalle = form.cleaned_data.get('detalle'),
        fecha_Inicio = form.cleaned_data.get('fechaInicio'),
        fecha_Fin = form.cleaned_data.get('fechaLimite'),
        usuario = request.user,
        departamento = form.cleaned_data['departamento'],
        etapas = form.cleaned_data.get('etapa'))
        print(form.cleaned_data.get('departamento'))
        print(form.cleaned_data.get('fechaInicio'))

        miSolicitud.save()
        messages.success(request, 'Solicitud agregada correctamente')
        #agregar redireccion a form para etapas

        return redirect('etapas/')
    return render(request, 'Solicitud.html', {'form': form})



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
            messages.success(request, f'Bienvenido {usuario.get_username()}')
            return redirect('Home')
        else:
            messages.error(request, 'Nombre de usuario o contraseña incorrectos')
    return render(request, 'login.html')


def salir(request):
    logout(request)
    return redirect('Home')

def Home(request):
    return render(request, 'home.html')

@login_required
@permission_required('Solicitud.view_solicitud', login_url='login/')
def listaSolicitudes(request):
    return render(request, 'listado.html')

#revisar obtener solicitud detallada

def editarSolicitud(request, codigo):
    if not request.user.has_perm('Solicitud.change_solicitud'):
        messages.error(request, 'No tiene permiso de modificar solicitudes')
    solicitud = Solicitud.objects.get(id=codigo)
    Departamentos = Departamento.objects.all()
    return render(request,'actualizarSolicitud.html',{
        's': solicitud,
        'dptos': Departamentos
    })

@permission_required('Solicitud.change_solicitud', login_url='login/')
def modificarSolicitud(request):
    if not request.user.has_perm('Solicitud.change_solicitud'):
        messages.error(request, 'No tiene permiso de modificar solicitudes')
        return redirect('Home')
    id = request.POST['id']
    titulo = request.POST['titulo']
    departamento = get_object_or_404(Departamento, pk=request.POST['departamento'])
    fechaI= request.POST['fechainicio']
    fechaF= request.POST['fechafin']
    completadas = request.POST['completadas']
    detalle = request.POST['detalle']

    solicitud = get_object_or_404(Solicitud, pk=id)
    solicitud.titulo = titulo
    solicitud.departamento =departamento
    solicitud.fecha_Inicio = fechaI
    solicitud.fecha_Fin= fechaF
    solicitud.detalle= detalle
    solicitud.completadas = completadas
    if int(completadas) > 0 and int(completadas) < int(request.POST['etapa']):
        estadoSolicitud = get_object_or_404(estado, pk=2)
        solicitud.estados = estadoSolicitud
    elif int(completadas) == int(request.POST['etapa']) :
        estadoSolicitud = get_object_or_404(estado, pk=3)
        solicitud.estados = estadoSolicitud
    solicitud.save()

    return redirect(f'/editarSolicitud/{id}')
    

def listaSolicitudes(request):
    solicitudes = Solicitud.objects.all()
    return render(request, "listado.html", {
        'solicitudes': solicitudes,
    })


def eliminarSolicitud(request, codigo):
    solicitud = Solicitud.objects.get(id=codigo)
    solicitud.delete()
    return redirect('listaSolicitudes')

def informe(request):
    completados=0
    enProceso=0
    sinEmpezar=0
    posicion= 350
    contador =1

    Solicitudes = Solicitud.objects.all()
    for s in Solicitudes:
        if s.completadas == s.etapas:
            completados+=1
        elif s.completadas>0 and s.completadas < s.etapas:
            enProceso+=1
        elif s.completadas==0:
            sinEmpezar+=1
    stats = {'x': ['Completado', 'En progreso', 'Sin Empezar'],
            'y': [completados,enProceso,sinEmpezar]}
    df= pd.DataFrame(stats)

    fig, ax = plt.subplots(figsize=(8,6))

    df.plot(x='x', y='y', kind='barh',ax=ax)
    plt.title('Estadisticas de proyectos')
    plt.ylabel('Estados')
    plt.xlabel('Cantidades')
    plt.savefig('graficoProyectos.png')

    pdf = canvas.Canvas('static/archivos/Resumen_proyectos.pdf',pagesize=LETTER)

    pdf.drawString(100,700, 'Resumen de proyectos de la empresa')
    pdf.drawString(100,750,'Remodelaciones Hidalgo ')
    pdf.drawImage('graficoProyectos.png',100,400, width=6*inch,height=4*inch)
    for s in Solicitudes:
        pdf.drawString(100,posicion, f'{contador}. {s.titulo} ({s.estado})')
        posicion-=20
        pdf.drawString(115,posicion, f'Fecha propuesta deIncio: {s.fecha_Inicio}')
        posicion-=20
        pdf.drawString(115,posicion, f'Fecha propuesta de fin: {s.fecha_Fin}')
        posicion-=20
        pdf.drawString(115,posicion, f'{s.detalle}')
        posicion-=30
        contador+=1


    pdf.save()

    messages.success(request, 'Informe generado correctamente')
    return FileResponse(open('static/archivos/Resumen_proyectos.pdf', 'rb'), content_type='application/pdf')



def DetallarEtapas(request):
    fases =[]
    if not request.user.has_perm('Solicitud.change_solicitud'):
        messages.error(request, 'No tiene permiso de crear solicitudes')
    solicitud = Solicitud.objects.latest('agregado')
    etapas=solicitud.etapas
    for e in range(0, etapas):
        fases.append(e+1)
        print(fases[e])
    return render(request,'etapas.html', {
        'etapas': fases,
        'solicitud': solicitud
        })


def guardarEtapas(request):
    
    solicitud = Solicitud.objects.get(id=request.POST['idSolicitud'])
    etapas = solicitud.etapas
    for e in range (0,etapas):
        nuevaEtapa = Etapa(
            solicitud=get_object_or_404(Solicitud, pk=request.POST['idSolicitud']),
            Detalle= request.POST[f'detalle{e+1}'],
            NumEtapa= e+1
        )
        nuevaEtapa.save()
    messages.success(request,'Proceso finalizado correctamente')
    return redirect('Home')
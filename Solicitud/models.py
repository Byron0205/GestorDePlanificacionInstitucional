from django.db import models
import datetime
from django.contrib.auth.models import User
from django.utils.timezone import now



class estado(models.Model):
    idEstado = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=20)

    def __str__(self):
        return self.nombre

class Departamento(models.Model):
    idDepartamento = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=20, null=False)

    def __str__(self):
        return self.nombre
    


class Solicitud(models.Model):
    id = models.AutoField(primary_key=True)
    titulo = models.CharField(max_length=30, null=False)
    detalle = models.CharField(max_length=300, null=False)
    fecha_Inicio = models.DateField(default=now())
    fecha_Fin = models.DateField(null=False)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    departamento = models.ForeignKey(Departamento, on_delete=models.CASCADE)
    etapas = models.SmallIntegerField()
    completadas = models.SmallIntegerField(default=0)
    estado = models.ForeignKey(estado, on_delete=models.CASCADE, default=1)
    agregado = models.DateTimeField(default=now())

    def __str__(self):
        return self.titulo

class Etapa(models.Model):
    id= models.AutoField(primary_key=True)
    solicitud = models.ForeignKey(Solicitud, on_delete=models.CASCADE)
    Detalle = models.CharField(max_length=300, null=False)
    NumEtapa = models.SmallIntegerField()

    def __str__(self):
        return "Etapa: "+str(self.NumEtapa) +" de proyecto: "+str(self.solicitud)
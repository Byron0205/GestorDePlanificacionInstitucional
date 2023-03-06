from django.contrib import admin
from .models import Solicitud, Departamento,estado
# Register your models here.

admin.site.register(Solicitud)
admin.site.register(estado)
admin.site.register(Departamento)

from django.contrib import admin
from .models import (
    Llave, Ruta,  Estacion, 
    MovimientosEstacion, Coordinador, Operador,
    ReporteDiario, RegistroDespliegue, Item)

# Register your models here.

admin.site.register(Llave)
admin.site.register(Ruta)
@admin.register(Estacion)
class EstacionAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Estacion._meta.fields]
    search_fields = ['codigo_equipo', 'nro_estacion', 'llave__nro_estacion', 'fase', 'estado_computadora']
    list_filter = ['estado_computadora', 'fase']
    
#admin.site.register(MovimientosEstacion)
admin.site.register(Coordinador)
admin.site.register(Operador)
admin.site.register(ReporteDiario)
admin.site.register(RegistroDespliegue)
admin.site.register(Item)

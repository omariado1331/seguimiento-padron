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
    # dentro de EstacionAdmin
    obs_fields = [f'obs_{c}' for c in [
        'computadora','monitor','escaner','impresora','pad_firmas',
        'camara','decadactilar','hub_usb','estabilizador_energia',
        'pila_madre','memorias_ram','disco_duro','teclado','regulador_voltaje'
    ]]
    fieldsets = (
        ('Hardware', {'fields': (
            'estado_computadora','obs_computadora',
            'estado_monitor','obs_monitor',
            'estado_escaner','obs_escaner',
            'estado_impresora','obs_impresora',
            'estado_pad_firmas','obs_pad_firmas',
            'estado_camara','obs_camara',
            'estado_decadactilar','obs_decadactilar',
            'estado_hub_usb','obs_hub_usb',
            'estado_estabilizador_energia','obs_estabilizador_energia',
            'estado_pila_madre','obs_pila_madre',
            'estado_memorias_ram','obs_memorias_ram',
            'estado_disco_duro','obs_disco_duro',
            'estado_teclado','obs_teclado',
            'estado_regulador_voltaje','obs_regulador_voltaje',
        )}),
    )
#admin.site.register(MovimientosEstacion)
admin.site.register(Coordinador)
admin.site.register(Operador)
admin.site.register(ReporteDiario)
admin.site.register(RegistroDespliegue)
admin.site.register(Item)

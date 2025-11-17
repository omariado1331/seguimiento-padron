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
    list_display = ['codigo_equipo', 'nro_estacion', 'fase', 'estado_computadora']
    search_fields = ['codigo_equipo', 'nro_estacion']
    list_filter = ['fase', 'estado_computadora']

    # Campos “estado” y su “obs” en pareja → aparecerán lado a lado
    fieldsets = (
        ('Datos generales', {
            'fields': ('codigo_equipo', 'nro_estacion', 'fase', 'tipo_estacion', 'modelo','llave')
        }),
        ('Hardware', {
            'description': 'Estado del hardware y sus observaciones',
            'fields': (
                # Cada pareja → izquierda: estado, derecha: observación
                ('estado_computadora', 'obs_computadora'),
                ('estado_monitor', 'obs_monitor'),
                ('estado_pad_firmas', 'obs_pad_firmas'),
                ('estado_decadactilar', 'obs_decadactilar'),
                ('estado_hub_usb', 'obs_hub_usb'),
                ('estado_estabilizador_energia', 'obs_estabilizador_energia'),
                ('estado_pila_madre', 'obs_pila_madre'),
                ('estado_memorias_ram', 'obs_memorias_ram'),
                ('estado_disco_duro', 'obs_disco_duro'),
                ('estado_teclado', 'obs_teclado'),
                ('estado_regulador_voltaje', 'obs_regulador_voltaje'),
                ('estado_escaner','modelo_escaner', 'obs_escaner'),
                ('estado_impresora','modelo_impresora', 'obs_impresora'),
                ('estado_camara', 'modelo_camara', 'obs_camara'),
            )
        }),
        ('Accesorios', {
            'fields': (
                'cable_extensor', 'tripode', 'banner',
                'adaptador_3a2', 'monitor_pc', 'testeo_pila'
            )
        }),
        ('Otros', {
            'fields': ('asignada', 'observacion')
        })
    )
#admin.site.register(MovimientosEstacion)
admin.site.register(Coordinador)
admin.site.register(Operador)
admin.site.register(ReporteDiario)
admin.site.register(RegistroDespliegue)
admin.site.register(Item)

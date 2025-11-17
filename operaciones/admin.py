from django.contrib import admin
from .models import (
    Llave, Ruta, Estacion, MovimientosEstacion,
    Coordinador, Operador, ReporteDiario,
    RegistroDespliegue, Item
)

# ---------------- Estacion  ----------------
@admin.register(Estacion)
class EstacionAdmin(admin.ModelAdmin):
    list_display = [f.name for f in Estacion._meta.fields]
    search_fields = ['codigo_equipo', 'nro_estacion']
    list_filter = ['fase', 'estado_computadora']

    fieldsets = (
        ('Datos generales', {
            'fields': ('codigo_equipo', 'nro_estacion', 'fase', 'tipo_estacion', 'modelo', 'llave')
        }),
        ('Hardware', {
            'description': 'Estado del hardware y sus observaciones',
            'fields': (
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
                ('estado_escaner', 'modelo_escaner', 'obs_escaner'),
                ('estado_impresora', 'modelo_impresora', 'obs_impresora'),
                ('estado_camara', 'modelo_camara', 'obs_camara'),
            )
        }),
        ('Accesorios', {
            'fields': (
                ('cable_extensor', 'obs_cable_extensor'),
                ('tripode',        'obs_tripode'),
                ('banner',         'obs_banner'),
                ('adaptador_3a2',  'obs_adaptador_3a2'),
                'monitor_pc',
                'testeo_pila'
            )
        }),
        ('Otros', {
            'fields': ('asignada', 'observacion')
        })
    )

# ---------------- Llave ----------------
@admin.register(Llave)
class LlaveAdmin(admin.ModelAdmin):
    list_display = ['nro_estacion', 'contador_r', 'contador_c']
    search_fields = ['nro_estacion']
    list_filter = ['nro_estacion']

# ---------------- Ruta ----------------
@admin.register(Ruta)
class RutaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'fecha_creacion']
    search_fields = ['nombre']
    list_filter = ['fecha_creacion']

# ---------------- MovimientosEstacion ----------------
@admin.register(MovimientosEstacion)
class MovimientosEstacionAdmin(admin.ModelAdmin):
    list_display = ['estacion', 'fecha_movimiento']
    search_fields = ['estacion__codigo_equipo']
    list_filter = ['fecha_movimiento']

# ---------------- Coordinador ----------------
@admin.register(Coordinador)
class CoordinadorAdmin(admin.ModelAdmin):
    list_display = ['user', 'estado', 'ruta', 'correo', 'celular']
    search_fields = ['user__username', 'nombre', 'apellido_paterno', 'correo', 'celular']
    list_filter = ['estado', 'ruta']

# ---------------- Operador ----------------
@admin.register(Operador)
class OperadorAdmin(admin.ModelAdmin):
    list_display = ['user', 'tipo_operador', 'estado', 'coordinador', 'estacion']
    search_fields = ['user__username', 'nombre', 'apellido_paterno', 'correo', 'celular']
    list_filter = ['estado', 'tipo_operador', 'coordinador', 'estacion']

# ---------------- ReporteDiario ----------------
@admin.register(ReporteDiario)
class ReporteDiarioAdmin(admin.ModelAdmin):
    list_display = ['operador', 'estacion', 'fecha_reporte', 'registro_c', 'registro_r', 'estado']
    search_fields = ['operador__user__username', 'estacion__codigo_equipo']
    list_filter = ['fecha_reporte', 'estado', 'sincronizar']

# ---------------- RegistroDespliegue ----------------
@admin.register(RegistroDespliegue)
class RegistroDespliegueAdmin(admin.ModelAdmin):
    list_display = ['operador', 'destino', 'descripcion_reporte', 'fecha_hora', 'sincronizar']
    search_fields = ['operador__user__username', 'destino']
    list_filter = ['descripcion_reporte', 'sincronizar', 'fecha_hora']

# ---------------- Item ----------------
@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ['codigo_item', 'serie_item', 'tipo', 'asignado_operador']
    search_fields = ['codigo_item', 'serie_item']
    list_filter = ['tipo', 'asignado_operador']
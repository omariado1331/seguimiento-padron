from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Llave(models.Model):
    nro_estacion = models.IntegerField(default=0, unique=True)
    contador_r = models.IntegerField(default=0)
    contador_c = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.nro_estacion}-C:{self.contador_c}:-R:{self.contador_r}"

class Ruta(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.nombre

class Estacion(models.Model):
    codigo_equipo = models.CharField(max_length=56, unique=True, blank=True )
    llave = models.ForeignKey(Llave, on_delete=models.CASCADE, null=True, blank=True)
    nro_estacion = models.IntegerField(default=0, unique=True, null=True, blank=True)
    ESTACION_CHOICES = [
        ('FIJA', 'FIJA'),
        ('MOVIL', 'MOVIL'),
    ]
    MODELO_CHOICES = [
        ('DELL OPTIPLEX 360', 'DELL OPTIPLEX 360'),
        ('DELL OPTIPLEX 390', 'DELL OPTIPLEX 390'),
        ('DELL E5500', 'DELL E5500'),
        ('DELL E5520', 'DELL E5520'),
    ]
    tipo_estacion = models.CharField(
        max_length=255, 
        choices=ESTACION_CHOICES,
        blank=True,
        null=True
    )
    modelo = models.CharField(
        max_length=255, 
        choices=MODELO_CHOICES,
        blank=True,
        null=True
    )
    FASES_CHOICES = [
        ('Recepcionado', 'Recepcionado'),
        ('En Revision', 'En Revision'),
        ('Revisado funcional', 'Revisado funcional'),
        ('En Clonacion', 'En Clonacion'),
        ('Clonado', 'Clonado'),
        ('En Masterizacion', 'En Masterizacion'),
        ('Masterizado', 'Masterizado'),
        ('Asignado', 'Asignado'),
        ('Desplegado', 'Desplegado'),
        ('En mantenimiento', 'En mantenimiento'),
    ]
    fase = models.CharField(
        max_length=56,
        choices=FASES_CHOICES,
        default='Recepcionado'
    )
    FUNCIONALIDAD_CHOICES = [
        ('Buena', 'Buena'),
        ('Mala', 'Mala'),
    ]
    ESTADO_CHOICES = [
        ('defectuoso', 'Defectuoso'),
        ('contingencia', 'Contingencia'),
        ('reparacion', 'En Reparacion'),
        ('funcional', 'Funcional'),
        ('nuevo', 'Nuevo'),
    ]
    estado_computadora = models.CharField(
        max_length=32,
        choices=ESTADO_CHOICES,
        default='funcional'
    )
    estado_monitor = models.CharField(
        max_length=24,
        choices=FUNCIONALIDAD_CHOICES,
        default='Buena'
    )
    estado_escaner  = models.CharField(
        max_length=24,
        choices=FUNCIONALIDAD_CHOICES,
        default='Buena'
    )
    estado_impresora  = models.CharField(
        max_length=24,
        choices=FUNCIONALIDAD_CHOICES,
        default='Buena'
    )
    estado_pad_firmas  = models.CharField(
        max_length=24,
        choices=FUNCIONALIDAD_CHOICES,
        default='Buena'
    )
    estado_camara  = models.CharField(
        max_length=24,
        choices=FUNCIONALIDAD_CHOICES,
        default='Buena'
    )
    estado_decadactilar  = models.CharField(
        max_length=24,
        choices=FUNCIONALIDAD_CHOICES,
        default='Buena'
    )
    estado_hub_usb  = models.CharField(
        max_length=24,
        choices=FUNCIONALIDAD_CHOICES,
        default='Buena'
    )
    estado_estabilizador_energia  = models.CharField(
        max_length=24,
        choices=FUNCIONALIDAD_CHOICES,
        default='Buena'
    )
    estado_pila_madre  = models.CharField(
        max_length=24,
        choices=FUNCIONALIDAD_CHOICES,
        default='Buena'
    )
    estado_memorias_ram  = models.CharField(
        max_length=24,
        choices=FUNCIONALIDAD_CHOICES,
        default='Buena'
    )
    estado_disco_duro  = models.CharField(
        max_length=24,
        choices=FUNCIONALIDAD_CHOICES,
        default='Buena'
    )
    cable_extensor = models.BooleanField(default=False)
    tripode = models.BooleanField(default=False)
    banner = models.BooleanField(default=False)
    adaptador_3a2 = models.BooleanField(default=False)
    monitor_pc =models.BooleanField(default=False)
    testeo_pila = models.BooleanField(default=False)
    asignada = models.BooleanField(default=False)
    observacion = models.TextField(blank=True)
    recepcionado = models.BooleanField(default=False)
    revisado = models.BooleanField(default=False)
    clonado = models.BooleanField(default=False)
    masterizado = models.BooleanField(default=False)
    asignado = models.BooleanField(default=False)
    def __str__(self):
        return f"{self.codigo_equipo} - Llave: {self.llave}"
    
class MovimientosEstacion(models.Model):
    estacion = models.ForeignKey(Estacion, on_delete=models.CASCADE)
    fecha_movimiento = models.DateTimeField(auto_now_add=True)
    descripcion = models.TextField()

    def __str__(self):
        return f"Movimiento de {self.estacion.codigo_equipo} el {self.fecha_movimiento}"
    
class Coordinador(models.Model):
    ESTADO_CHOICES = [
        ('postulante', 'Postulante'),
        ('seleccionado', 'Seleccionado'),
        ('contratado', 'Contratado'),
        ('sin_firmar_contrato', 'Sin Firmar Contrato'),
        ('renuncia', 'Renuncia'),
    ]
    estado = models.CharField(
        max_length=20,
        choices=ESTADO_CHOICES,
        default='postulante'
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    ruta = models.ForeignKey(Ruta, on_delete=models.CASCADE, null=True, blank=True)
    nombre = models.CharField(max_length=100, null=True, blank=True)
    apellido_paterno = models.CharField(max_length=100, null=True, blank=True)
    apellido_materno = models.CharField(max_length=100, null=True, blank=True)
    direccion = models.CharField(max_length=200, blank=True, null=True)
    correo = models.EmailField(unique=True, null=True, blank=True)
    celular = models.CharField(max_length=15, unique=True, null=True, blank=True)

    def __str__(self):
        return self.user.username

class Operador(models.Model):
    ESTADO_CHOICES = [
        ('postulante', 'Postulante'),
        ('seleccionado', 'Seleccionado'),
        ('contratado', 'Contratado'),
        ('sin_firmar_contrato', 'Sin Firmar Contrato'),
        ('renuncia', 'Renuncia'),
    ]
    TIPO_OPERADOR_CHOICES = [
        ('Operador Urbano', 'Operador Urbano'),
        ('Operador Rural', 'Operador Rural'),
    ]
    estado = models.CharField(
        max_length=20,
        choices=ESTADO_CHOICES,
        default='postulante'
    )
    tipo_operador = models.CharField(
        max_length=20,
        choices=TIPO_OPERADOR_CHOICES
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    ruta = models.ForeignKey(Ruta, null=True, blank=True, on_delete=models.SET_NULL)
    coordinador = models.ForeignKey(Coordinador, null=True, blank=True, on_delete=models.SET_NULL)
    estacion = models.ForeignKey(Estacion, null=True, blank=True, on_delete=models.SET_NULL)  
    nombre = models.CharField(max_length=100, null=True, blank=True)
    apellido_paterno = models.CharField(max_length=100, null=True, blank=True)
    apellido_materno = models.CharField(max_length=100, null=True, blank=True)
    direccion = models.CharField(max_length=200, blank=True, null=True)
    correo = models.EmailField(unique=True, null=True, blank=True)
    celular = models.CharField(max_length=15, unique=True, null=True, blank=True)

    def __str__(self):
        return self.user.username


class ReporteDiario(models.Model):
    operador = models.ForeignKey(Operador, on_delete=models.CASCADE)
    estacion = models.ForeignKey(Estacion, on_delete=models.CASCADE)
    fecha_reporte = models.DateTimeField(null=True, blank=True)
    contador_inicial_c = models.IntegerField(default=0)
    contador_final_c = models.IntegerField(default=0)
    contador_inicial_r = models.IntegerField(default=0)
    contador_final_r = models.IntegerField(default=0)
    incidencias = models.TextField(blank=True)
    observaciones = models.TextField(blank=True)
    fecha_registro = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    sincronizar = models.BooleanField(default=False)  
    estado = models.CharField(max_length=25, blank = True)
    def __str__(self):
        return f"{self.operador.user.username} Inicio {self.estacion.codigo_equipo} C{self.contador_inicial_c} R{self.contador_inicial_r} - Fin {self.contador_final_c} R{self.contador_final_r} el {self.fecha_reporte}"

class RegistroDespliegue(models.Model):
    operador = models.ForeignKey(Operador, on_delete=models.CASCADE)
    destino = models.CharField(max_length=255, null=True)
    latitud = models.CharField(max_length=255, null=True)
    longitud = models.CharField(max_length=255, null=True)
    DESCRIPCION_REPORTE_CHOICES = [
        ('Despliegue', 'Despliegue'),
        ('En camino', 'En camino'),
        ('Incidencia', 'Incidencia'),
        ('Llego a destino', 'Llego a destino')
    ]
    descripcion_reporte = models.CharField(
        max_length= 56,
        choices= DESCRIPCION_REPORTE_CHOICES,
        null = True
    )
    estado = models.CharField(max_length=255, null=True)
    sincronizar = models.BooleanField(default=False)    
    observaciones = models.TextField(blank=True)
    incidencias = models.TextField(blank=True)
    fecha_hora = models.DateTimeField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.operador.user.username}-{self.destino}--{self.descripcion_reporte}"

class Item(models.Model):
    TIPO_CHOICES = [
        ('Periferico', 'Periferico'),
        ('Herramiento', 'Herramienta'),
        ('Insumo', 'Insumo'),
        ('Accesorio', 'Accesorio'),
    ]
    tipo = models.CharField(
        max_length=32,
        choices= TIPO_CHOICES,
        null=True,
        blank=True
    )
    codigo_item = models.CharField(max_length=55, blank=True, null=True)
    serie_item = models.CharField(max_length=55, blank=True, null=True)
    asignado_operador = models.BooleanField(default=False)
    operador = models.ForeignKey(Operador, on_delete=models.CASCADE, null=True, blank=True)
    descripcion = models.TextField(blank=True)
    observacion = models.TextField(blank=True)

from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import (
    Llave, Ruta, Estacion, 
    MovimientosEstacion, Coordinador, Operador,
    ReporteDiario, RegistroDespliegue, Item, CentroEmpadronamiento,
    UbicacionesOperador    
)

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        token['group'] = user.groups.first().name if user.groups.exists() else None
        return token

    def _datos_personales(self, modelo, user):
        """Devuelve el dict común de datos personales o None si no existe."""
        try:
            obj = modelo.objects.get(user=user)
            return {
                "id": obj.id,
                "nombre": obj.nombre,
                "apellido_paterno": obj.apellido_paterno,
                "apellido_materno": obj.apellido_materno,
                "celular": obj.celular,
            }
        except modelo.DoesNotExist:
            return None

    def validate(self, attrs):
        data = super().validate(attrs)
        user = self.user

        # base user
        data['user'] = {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'groups': [g.name for g in user.groups.all()],
        }

        # ====== 1. CASO COORDINADOR ======
        if user.groups.filter(name='Coordinador').exists():
            coord_data = self._datos_personales(Coordinador, user)
            if not coord_data:
                data['user']['coordinador'] = None
                data['user']['operadores_asignados'] = []
                data['user']['operador'] = None
                return data

            coord = Coordinador.objects.get(user=user)
            operadores = Operador.objects.filter(
                coordinador=coord
            ).select_related('user', 'ruta', 'estacion__llave')

            operadores_list = []
            for op in operadores:
                operadores_list.append({
                    "id": op.user.id,
                    "id_operador": op.id,
                    "tipo_operador": op.tipo_operador,
                    "ruta": op.ruta.nombre if op.ruta else None,
                    "nro_estacion": op.estacion.llave.nro_estacion if op.estacion and op.estacion.llave else 0,
                    "username": op.user.username,
                    "email": op.user.email
                })

            data['user']['coordinador'] = {
                **coord_data,
                "cantidad_operadores": operadores.count()
            }
            data['user']['operadores_asignados'] = operadores_list
            data['user']['operador'] = None
            return data

        # ====== 2. CASO OPERADOR (formato anterior) ======
        try:
            operador = Operador.objects.select_related("estacion", "ruta").get(user=user)
            id_estacion = operador.estacion.id if operador.estacion else 0
            nro_estacion = operador.estacion.llave.nro_estacion if operador.estacion and operador.estacion.llave else 0
            ruta_data = {"id": operador.ruta.id, "nombre": str(operador.ruta)} if operador.ruta else None

            data['user']['operador'] = {
                "id_operador": operador.id,
                "ruta": ruta_data,
                "id_estacion": id_estacion,
                "nro_estacion": nro_estacion,
                "tipo_operador": operador.tipo_operador,
            }
        except Operador.DoesNotExist:
            data['user']['operador'] = None

        # ====== 3. OTROS ROLES (Soporte, Logistico, AsistenteMegacentro) ======
        for rol, modelo in (
            ('Soporte', Soporte),
            ('Logistico', Logistico),
            ('AsistenteMegacentro', AsistenteMegacentro),
        ):
            if user.groups.filter(name=rol).exists():
                data['user'][rol.lower()] = self._datos_personales(modelo, user)
                break
        else:
            # si no entró a ninguno, ponemos None
            data['user']['soporte'] = None
            data['user']['logistico'] = None
            data['user']['asistentemegacentro'] = None

        data['user']['coordinador'] = None
        data['user']['operadores_asignados'] = []
        return data

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'groups']
    
class LlaveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Llave
        fields = '__all__'

class RutaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ruta
        fields = '__all__'

class EstacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Estacion
        fields = '__all__'

class MovimientosEstacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovimientosEstacion
        fields = '__all__'     

class CoordinadorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coordinador
        fields = '__all__'

class OperadorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Operador
        fields = '__all__'

class ReporteDiarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReporteDiario
        fields = '__all__'

class RegistroDespliegueSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegistroDespliegue
        fields = '__all__'

class ListarOperadoresSerializer(serializers.ModelSerializer):
    nombre = serializers.CharField(source = 'operador.nombre', read_only=True)
    apellido_paterno = serializers.CharField(source = 'operador.apellido_paterno', read_only = True)
    apellido_materno = serializers.CharField(source = 'operador.apellido_materno', read_only = True)

    class Meta:
        model = RegistroDespliegue
        fields = ['nombre', 'apellido_paterno', 'apellido_materno']

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = '__all__'

class CentroEmpadronamientoSerializer(serializers.ModelSerializer):
    class Meta:
        model= CentroEmpadronamiento
        fields = '__all__'

class UbicacionesOperadorSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='operador.user', read_only=True)
    class Meta:
        model  = UbicacionesOperador
        fields = ['id','latitud','longitud','fecha','operador','user']
class UltimoRegistroDespliegueSerializer(serializers.ModelSerializer):
    """Serializer para devolver el último registro de despliegue de un operador."""
    class Meta:
        model  = RegistroDespliegue
        fields = '__all__'
class PuntoEmpadronamientoSerializer(serializers.ModelSerializer):
    """Listar: id, provincia, punto_de_empadronamiento"""
    class Meta:
        model  = CentroEmpadronamiento
        fields = ['id', 'provincia', 'punto_de_empadronamiento']

class ListarEstacionesLlavesSerializer(serializers.ModelSerializer):
    id_llave = serializers.SerializerMethodField()
    nro_estacion = serializers.SerializerMethodField()
    contador_r = serializers.SerializerMethodField()
    contador_c = serializers.SerializerMethodField()

    class Meta:
        model = Estacion
        fields = ['id', 'codigo_equipo', 'tipo_estacion', 'id_llave', 'nro_estacion', 'contador_r', 'contador_c']
    
    def get_id_llave(self, obj):
        return obj.llave.id if obj.llave else "Sin llave asignada"
    
    def get_nro_estacion(self, obj):
        return obj.llave.nro_estacion if obj.llave else 0
    
    def get_contador_r(self, obj):
        return obj.llave.contador_r if obj.llave else 0
    
    def get_contador_c(self, obj):
        return obj.llave.contador_c if obj.llave else 0

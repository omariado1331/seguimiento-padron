from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import (
    Llave, Ruta, Estacion, 
    MovimientosEstacion, Coordinador, Operador,
    ReporteDiario, RegistroDespliegue, Item)

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['username'] = user.username
        if user.groups.exists():
            token['group'] = user.groups.first().name
        else:
            token['group'] = None
        
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        user = self.user

        data['user'] = {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'groups': [g.name for g in user.groups.all()],
        }

        # Operador
        try:
            operador = Operador.objects.select_related("estacion", "ruta").get(user=user)
            if operador.estacion:
                id_estacion = operador.estacion.id
                nro_estacion = operador.estacion.nro_estacion
            else:
                id_estacion = 0
                nro_estacion = 0

            # ✅ Corregido: convertir 'ruta' a un dict simple
            ruta_data = None
            if operador.ruta:
                ruta_data = {
                    "id": operador.ruta.id,
                    "nombre": str(operador.ruta),
                }

            data["user"]['operador'] = {
                "id_operador": operador.id,
                "ruta": ruta_data,
                "id_estacion": id_estacion,
                "nro_estacion": nro_estacion,
                "tipo_operador": operador.tipo_operador,
            }
        except Operador.DoesNotExist:
            data["user"]["operador"] = None

        # Coordinador
        try:
            coordinador = Coordinador.objects.select_related("ruta").get(user=user)

            # ✅ Corregido: convertir 'ruta' a un dict simple
            ruta_data = None
            if coordinador.ruta:
                ruta_data = {
                    "id": coordinador.ruta.id,
                    "nombre": str(coordinador.ruta),
                }

            data["user"]["coordinador"] = {
                "id_coordinador": coordinador.id,
                "ruta": ruta_data,
            }
        except Coordinador.DoesNotExist:
            data["user"]["coordinador"] = None

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

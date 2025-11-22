from django.contrib.auth.models import User
from rest_framework import viewsets, generics
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenObtainPairSerializer
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .models import RegistroDespliegue
from .serializers import UltimoRegistroDespliegueSerializer
from simple_history.utils import update_change_reasonX
from .models import (
    Llave, Ruta, Estacion, 
    MovimientosEstacion, Coordinador, Operador,
    ReporteDiario, RegistroDespliegue, Item, CentroEmpadronamiento,
    UbicacionesOperador
)
from simple_history.utils import update_change_reason
from .serializers import (
    LlaveSerializer, RutaSerializer,
    EstacionSerializer, MovimientosEstacionSerializer, 
    CoordinadorSerializer, OperadorSerializer,
    ReporteDiarioSerializer, RegistroDespliegueSerializer, 
    UserSerializer, ListarOperadoresSerializer, ItemSerializer, 
    CentroEmpadronamientoSerializer, UbicacionesOperadorSerializer, 
    PuntoEmpadronamientoSerializer, ListarEstacionesLlavesSerializer
)

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class LlaveViewSet(viewsets.ModelViewSet):
    queryset = Llave.objects.all()
    serializer_class = LlaveSerializer

class RutaViewSet(viewsets.ModelViewSet):
    queryset = Ruta.objects.all()
    serializer_class = RutaSerializer

class EstacionViewSet(viewsets.ModelViewSet):
    queryset = Estacion.objects.all()
    serializer_class = EstacionSerializer

    # Registro de usuario y motivo para modificar desde API
    def perform_update(self, serializer):
        obj = serializer.save(history_user=self.request.user)
        update_change_reason(obj, "Modificado desde Panel")


class MovimientosEstacionViewSet(viewsets.ModelViewSet):
    queryset = MovimientosEstacion.objects.all()
    serializer_class = MovimientosEstacionSerializer

class CoordinadorViewSet(viewsets.ModelViewSet):
    queryset = Coordinador.objects.all()
    serializer_class = CoordinadorSerializer

class OperadorViewSet(viewsets.ModelViewSet):
    queryset = Operador.objects.all()
    serializer_class = OperadorSerializer

class ReporteDiarioViewSet(viewsets.ModelViewSet):
    queryset = ReporteDiario.objects.all()
    serializer_class = ReporteDiarioSerializer

class RegistroDespliegueViewSet(viewsets.ModelViewSet):
    queryset = RegistroDespliegue.objects.all()
    serializer_class = RegistroDespliegueSerializer

class ListarOperadoresListView(generics.ListAPIView):
    queryset = RegistroDespliegue.objects.select_related('operador').all()
    serializer_class = ListarOperadoresSerializer

class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

class CentroEmpadronamientoViewSet(viewsets.ModelViewSet):
    queryset = CentroEmpadronamiento.objects.all()
    serializer_class = CentroEmpadronamientoSerializer

class UbicacionesOperadorViewSet(viewsets.ModelViewSet):
    queryset = UbicacionesOperador.objects.all()
    serializer_class = UbicacionesOperadorSerializer
class UltimoRegistroDespliegueView(generics.RetrieveAPIView):
    """
    GET /api/ultimo-registro-despliegue/<id_operador>/
    Devuelve el último RegistroDespliegue del operador indicado.
    """
    serializer_class = UltimoRegistroDespliegueSerializer

    def get_object(self):
        id_operador = self.kwargs['id_operador']
        try:
            # último por fecha/hora descendente
            return RegistroDespliegue.objects.filter(
                operador_id=id_operador
            ).latest('fecha_hora')
        except RegistroDespliegue.DoesNotExist:
            # puedes lanzar 404 o devolver un payload vacío
            from django.http import Http404
            raise Http404("El operador no tiene registros de despliegue.")
        
class ListarPuntosEmpadronamientoView(generics.ListAPIView):
    queryset           = CentroEmpadronamiento.objects.all()
    serializer_class   = PuntoEmpadronamientoSerializer
    pagination_class   = None

class ListasEstacionesLlavesView(generics.ListAPIView):
    queryset = Estacion.objects.select_related('llave').all()
    serializer_class = ListarEstacionesLlavesSerializer

class LlavesSinAsignarView(APIView):
    def get(self, request):
        llaves = Llave.objects.filter(estacion__isnull=True)
        serializer = LlaveSerializer(llaves, many=True)
        return Response(serializer.data)

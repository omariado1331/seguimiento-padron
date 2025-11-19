from django.contrib.auth.models import User
from rest_framework import viewsets, generics
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenObtainPairSerializer
from .models import (
    Llave, Ruta, Estacion, 
    MovimientosEstacion, Coordinador, Operador,
    ReporteDiario, RegistroDespliegue, Item, CentroEmpadronamiento,
    UbicacionesOperador
)
from .serializers import (
    LlaveSerializer, RutaSerializer,
    EstacionSerializer, MovimientosEstacionSerializer, 
    CoordinadorSerializer, OperadorSerializer,
    ReporteDiarioSerializer, RegistroDespliegueSerializer, 
    UserSerializer, ListarOperadoresSerializer, ItemSerializer, 
    CentroEmpadronamientoSerializer, UbicacionesOperadorSerializer
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

from django.contrib.auth.models import User
from rest_framework import viewsets, generics
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenObtainPairSerializer
#from rest_framework import generics, status
from rest_framework.response import Response
#from rest_framework.decorators import action
#from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models import RegistroDespliegue
from .serializers import UltimoRegistroDespliegueSerializer
from simple_history.utils import update_change_reason
from .models import (
    Llave, Ruta, Estacion, 
    MovimientosEstacion, Coordinador, Operador,
    ReporteDiario, RegistroDespliegue, Item, CentroEmpadronamiento,
    UbicacionesOperador
)
from simple_history.utils import update_change_reason
#from reportlab.pdfgen import canvas
#from reportlab.lib.utils import ImageReader
#from reportlab.lib.pagesizes import landscape, A5
#import qrcode
#from io import BytesIO
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
    queryset = Estacion.objects.all().order_by('codigo_equipo')
    serializer_class = EstacionSerializer

    # Registro de usuario y motivo para modificar desde API
    def perform_update(self, serializer):
        user = self.request.user if self.request.user.is_authenticated else None
        obj = serializer.save(_history_user=user)
        update_change_reason(obj, "Modificado desde Panel")
    
    # @action(detail=True, methods=["get"])
    # def ticket(self, request, pk=None):
    #     estacion = self.get_object()
    #     llave = estacion.llave
    #     codigo_equipo = estacion.codigo_equipo
    #     buffer = BytesIO()
    #     pdf = canvas.Canvas(buffer, pagesize=landscape(A5))

    #     tickets = [
    #         (20, 210),
    #         (220, 210),
    #         (20, 20),
    #         (220, 20),
    #     ]

    #     for x,y in tickets:
    #         self.draw_ticket(pdf, llave, codigo_equipo, x, y)

    #     pdf.showPage()
        
    #     pdf.save()
    #     buffer.seek(0)

    #     return HttpResponse(buffer.getvalue(), content_type='application/pdf')
    
    # def draw_ticket(self, pdf, llave, codigo_equipo, x, y):
    #     #dimensiones del ticket
    #     width = 180
    #     height = 100

    #     #  dibujar borde del ticket
    #     pdf.setLineWidth(1)
    #     pdf.rect(x, y, width, height)

    #      # --- Logos ---
    #     logo_left = ImageReader("operaciones/static/img/oep.png")
    #     logo_right = ImageReader("operaciones/static/img/sereci.png")
        
    #     pdf.drawImage(logo_left, x + 5, y + height - 40, width=35, height=35, preserveAspectRatio=True)
    #     pdf.drawImage(logo_right, x + width - 40, y + height - 40, width=35, height=35, preserveAspectRatio=True)

    #     # --- Título centrado ---
    #     pdf.setFont("Helvetica-Bold", 6)
    #     pdf.drawCentredString(x + width/2, y + height - 20, "TRIBUNAL SUPREMO ELECTORAL")
    #     pdf.setFont("Helvetica", 5)
    #     pdf.drawCentredString(x + width/2, y + height - 28, "SERVICIO DE REGISTRO CIVICO - LA PAZ")
    #     pdf.drawCentredString(x + width/2, y + height - 33, "EMPADRONAMIENTO BIOMETRICO MASIVO")
    #     pdf.drawCentredString(x + width/2, y + height - 38, "ELECCION DE AUTORIDADES DEPARTAMENTALES, REGIONALES Y MUNICIPALES")
    #     pdf.drawCentredString(x + width/2, y + height - 43, "SUBNACIONALES 2026")

    #     # --- Número de estación ---
    #     pdf.setFont("Helvetica-Bold", 32)
    #     pdf.drawCentredString(x + width/2, y + height/2 -10 , str(llave.nro_estacion))

    #     # --- Contadores ---
    #     pdf.setFont("Helvetica-Bold", 12)
    #     pdf.drawString(x , y - 10 , f"R: {llave.contador_r}    C: {llave.contador_c}")

    #     # --- QR ---
    #     qrData = f"{llave.nro_estacion}|R:{llave.contador_r}|C:{llave.contador_c}|{codigo_equipo}"
    #     qr = qrcode.make(qrData)
    #     qr_io = BytesIO()

    #     qr.save(qr_io, format="PNG")
    #     qr_io.seek(0)
    #     qr_image = ImageReader(qr_io)
    #     pdf.drawImage(qr_image, x+100, y, width=50, height=50)


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
    serializer_class = ListarEstacionesLlavesSerializer
    def get_queryset(self):
        return( 
            Estacion.objects
            .select_related('llave')
            .filter(llave__isnull=False)
            .order_by('codigo_equipo')
        )

class LlavesSinAsignarView(APIView):
    def get(self, request):
        llaves = Llave.objects.filter(estacion__isnull=True).order_by('nro_estacion')
        serializer = LlaveSerializer(llaves, many=True)
        return Response(serializer.data)
    
class OperadoresSinEstacionAsignadaView(APIView):
    def get(self, request):
        operadores = Operador.objects.filter(estacion__isnull=True)
        serializer = OperadorSerializer(operadores, many=True)
        return Response(serializer.data)

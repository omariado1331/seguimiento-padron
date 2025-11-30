from django.contrib.auth.models import User
from rest_framework import viewsets, generics
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenObtainPairSerializer
#from rest_framework import generics, status
from rest_framework.response import Response
from django.db.models import Prefetch, OuterRef, Subquery
from django.db.models import Max
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
        llaves = (
            Llave.objects
            .filter(estacion__isnull=True)
            .exclude(nro_estacion__range=(10450, 10474))
            .order_by('nro_estacion'))
        serializer = LlaveSerializer(llaves, many=True)
        return Response(serializer.data)
    
class OperadoresSinEstacionAsignadaView(APIView):
    def get(self, request):
        operadores = Operador.objects.filter(estacion__isnull=True)
        serializer = OperadorSerializer(operadores, many=True)
        return Response(serializer.data)

class EstacionesCambioFaseConLlaveViewSet(APIView):
    def get(self, request):
        HistoricalEstacion = Estacion.history.model
        
        # Primero obtener solo los registros más recientes de cada estación
        estaciones_ids = Estacion.objects.values_list('id', flat=True)
        
        resultados_finales = []
        
        for estacion_id in estaciones_ids:
            # Obtener el registro histórico más reciente de esta estación
            historico_reciente = HistoricalEstacion.objects.filter(
                id=estacion_id
            ).select_related(
                'history_user',
                'llave'
            ).order_by('-history_date').first()
            
            if not historico_reciente:
                continue
                
            # Obtener el registro anterior para comparar
            registro_anterior = historico_reciente.prev_record
            if not registro_anterior:
                continue
            
            # Comparar los dos registros
            diff = historico_reciente.diff_against(registro_anterior)
            
            # Verificar si hay cambios en fase Y llave
            cambios_fase = [c for c in diff.changes if c.field == 'fase']
            cambios_llave = [c for c in diff.changes if c.field == 'llave']
            
            if cambios_fase and cambios_llave and historico_reciente.llave:
                cambio_fase = cambios_fase[0]
                cambio_llave = cambios_llave[0]
                
                registro = {
                    "codigo_equipo": historico_reciente.codigo_equipo,
                    "modelo": historico_reciente.modelo,
                    "tipo_estacion": historico_reciente.tipo_estacion,
                    "llave": {
                        "nro_estacion": historico_reciente.llave.nro_estacion,
                        "contador_c": historico_reciente.llave.contador_c,
                        "contador_r": historico_reciente.llave.contador_r,
                    },
                    "username": historico_reciente.history_user.username if historico_reciente.history_user else None,
                    "fecha_modificacion": historico_reciente.history_date,
                    "motivo_cambio": historico_reciente.history_change_reason,
                    "cambios": {
                        "fase_anterior": cambio_fase.old,
                        "fase_nueva": cambio_fase.new,
                        "llave_anterior": str(cambio_llave.old),
                        "llave_nueva": str(cambio_llave.new)
                    }
                }
                
                resultados_finales.append(registro)
        
        return Response({
            "success": True,
            "total_registros": len(resultados_finales),
            "data": resultados_finales
        })

class HistorialMasterizacionView(APIView):
    def get(self, request):
        HistoricalEstacion = Estacion.history.model
        
        # Subquery para obtener el histórico más reciente de cada estación
        latest_historical = HistoricalEstacion.objects.filter(
            id=OuterRef('id')
        ).order_by('-history_date')
        
        # Obtener estaciones con su histórico más reciente
        estaciones_con_historico = Estacion.objects.annotate(
            latest_history_date=Subquery(latest_historical.values('history_date')[:1])
        ).filter(
            latest_history_date__isnull=False
        )
        
        resultado = []
        
        for estacion in estaciones_con_historico:
            # Obtener el registro histórico más reciente
            historico_reciente = HistoricalEstacion.objects.filter(
                id=estacion.id,
                history_date=estacion.latest_history_date
            ).select_related('history_user', 'llave').first()
            
            if not historico_reciente:
                continue
                
            registro_anterior = historico_reciente.prev_record
            if not registro_anterior:
                continue
            
            diff = historico_reciente.diff_against(registro_anterior)
            
            cambios_fase = [c for c in diff.changes if c.field == 'fase']
            cambios_llave = [c for c in diff.changes if c.field == 'llave']
            
            if cambios_fase and cambios_llave and historico_reciente.llave:
                cambio_fase = cambios_fase[0]
                cambio_llave = cambios_llave[0]
                
                registro = {
                    "codigo_equipo": historico_reciente.codigo_equipo,
                    "modelo": historico_reciente.modelo,
                    "tipo_estacion": historico_reciente.tipo_estacion,
                    "fase": historico_reciente.fase,
                    "llave": {
                        "nro_estacion": historico_reciente.llave.nro_estacion,
                        "contador_c": historico_reciente.llave.contador_c,
                        "contador_r": historico_reciente.llave.contador_r,
                    },
                    "username": historico_reciente.history_user.username if historico_reciente.history_user else None,
                    "fecha_modificacion": historico_reciente.history_date,
                    "motivo_cambio": historico_reciente.history_change_reason,
                    "cambios": {
                        "fase_anterior": cambio_fase.old,
                        "fase_nueva": cambio_fase.new,
                        "llave_anterior": str(cambio_llave.old),
                        "llave_nueva": str(cambio_llave.new)
                    }
                }
                
                resultado.append(registro)
        
        return Response({
            "success": True,
            "total_registros": len(resultado),
            "data": resultado
        })

class HistorialMasterizacionViewSet(APIView):
    def get(self, request):
        HistoricalEstacion = Estacion.history.model
        
        # 1. Subquery para obtener el registro histórico más reciente de cada estación
        latest_history_subquery = HistoricalEstacion.objects.filter(
            id=OuterRef('id')
        ).order_by('-history_date').values('history_id')[:1]
        
        # 2. Subquery para obtener la fecha del histórico más reciente
        latest_history_date_subquery = HistoricalEstacion.objects.filter(
            id=OuterRef('id')
        ).order_by('-history_date').values('history_date')[:1]
        
        # 3. Subquery para obtener el registro anterior al más reciente
        second_latest_history_subquery = HistoricalEstacion.objects.filter(
            id=OuterRef('id'),
            history_date__lt=Subquery(latest_history_date_subquery)
        ).order_by('-history_date').values('history_id')[:1]
        
        # 4. Consulta principal con todas las relaciones
        estaciones = Estacion.objects.filter(
            llave__isnull=False  # Solo estaciones que tienen llave
        ).annotate(
            latest_history_id=Subquery(latest_history_subquery),
            second_latest_history_id=Subquery(second_latest_history_subquery)
        ).filter(
            latest_history_id__isnull=False,
            second_latest_history_id__isnull=False
        ).select_related('llave')
        
        # 5. Cargar todos los históricos necesarios en memoria
        historical_ids = []
        for estacion in estaciones:
            historical_ids.append(estacion.latest_history_id)
            historical_ids.append(estacion.second_latest_history_id)
        
        # Cargar todos los históricos en un solo query
        historicos_dict = {
            h.history_id: h for h in HistoricalEstacion.objects.filter(
                history_id__in=historical_ids
            ).select_related('history_user', 'llave')
        }
        
        resultado = []
        
        for estacion in estaciones:
            historico_reciente = historicos_dict.get(estacion.latest_history_id)
            historico_anterior = historicos_dict.get(estacion.second_latest_history_id)
            
            if not historico_reciente or not historico_anterior:
                continue
            
            # Comparar los registros
            diff = historico_reciente.diff_against(historico_anterior)
            
            cambios_fase = [c for c in diff.changes if c.field == 'fase']
            cambios_llave = [c for c in diff.changes if c.field == 'llave']
            
            if cambios_fase and cambios_llave:
                cambio_fase = cambios_fase[0]
                cambio_llave = cambios_llave[0]
                
                registro = {
                    "codigo_equipo": estacion.codigo_equipo,
                    "modelo": estacion.modelo,
                    "tipo_estacion": estacion.tipo_estacion,
                    "llave": {
                        "nro_estacion": estacion.llave.nro_estacion,
                        "contador_c": estacion.llave.contador_c,
                        "contador_r": estacion.llave.contador_r,
                    },
                    "username": historico_reciente.history_user.username if historico_reciente.history_user else None,
                    "fecha_modificacion": historico_reciente.history_date,
                    "motivo_cambio": historico_reciente.history_change_reason,
                    "cambios": {
                        "fase_anterior": cambio_fase.old,
                        "fase_nueva": cambio_fase.new,
                        "llave_anterior": str(cambio_llave.old),
                        "llave_nueva": str(cambio_llave.new)
                    }
                }
                
                resultado.append(registro)
        
        return Response({
            "success": True,
            "total_registros": len(resultado),
            "data": resultado
        })
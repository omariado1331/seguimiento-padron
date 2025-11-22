from django.urls import path, include
from .views import CustomTokenObtainPairView
from rest_framework import routers
from rest_framework_simplejwt.views import TokenRefreshView
from .api_views import UltimoRegistroDespliegueView 
from . import views
from .api_views import (
    LlaveViewSet, RutaViewSet, 
    EstacionViewSet, MovimientosEstacionViewSet, CoordinadorViewSet, 
    OperadorViewSet, ReporteDiarioViewSet, RegistroDespliegueViewSet,
    UserViewSet, ListarOperadoresListView, ItemViewSet, 
    CentroEmpadronamientoViewSet, UbicacionesOperadorViewSet,
    ListarPuntosEmpadronamientoView, ListasEstacionesLlavesView,
    LlavesSinAsignarView
)
from . import views

from .views import mapa_dashboard
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'llaves', LlaveViewSet)
router.register(r'rutas', RutaViewSet)
router.register(r'estaciones', EstacionViewSet)
router.register(r'movimientos-estacion', MovimientosEstacionViewSet)
router.register(r'coordinadores', CoordinadorViewSet)
router.register(r'operadores', OperadorViewSet)
router.register(r'reportesdiarios', ReporteDiarioViewSet)
router.register(r'registrosdespliegue', RegistroDespliegueViewSet)
router.register(r'items', ItemViewSet)
router.register(r'centros-empadronamiento', CentroEmpadronamientoViewSet)
router.register(r'ubicaciones-operador', UbicacionesOperadorViewSet)

urlpatterns = [
    #path('', views.index, name='index'),
    #path para apis
    path('api/', include(router.urls)),
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('listar-operadores/', ListarOperadoresListView.as_view(), name='listado-operadores'),
    path('api/ultimo-registro-despliegue/<int:id_operador>/',
         UltimoRegistroDespliegueView.as_view(),
         name='ultimo-registro-despliegue'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('panel/<str:rol>/', views.panel_view, name='panel'),
    path('qr/scan/', views.qr_scan, name='qr_scan'),
    path('api/listar-puntos-empadronamiento/',
         ListarPuntosEmpadronamientoView.as_view(),
         name='listar-puntos-empadronamiento'),
    path('mapa/', mapa_dashboard, name='mapa_dashboard'), 
    path('lista-estaciones-llaves/', ListasEstacionesLlavesView.as_view(), name='estaciones-llaves'),
    path('llaves-sin-asignar/', LlavesSinAsignarView.as_view(), name='llaves_sin_asignar'),
    path('soporte/', views.soporte_view, name='soporte'),
]

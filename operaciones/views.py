from django.shortcuts import render
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenObtainPairSerializer
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Estacion

# Create your views here.

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


# ---------- LOGIN ----------
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # 1 sólo grupo por usuario (simplificación)
            grupo = user.groups.first()
            if not grupo:
                return render(request, 'operaciones/login.html',
                              {'error': 'Usuario sin grupo asignado'})
            return redirect('panel', rol=grupo.name)
        return render(request, 'operaciones/login.html',
                      {'error': 'Credenciales inválidas'})
    return render(request, 'operaciones/login.html')

# ---------- PANEL SEGÚN ROL ----------
@login_required
def panel_view(request, rol):
    # comprobamos que el rol coincida con el grupo real
    if not request.user.groups.filter(name=rol).exists():
        return redirect('login')
    return render(request, 'operaciones/panel.html', {'rol': rol})

# ---------- LECTURA QR (AJAX) ----------
@login_required
def qr_escanear(request):
    if request.method != 'POST':
        return JsonResponse({'ok': False, 'msg': 'Método no permitido'})

    codigo = request.POST.get('codigo', '').strip()
    if not codigo:
        return JsonResponse({'ok': False, 'msg': 'Código vacío'})

    estacion = get_object_or_404(Estacion, codigo_equipo=codigo)

    rol = request.user.groups.first().name
    nueva_fase = None
    campos_bool = {}          # campos adicionales a actualizar

    # ---- regla de negocio ----
    if rol == 'SoporteInventarios':
        if estacion.fase != 'Recepcionado':
            return JsonResponse({'ok': False, 'msg': 'Equipo no está en Recepcionado'})
        nueva_fase = 'En Revision'
        campos_bool['recepcionado'] = True

    elif rol == 'SoporteMantenimiento':
        if estacion.fase != 'En Revision':
            return JsonResponse({'ok': False, 'msg': 'Equipo no está En Revision'})
        # aquí podrías validar que vengan todos los campos POST
        # por simplicidad los leemos y grabamos
        for campo in ['estado_computadora', 'estado_monitor', 'estado_escaner',
                      'estado_impresora', 'estado_pad_firmas', 'estado_camara',
                      'estado_decadactilar', 'estado_hub_usb',
                      'estado_estabilizador_energia', 'estado_pila_madre',
                      'estado_memorias_ram', 'estado_disco_duro',
                      'cable_extensor', 'tripode', 'banner',
                      'adaptador_3a2', 'monitor_pc', 'testeo_pila',
                      'asignada', 'observacion']:
            if campo in request.POST:
                setattr(estacion, campo, request.POST[campo])
        nueva_fase = 'Revisado funcional'
        campos_bool['revisado'] = True

    elif rol == 'SoporteClonacion':
        if estacion.fase != 'Revisado funcional':
            return JsonResponse({'ok': False, 'msg': 'Equipo no está Revisado funcional'})
        nueva_fase = 'En Masterizacion'
        campos_bool['clonado'] = True

    elif rol == 'SoporteMasterizacion':
        if estacion.fase == 'En Masterizacion':
            nueva_fase = 'Masterizado'
            campos_bool['masterizado'] = True
        elif estacion.fase == 'Revisado funcional':
            nueva_fase = 'En Masterizacion'
        else:
            return JsonResponse({'ok': False, 'msg': 'Equipo no puede pasar a Masterización'})

    elif rol == 'SoporteEntrega':
        if estacion.fase != 'Masterizado':
            return JsonResponse({'ok': False, 'msg': 'Equipo no está Masterizado'})
        nro = request.POST.get('nro_estacion')
        if not nro or not nro.isdigit():
            return JsonResponse({'ok': False, 'msg': 'Debe enviar nro_estacion numérico'})
        estacion.nro_estacion = int(nro)
        nueva_fase = 'Asignado'
        campos_bool['asignado'] = True

    else:
        return JsonResponse({'ok': False, 'msg': 'Rol sin acceso a cambio de fase'})

    # --- aplicar cambios ---
    if nueva_fase:
        estacion.fase = nueva_fase
    for k, v in campos_bool.items():
        setattr(estacion, k, v)
    estacion.save()

    return JsonResponse({'ok': True, 'nueva_fase': estacion.fase})
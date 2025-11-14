from django.shortcuts import render
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenObtainPairSerializer
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Estacion
from django.contrib.auth import authenticate, login, logout
from django.contrib.contenttypes.models import ContentType
from django.contrib.admin.models import LogEntry, ADDITION, CHANGE
# Create your views here.

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


# ---------- LOGIN / LOGOUT ----------
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            grupo = user.groups.first()
            if not grupo:
                return render(request, 'operaciones/login.html',
                              {'error': 'Usuario sin grupo asignado'})
            return redirect('panel', rol=grupo.name)
        return render(request, 'operaciones/login.html',
                      {'error': 'Credenciales inválidas'})
    return render(request, 'operaciones/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

# ---------- PANEL ----------
@login_required
def panel_view(request, rol):
    if not request.user.groups.filter(name=rol).exists():
        return redirect('login')
    # Pasamos la lista de fases para pintar los badges
    fases = [c[0] for c in Estacion.FASES_CHOICES]
    return render(request, 'operaciones/panel.html', {'rol': rol, 'fases': fases})

# ---------- QR SCAN (AJAX) ----------
@login_required
def qr_scan(request):
    if request.method != 'POST':
        return JsonResponse({'ok': False, 'msg': 'Método no permitido'})

    data = json.loads(request.body or '{}')
    codigo = (data.get('codigo') or '').strip()
    accion = data.get('accion', '')          # revision / mantenimiento / clonacion / masterizacion / entrega
    nro_estacion = data.get('nro_estacion')

    # ---- Inventarios: crea si no existe ----
    if request.user.groups.first().name == 'SoporteInventarios':
        estacion, created = Estacion.objects.get_or_create(
            codigo_equipo=codigo,
            defaults={'fase': 'Recepcionado', 'recepcionado': True}
        )
        if created:
            log(request.user, estacion, 'Creó estación', ADDITION)
        return JsonResponse({'ok': True, 'nueva_fase': estacion.fase, 'created': created})

    # ---- Resto de roles: equipo debe existir ----
    try:
        estacion = Estacion.objects.get(codigo_equipo=codigo)
    except Estacion.DoesNotExist:
        return JsonResponse({'ok': False, 'msg': 'CÓDIGO NO REGISTRADO, COMUNÍQUESE CON TICs LA PAZ'})

    rol = request.user.groups.first().name
    nueva_fase = None
    campos_bool = {}

    # ---------- SoporteMantenimiento ----------
    if rol == 'SoporteMantenimiento':
        if accion == 'revision':
            if estacion.fase not in ('Recepcionado', 'Revisado funcional', 'En mantenimiento'):
                return JsonResponse({'ok': False, 'msg': 'No puede pasar a En Revisión desde esta fase'})
            nueva_fase = 'En Revision'
        elif accion == 'mantenimiento':
            nueva_fase = 'En mantenimiento'
        elif accion == 'finalizar':
            # cierra revisión o mantenimiento → Revisado funcional
            # aquí puedes pedir el checklist vía AJAX si quieres
            nueva_fase = 'Revisado funcional'
            campos_bool['revisado'] = True
        else:
            return JsonResponse({'ok': False, 'msg': 'Acción no válida'})

    # ---------- SoporteClonacion ----------
    elif rol == 'SoporteClonacion':
        if accion == 'clonacion':
            if estacion.fase != 'Revisado funcional':
                return JsonResponse({'ok': False, 'msg': 'Requisito: Revisado funcional'})
            nueva_fase = 'En Clonacion'
        elif accion == 'finalizar':
            if estacion.fase != 'En Clonacion':
                return JsonResponse({'ok': False, 'msg': 'El equipo no está En Clonación'})
            nueva_fase = 'Clonado'
            campos_bool['clonado'] = True
        else:
            return JsonResponse({'ok': False, 'msg': 'Acción no válida'})

    # ---------- SoporteMasterizacion ----------
    elif rol == 'SoporteMasterizacion':
        if accion == 'masterizacion':
            if estacion.fase != 'Clonado':
                return JsonResponse({'ok': False, 'msg': 'Requisito: Clonado'})
            nueva_fase = 'En Masterizacion'
        elif accion == 'finalizar':
            if estacion.fase != 'En Masterizacion':
                return JsonResponse({'ok': False, 'msg': 'El equipo no está En Masterización'})
            nueva_fase = 'Masterizado'
            campos_bool['masterizado'] = True
        else:
            return JsonResponse({'ok': False, 'msg': 'Acción no válida'})

    # ---------- SoporteEntrega ----------
    elif rol == 'SoporteEntrega':
        if estacion.fase != 'Masterizado':
            return JsonResponse({'ok': False, 'msg': 'Requisito: Masterizado'})
        if not nro_estacion or not str(nro_estacion).isdigit():
            return JsonResponse({'ok': False, 'msg': 'Debe ingresar un nro_estacion numérico'})
        estacion.nro_estacion = int(nro_estacion)
        nueva_fase = 'Asignado'
        campos_bool['asignado'] = True

    else:
        return JsonResponse({'ok': False, 'msg': 'Rol sin permisos'})

    # ----- aplicar -----
    if nueva_fase:
        estacion.fase = nueva_fase
    for k, v in campos_bool.items():
        setattr(estacion, k, v)
    estacion.save()
    log(request.user, estacion, f'Cambió fase a {nueva_fase}', CHANGE)
    return JsonResponse({'ok': True, 'nueva_fase': nueva_fase})

# ---------- Helper para dejar rastro en Admin ----------
def log(user, obj, message, flag=CHANGE):
    LogEntry.objects.log_action(
        user_id=user.pk,
        content_type_id=ContentType.objects.get_for_model(obj).pk,
        object_id=obj.pk,
        object_repr=str(obj),
        action_flag=flag,
        change_message=message
    )
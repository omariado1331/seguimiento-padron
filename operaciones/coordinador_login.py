from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response
from django.contrib.auth.models import User
from .models import Coordinador, Operador

class CoordinadorLoginView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        # obtenemos el token normal
        response = super().post(request, *args, **kwargs)
        user = User.objects.get(username=request.data['username'])

        # solo si es coordinador
        if not user.groups.filter(name='Coordinador').exists():
            return response   # devolvemos el token estándar

        coord = Coordinador.objects.get(user=user)
        operadores = Operador.objects.filter(
            coordinador=coord
        ).select_related('user', 'estacion', 'ruta')

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

        # sobre-escribimos el payload
        response.data['user'] = {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "groups": list(user.groups.values_list('name', flat=True)),
            "coordinador": {
                "id_coordinador": coord.id,
                "zona": "Norte",   # <-- podés cambiarlo por un campo real
                "cantidad_operadores": operadores.count()
            },
            "operadores_asignados": operadores_list,
            "operador": None
        }
        return response
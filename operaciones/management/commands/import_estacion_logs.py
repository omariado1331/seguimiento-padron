from django.core.management.base import BaseCommand
from django.contrib.admin.models import LogEntry
from django.contrib.contenttypes.models import ContentType
from django.db import transaction
from operaciones.models import Estacion

class Command(BaseCommand):
    help = "Importa logs del admin al historial de Estacion (simple-history)"

    def handle(self, *args, **kwargs):
        # Obtener logs del modelo Estacion
        ct = ContentType.objects.get_for_model(Estacion)
        # Filtrar logs por el content type de Estacion
        logs = LogEntry.objects.filter(content_type=ct).order_by("action_time")
        # Modelo de historial de Estacion
        HistoricalEstacion = Estacion.history.model

        if not logs.exists():
            self.stdout.write(self.style.WARNING("No hay logs para importar."))
            return

        total = logs.count()
        importados = 0
        omitidos = 0

        self.stdout.write(f"Procesando {total} logs...")

        for log in logs:
            # Obtener la instancia de Estacion correspondiente
            try:
                # El object_id en LogEntry es un string, convertir a int
                estacion = Estacion.objects.get(pk=log.object_id)
                # Si no existe, se omite
            except Estacion.DoesNotExist:
                omitidos += 1
                continue

            if estacion.history.filter(
                history_date=log.action_time,
                history_user_id=log.user_id
            ).exists():
                omitidos += 1
                continue

            with transaction.atomic():

                # Copiar todos los campos reales del modelo
                historial_data = {
                    field.name: getattr(estacion, field.name)
                    for field in Estacion._meta.fields
                }

                # Agregar datos del historial
                historial = HistoricalEstacion(
                    **historial_data,
                    history_date=log.action_time,
                    history_user=log.user,
                    history_change_reason=(
                        log.change_message or "Importado desde django_admin_log"
                    ),
                    history_type={
                        1: '+',
                        2: '~',
                        3: '-'
                    }.get(log.action_flag, '~')
                )

                historial.save()

            importados += 1
            self.stdout.write(f"  ✔ Importado log ID {log.id}")

        self.stdout.write(self.style.SUCCESS(f"\nImportación completada."))
        self.stdout.write(self.style.SUCCESS(f"Total procesados: {total}"))
        self.stdout.write(self.style.SUCCESS(f"Importados: {importados}"))
        self.stdout.write(self.style.WARNING(f"Omitidos: {omitidos}"))

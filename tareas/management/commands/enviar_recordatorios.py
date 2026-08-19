from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.utils import timezone
from tareas.models import Tarea


class Command(BaseCommand):
    help = 'Envía por email las tareas que vencen hoy o están atrasadas'

    def handle(self, *args, **options):
        hoy = timezone.localdate()
        por_vencer = Tarea.objects.exclude(estado='completada').filter(fecha_limite__lte=hoy)
        if not por_vencer:
            self.stdout.write(self.style.SUCCESS('No hay tareas por vencer 🎉'))
            return

        lineas = []
        for t in por_vencer:
            tipo = 'ATRASADA' if t.fecha_limite < hoy else 'VENCE HOY'
            lineas.append(f'- [{tipo}] {t.titulo} (Proyecto: {t.proyecto.nombre})')

        send_mail(
            subject='⏰ Recordatorio de tareas por vencer',
            message='Tienes tareas por vencer:\n\n' + '\n'.join(lineas),
            from_email='gestor@demo.com',
            recipient_list=['tucorreo@ejemplo.com'],
        )
        self.stdout.write(self.style.SUCCESS(f'Email enviado con {por_vencer.count()} tareas (revisa la consola).'))
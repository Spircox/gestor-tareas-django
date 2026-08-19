from datetime import timedelta
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.utils import timezone
from tareas.models import Proyecto, Tarea, Etiqueta, Subtarea


class Command(BaseCommand):
    help = 'Crea datos de ejemplo para probar todo'

    if Proyecto.objects.exists():
        self.stdout.write(self.style.WARNING('Ya existen proyectos, no se crearán datos de ejemplo'))
    
    def handle(self, *args, **options):
        usuario, _ = User.objects.get_or_create(username='demo')
        usuario.set_password('demo1234')
        usuario.save()

        # Rescata proyectos antiguos sin dueño
        Proyecto.objects.filter(usuario__isnull=True).update(usuario=usuario)

        urgente = Etiqueta.objects.get_or_create(nombre='Urgente', defaults={'color': '#dc3545'})[0]
        trabajo = Etiqueta.objects.get_or_create(nombre='Trabajo', defaults={'color': '#0d6efd'})[0]
        casa = Etiqueta.objects.get_or_create(nombre='Casa', defaults={'color': '#198754'})[0]
        estudio = Etiqueta.objects.get_or_create(nombre='Estudio', defaults={'color': '#6f42c1'})[0]
        hoy = timezone.localdate()

        p1 = Proyecto.objects.create(usuario=usuario, nombre='App Django', descripcion='Desarrollo de la app de prueba')
        p2 = Proyecto.objects.create(usuario=usuario, nombre='Mudanza', descripcion='Organización de la mudanza')

        t1 = Tarea.objects.create(proyecto=p1, titulo='Configurar modelos', estado='completada', orden=1)
        t2 = Tarea.objects.create(proyecto=p1, titulo='Diseñar tablero Kanban', estado='en_proceso', fecha_limite=hoy, orden=1)
        t2.etiquetas.add(trabajo, urgente)
        t3 = Tarea.objects.create(proyecto=p1, titulo='Desplegar en producción', fecha_limite=hoy + timedelta(days=3), orden=2)
        t3.etiquetas.add(trabajo)
        t4 = Tarea.objects.create(proyecto=p1, titulo='Escribir documentación', fecha_limite=hoy - timedelta(days=2), orden=3)
        t4.etiquetas.add(estudio)
        t5 = Tarea.objects.create(proyecto=p2, titulo='Empacar libros', estado='en_proceso', orden=1)
        t5.etiquetas.add(casa)
        t6 = Tarea.objects.create(proyecto=p2, titulo='Contratar camión', fecha_limite=hoy, orden=2)
        t6.etiquetas.add(casa, urgente)

        Subtarea.objects.get_or_create(tarea=t2, texto='HTML de columnas', defaults={'completada': True})
        Subtarea.objects.get_or_create(tarea=t2, texto='JavaScript drag & drop', defaults={'completada': True})
        Subtarea.objects.get_or_create(tarea=t2, texto='Endpoint AJAX')

        self.stdout.write(self.style.SUCCESS('Datos listos ✔  Entra con: demo / demo1234'))

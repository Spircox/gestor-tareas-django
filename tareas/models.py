from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User


class Proyecto(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='proyectos', null=True, blank=True)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    creado_el = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-creado_el']

    def __str__(self):
        return self.nombre

    def get_absolute_url(self):
        return reverse('tareas:proyecto_detalle', kwargs={'pk': self.pk})

    @property
    def progreso(self):
        total = self.tareas.count()
        if total == 0:
            return 0
        return round(self.tareas.filter(estado='completada').count() * 100 / total)


class Etiqueta(models.Model):
    nombre = models.CharField(max_length=30, unique=True)
    color = models.CharField(max_length=7, default='#6c757d')

    class Meta:
        ordering = ['nombre']

    def __str__(self):
        return self.nombre


class Tarea(models.Model):
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('en_proceso', 'En proceso'),
        ('completada', 'Completada'),
    ]

    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE, related_name='tareas')
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='pendiente')
    fecha_limite = models.DateField(null=True, blank=True)
    etiquetas = models.ManyToManyField(Etiqueta, blank=True, related_name='tareas')
    orden = models.IntegerField(default=0)
    creada_el = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['orden', '-creada_el']

    def __str__(self):
        return self.titulo

    @property
    def atrasada(self):
        return self.fecha_limite and self.estado != 'completada' and self.fecha_limite < timezone.localdate()

    @property
    def vence_hoy(self):
        return self.fecha_limite == timezone.localdate() and self.estado != 'completada'

    @property
    def progreso_subtareas(self):
        total = self.subtareas.count()
        if total == 0:
            return None
        return f"{self.subtareas.filter(completada=True).count()}/{total}"


class Subtarea(models.Model):
    tarea = models.ForeignKey(Tarea, on_delete=models.CASCADE, related_name='subtareas')
    texto = models.CharField(max_length=200)
    completada = models.BooleanField(default=False)

    def __str__(self):
        return self.texto
from django.contrib import admin
from .models import Proyecto, Tarea, Etiqueta, Subtarea


class TareaInline(admin.TabularInline):
    model = Tarea
    extra = 1


class SubtareaInline(admin.TabularInline):
    model = Subtarea
    extra = 1


@admin.register(Proyecto)
class ProyectoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'creado_el')
    inlines = [TareaInline]


@admin.register(Tarea)
class TareaAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'proyecto', 'estado', 'fecha_limite')
    list_filter = ('estado', 'proyecto', 'etiquetas')
    inlines = [SubtareaInline]


@admin.register(Etiqueta)
class EtiquetaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'color')
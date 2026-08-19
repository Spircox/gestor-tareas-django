from django.urls import path
from . import views

app_name = 'tareas'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('proyectos/', views.proyecto_lista, name='proyecto_lista'),
    path('proyectos/nuevo/', views.proyecto_crear, name='proyecto_crear'),
    path('proyectos/<int:pk>/', views.proyecto_detalle, name='proyecto_detalle'),
    path('proyectos/<int:pk>/editar/', views.proyecto_editar, name='proyecto_editar'),
    path('proyectos/<int:pk>/eliminar/', views.proyecto_eliminar, name='proyecto_eliminar'),
    path('proyectos/<int:proyecto_id>/tareas/nueva/', views.tarea_crear, name='tarea_crear'),
    path('tareas/<int:pk>/', views.tarea_detalle, name='tarea_detalle'),
    path('tareas/<int:pk>/editar/', views.tarea_editar, name='tarea_editar'),
    path('tareas/<int:pk>/mover/', views.tarea_mover, name='tarea_mover'),
    path('tareas/<int:pk>/eliminar/', views.tarea_eliminar, name='tarea_eliminar'),
    path('tareas/<int:pk>/subtarea/', views.subtarea_agregar, name='subtarea_agregar'),
    path('subtareas/<int:pk>/toggle/', views.subtarea_toggle, name='subtarea_toggle'),
    path('subtareas/<int:pk>/eliminar/', views.subtarea_eliminar, name='subtarea_eliminar'),
    path('buscar/', views.buscar, name='buscar'),
]
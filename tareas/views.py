from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Q, Count, Max
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.views.decorators.http import require_POST

from .forms import ProyectoForm, TareaForm, SubtareaForm
from .models import Etiqueta, Proyecto, Subtarea, Tarea


# ---------- CUENTAS ----------
def registro(request):
    if request.user.is_authenticated:
        return redirect('tareas:dashboard')
    form = UserCreationForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        usuario = form.save()
        login(request, usuario)
        messages.success(request, f'¡Bienvenido, {usuario.username}!')
        return redirect('tareas:dashboard')
    return render(request, 'registration/registro.html', {'form': form})


# ---------- DASHBOARD ----------
@login_required
def dashboard(request):
    tareas = Tarea.objects.filter(proyecto__usuario=request.user)
    datos = {
        'total_proyectos': Proyecto.objects.filter(usuario=request.user).count(),
        'total_tareas': tareas.count(),
        'completadas': tareas.filter(estado='completada').count(),
        'en_proceso': tareas.filter(estado='en_proceso').count(),
        'pendientes': tareas.filter(estado='pendiente').count(),
        'atrasadas': tareas.exclude(estado='completada').filter(fecha_limite__lt=timezone.localdate()).count(),
    }
    proyectos = Proyecto.objects.filter(usuario=request.user).annotate(
        total=Count('tareas'),
        hechas=Count('tareas', filter=Q(tareas__estado='completada')),
    )
    chart = {
        'labels': ['Pendientes', 'En proceso', 'Completadas'],
        'datos': [datos['pendientes'], datos['en_proceso'], datos['completadas']],
    }
    return render(request, 'tareas/dashboard.html', {'datos': datos, 'proyectos': proyectos, 'chart': chart})


# ---------- PROYECTOS ----------
@login_required
def proyecto_lista(request):
    return render(request, 'tareas/proyecto_lista.html',
                  {'proyectos': Proyecto.objects.filter(usuario=request.user)})


@login_required
def proyecto_detalle(request, pk):
    proyecto = get_object_or_404(Proyecto, pk=pk, usuario=request.user)
    columnas = [(estado, label, proyecto.tareas.filter(estado=estado)) for estado, label in Tarea.ESTADO_CHOICES]
    return render(request, 'tareas/proyecto_detalle.html', {'proyecto': proyecto, 'columnas': columnas})


@login_required
def proyecto_crear(request):
    if request.method == 'POST':
        form = ProyectoForm(request.POST)
        if form.is_valid():
            proyecto = form.save(commit=False)
            proyecto.usuario = request.user
            proyecto.save()
            messages.success(request, 'Proyecto creado correctamente.')
            return redirect('tareas:proyecto_lista')
    else:
        form = ProyectoForm()
    return render(request, 'tareas/proyecto_form.html', {'form': form, 'titulo': 'Nuevo Proyecto'})


@login_required
def proyecto_editar(request, pk):
    proyecto = get_object_or_404(Proyecto, pk=pk, usuario=request.user)
    form = ProyectoForm(request.POST or None, instance=proyecto)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Proyecto actualizado.')
        return redirect('tareas:proyecto_detalle', pk=proyecto.pk)
    return render(request, 'tareas/proyecto_form.html', {'form': form, 'titulo': 'Editar Proyecto'})


@login_required
def proyecto_eliminar(request, pk):
    proyecto = get_object_or_404(Proyecto, pk=pk, usuario=request.user)
    if request.method == 'POST':
        proyecto.delete()
        messages.success(request, 'Proyecto eliminado.')
        return redirect('tareas:proyecto_lista')
    return redirect('tareas:proyecto_detalle', pk=pk)


# ---------- TAREAS ----------
@login_required
def tarea_crear(request, proyecto_id):
    proyecto = get_object_or_404(Proyecto, pk=proyecto_id, usuario=request.user)
    if request.method == 'POST':
        form = TareaForm(request.POST)
        if form.is_valid():
            tarea = form.save(commit=False)
            tarea.proyecto = proyecto
            tarea.save()
            form.save_m2m()
            messages.success(request, 'Tarea añadida.')
            return redirect('tareas:proyecto_detalle', pk=proyecto.pk)
    else:
        form = TareaForm()
    return render(request, 'tareas/tarea_form.html', {'form': form, 'proyecto': proyecto, 'titulo': 'Nueva Tarea'})


@login_required
def tarea_detalle(request, pk):
    tarea = get_object_or_404(Tarea, pk=pk, proyecto__usuario=request.user)
    return render(request, 'tareas/tarea_detalle.html', {'tarea': tarea, 'form_sub': SubtareaForm()})


@login_required
def tarea_editar(request, pk):
    tarea = get_object_or_404(Tarea, pk=pk, proyecto__usuario=request.user)
    form = TareaForm(request.POST or None, instance=tarea)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Tarea actualizada.')
        return redirect('tareas:tarea_detalle', pk=tarea.pk)
    return render(request, 'tareas/tarea_form.html', {'form': form, 'proyecto': tarea.proyecto, 'titulo': 'Editar Tarea'})


@login_required
def tarea_eliminar(request, pk):
    tarea = get_object_or_404(Tarea, pk=pk, proyecto__usuario=request.user)
    proyecto_id = tarea.proyecto.pk
    if request.method == 'POST':
        tarea.delete()
        messages.success(request, 'Tarea eliminada.')
    return redirect('tareas:proyecto_detalle', pk=proyecto_id)


@login_required
@require_POST
def tarea_mover(request, pk):
    tarea = get_object_or_404(Tarea, pk=pk, proyecto__usuario=request.user)
    nuevo_estado = request.POST.get('estado')
    if nuevo_estado not in dict(Tarea.ESTADO_CHOICES):
        return JsonResponse({'error': 'Estado inválido'}, status=400)
    max_orden = Tarea.objects.filter(proyecto=tarea.proyecto, estado=nuevo_estado).aggregate(m=Max('orden'))['m'] or 0
    tarea.estado = nuevo_estado
    tarea.orden = max_orden + 1
    tarea.save()

    if request.POST.get('volver') == 'detalle':
        messages.success(request, f'Estado actualizado a "{tarea.get_estado_display()}".')
        return redirect('tareas:tarea_detalle', pk=tarea.pk)
    return JsonResponse({'ok': True})


# ---------- SUBTAREAS ----------
@login_required
@require_POST
def subtarea_agregar(request, pk):
    tarea = get_object_or_404(Tarea, pk=pk, proyecto__usuario=request.user)
    form = SubtareaForm(request.POST)
    if form.is_valid():
        sub = form.save(commit=False)
        sub.tarea = tarea
        sub.save()
    return redirect('tareas:tarea_detalle', pk=tarea.pk)


@login_required
@require_POST
def subtarea_toggle(request, pk):
    sub = get_object_or_404(Subtarea, pk=pk, tarea__proyecto__usuario=request.user)
    sub.completada = not sub.completada
    sub.save()
    return redirect('tareas:tarea_detalle', pk=sub.tarea.pk)


@login_required
@require_POST
def subtarea_eliminar(request, pk):
    sub = get_object_or_404(Subtarea, pk=pk, tarea__proyecto__usuario=request.user)
    tarea_id = sub.tarea.pk
    sub.delete()
    return redirect('tareas:tarea_detalle', pk=tarea_id)


# ---------- BUSCADOR ----------
@login_required
def buscar(request):
    q = request.GET.get('q', '').strip()
    estado = request.GET.get('estado', '')
    etiqueta = request.GET.get('etiqueta', '')

    tareas = Tarea.objects.filter(proyecto__usuario=request.user)
    if q:
        tareas = tareas.filter(Q(titulo__icontains=q) | Q(descripcion__icontains=q))
    if estado:
        tareas = tareas.filter(estado=estado)
    if etiqueta:
        tareas = tareas.filter(etiquetas__id=etiqueta)

    return render(request, 'tareas/buscar.html', {
        'tareas': tareas.distinct(), 'q': q, 'estado': estado, 'etiqueta': etiqueta,
        'estados': Tarea.ESTADO_CHOICES, 'etiquetas': Etiqueta.objects.all(),
    })
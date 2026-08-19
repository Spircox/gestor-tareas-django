from django.utils import timezone
from .models import Tarea


def avisos(request):
    if not request.user.is_authenticated:
        return {'avisos': [], 'num_avisos': 0}
    urgentes = Tarea.objects.filter(proyecto__usuario=request.user).exclude(estado='completada').filter(fecha_limite__lte=timezone.localdate())
    return {'avisos': urgentes, 'num_avisos': urgentes.count()}
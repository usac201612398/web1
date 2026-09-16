from django.shortcuts import render
from django.utils import timezone

from ..models import (
    Maquina,
    Ubicacion,
    centrodecosto,
    DistribucionMaquinas,
    ListaMantenimientos,
    Usuarios,
    SolicitarOperacion,
    MantenimientoRealizado,
)


# ==========================================================
# TABLERO PRINCIPAL
# ==========================================================

def index(request):

    hoy = timezone.localdate()


    # ======================================================
    # INDICADORES
    # ======================================================

    total_maquinas_activas = Maquina.objects.filter(
        status='Activa'
    ).count()


    solicitudes_activas = SolicitarOperacion.objects.filter(
        status='Activa'
    ).count()


    solicitudes_vencidas = SolicitarOperacion.objects.filter(
        status='Vencida'
    ).count()


    mantenimientos_realizados = MantenimientoRealizado.objects.filter(
        status='Atendido'
    ).count()


    # ======================================================
    # PROXIMOS MANTENIMIENTOS
    # ======================================================

    proximos_mantenimientos = (
        ListaMantenimientos.objects
        .select_related('maquina')
        .filter(
            status='Vigente',
            maquina__status='Activa'
        )
        .order_by('maquina__nombre', 'registro')[:5]
    )


    # ======================================================
    # SOLICITUDES RECIENTES
    # ======================================================

    solicitudes_recientes = (
        SolicitarOperacion.objects
        .select_related(
            'maquina',
            'ubicacion',
            'mantenimiento'
        )
        .exclude(
            status='Anulada'
        )
        .order_by('-created_at')[:5]
    )


    # ======================================================
    # CONTEXTO
    # ======================================================

    context = {

        'total_maquinas_activas':
            total_maquinas_activas,

        'solicitudes_activas':
            solicitudes_activas,

        'solicitudes_vencidas':
            solicitudes_vencidas,

        'mantenimientos_realizados':
            mantenimientos_realizados,

        'proximos_mantenimientos':
            proximos_mantenimientos,

        'solicitudes_recientes':
            solicitudes_recientes,

    }


    return render(
        request,
        'mantenimiento/tableros/tablero.html',
        context
    )
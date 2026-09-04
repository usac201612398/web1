import csv
from datetime import timedelta

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import (
    CreateView, DeleteView, DetailView, ListView, TemplateView, UpdateView,
)

from .forms import (
    ActividadForm, AreaForm, EvidenciaFormSet, MaquinaForm, ProgramaForm, ServicioForm,
)
from .models import Actividad, Area, Evidencia, Maquina, Programa, Servicio


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def programas_ordenados(qs=None):
    """Devuelve programas activos ordenados por urgencia (más vencido primero)."""
    qs = qs if qs is not None else Programa.objects.all()
    qs = (
        qs.filter(activo=True, maquina__activa=True, actividad__activa=True)
        .select_related("maquina", "maquina__area", "actividad", "responsable")
        .prefetch_related("servicios")
    )
    return sorted(qs, key=lambda p: p.dias_restantes)


# ---------------------------------------------------------------------------
# Tablero
# ---------------------------------------------------------------------------
class Tablero(LoginRequiredMixin, TemplateView):
    template_name = "mantenimiento/tablero.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        hoy = timezone.localdate()

        area_id = self.request.GET.get("area") or ""
        frecuencia = self.request.GET.get("frecuencia") or ""

        qs = Programa.objects.all()
        if area_id:
            qs = qs.filter(maquina__area_id=area_id)
        if frecuencia:
            qs = qs.filter(actividad__frecuencia=frecuencia)

        programas = programas_ordenados(qs)

        vencidos = [p for p in programas if p.estado == Programa.VENCIDO]
        proximos = [p for p in programas if p.estado == Programa.PROXIMO]

        # Resumen por área (semáforo)
        resumen = []
        for area in Area.objects.filter(activa=True):
            ps = [p for p in programas if p.maquina.area_id == area.id]
            resumen.append({
                "area": area,
                "maquinas": area.maquinas.filter(activa=True).count(),
                "total": len(ps),
                "vencidos": sum(1 for p in ps if p.estado == Programa.VENCIDO),
                "proximos": sum(1 for p in ps if p.estado == Programa.PROXIMO),
                "al_dia": sum(1 for p in ps if p.estado == Programa.AL_DIA),
            })

        ctx.update({
            "hoy": hoy,
            "vencidos": vencidos,
            "proximos": proximos,
            "total_programas": len(programas),
            "al_dia": len(programas) - len(vencidos) - len(proximos),
            "resumen": resumen,
            "areas": Area.objects.filter(activa=True),
            "frecuencias": Actividad.FRECUENCIAS,
            "f_area": area_id,
            "f_frecuencia": frecuencia,
            "ultimos": Servicio.objects.select_related(
                "programa__maquina__area", "programa__actividad", "realizado_por"
            )[:10],
            "cumplimiento_30d": Servicio.objects.filter(
                estado=Servicio.REALIZADO, fecha__gte=hoy - timedelta(days=30)
            ).count(),
        })
        return ctx


class Agenda(LoginRequiredMixin, TemplateView):
    """Qué toca en los próximos N días, agrupado por fecha."""

    template_name = "mantenimiento/agenda.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        dias = int(self.request.GET.get("dias", 15))
        limite = timezone.localdate() + timedelta(days=dias)
        programas = [p for p in programas_ordenados() if p.proxima_fecha <= limite]

        agenda = {}
        for p in programas:
            agenda.setdefault(p.proxima_fecha, []).append(p)

        ctx["dias"] = dias
        ctx["agenda"] = sorted(agenda.items())
        return ctx


# ---------------------------------------------------------------------------
# CRUD Áreas
# ---------------------------------------------------------------------------
class AreaList(LoginRequiredMixin, ListView):
    model = Area
    template_name = "mantenimiento/area_list.html"
    context_object_name = "areas"

    def get_queryset(self):
        return Area.objects.annotate(n_maquinas=Count("maquinas"))


class AreaCreate(LoginRequiredMixin, CreateView):
    model = Area
    form_class = AreaForm
    template_name = "mantenimiento/form.html"
    extra_context = {"titulo": "Nueva área"}


class AreaUpdate(LoginRequiredMixin, UpdateView):
    model = Area
    form_class = AreaForm
    template_name = "mantenimiento/form.html"
    extra_context = {"titulo": "Editar área"}


class AreaDelete(LoginRequiredMixin, DeleteView):
    model = Area
    template_name = "mantenimiento/confirm_delete.html"
    success_url = reverse_lazy("area_list")


# ---------------------------------------------------------------------------
# CRUD Máquinas
# ---------------------------------------------------------------------------
class MaquinaList(LoginRequiredMixin, ListView):
    model = Maquina
    template_name = "mantenimiento/maquina_list.html"
    context_object_name = "maquinas"
    paginate_by = 30

    def get_queryset(self):
        qs = Maquina.objects.select_related("area").prefetch_related(
            "programas__actividad", "programas__servicios"
        )
        q = self.request.GET.get("q")
        area = self.request.GET.get("area")
        tipo = self.request.GET.get("tipo")
        if q:
            qs = qs.filter(
                Q(nombre__icontains=q) | Q(codigo__icontains=q)
                | Q(controlador__icontains=q) | Q(area__nombre__icontains=q)
            )
        if area:
            qs = qs.filter(area_id=area)
        if tipo:
            qs = qs.filter(tipo=tipo)
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["areas"] = Area.objects.all()
        ctx["tipos"] = Maquina.TIPOS
        ctx["q"] = self.request.GET.get("q", "")
        return ctx


class MaquinaDetail(LoginRequiredMixin, DetailView):
    model = Maquina
    template_name = "mantenimiento/maquina_detail.html"
    context_object_name = "maquina"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["programas"] = programas_ordenados(self.object.programas.all())
        ctx["historial"] = Servicio.objects.filter(
            programa__maquina=self.object
        ).select_related("programa__actividad", "realizado_por")[:100]
        return ctx


class MaquinaCreate(LoginRequiredMixin, CreateView):
    model = Maquina
    form_class = MaquinaForm
    template_name = "mantenimiento/form.html"
    extra_context = {"titulo": "Nueva máquina"}


class MaquinaUpdate(LoginRequiredMixin, UpdateView):
    model = Maquina
    form_class = MaquinaForm
    template_name = "mantenimiento/form.html"
    extra_context = {"titulo": "Editar máquina"}


class MaquinaDelete(LoginRequiredMixin, DeleteView):
    model = Maquina
    template_name = "mantenimiento/confirm_delete.html"
    success_url = reverse_lazy("maquina_list")


# ---------------------------------------------------------------------------
# CRUD Actividades
# ---------------------------------------------------------------------------
class ActividadList(LoginRequiredMixin, ListView):
    model = Actividad
    template_name = "mantenimiento/actividad_list.html"
    context_object_name = "actividades"

    def get_queryset(self):
        qs = Actividad.objects.annotate(n_programas=Count("programas"))
        f = self.request.GET.get("frecuencia")
        return qs.filter(frecuencia=f) if f else qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["frecuencias"] = Actividad.FRECUENCIAS
        return ctx


class ActividadCreate(LoginRequiredMixin, CreateView):
    model = Actividad
    form_class = ActividadForm
    template_name = "mantenimiento/form.html"
    extra_context = {"titulo": "Nueva actividad"}


class ActividadUpdate(LoginRequiredMixin, UpdateView):
    model = Actividad
    form_class = ActividadForm
    template_name = "mantenimiento/form.html"
    extra_context = {"titulo": "Editar actividad"}


class ActividadDelete(LoginRequiredMixin, DeleteView):
    model = Actividad
    template_name = "mantenimiento/confirm_delete.html"
    success_url = reverse_lazy("actividad_list")


# ---------------------------------------------------------------------------
# CRUD Programas
# ---------------------------------------------------------------------------
class ProgramaCreate(LoginRequiredMixin, CreateView):
    model = Programa
    form_class = ProgramaForm
    template_name = "mantenimiento/form.html"
    extra_context = {"titulo": "Asignar actividad a máquina"}

    def get_initial(self):
        ini = super().get_initial()
        if "maquina" in self.request.GET:
            ini["maquina"] = self.request.GET["maquina"]
        return ini


class ProgramaUpdate(LoginRequiredMixin, UpdateView):
    model = Programa
    form_class = ProgramaForm
    template_name = "mantenimiento/form.html"
    extra_context = {"titulo": "Editar programación"}


class ProgramaDelete(LoginRequiredMixin, DeleteView):
    model = Programa
    template_name = "mantenimiento/confirm_delete.html"

    def get_success_url(self):
        return reverse_lazy("maquina_detail", args=[self.object.maquina_id])


# ---------------------------------------------------------------------------
# CRUD Servicios (con evidencias)
# ---------------------------------------------------------------------------
class ServicioList(LoginRequiredMixin, ListView):
    model = Servicio
    template_name = "mantenimiento/servicio_list.html"
    context_object_name = "servicios"
    paginate_by = 40

    def get_queryset(self):
        qs = Servicio.objects.select_related(
            "programa__maquina__area", "programa__actividad", "realizado_por"
        )
        g = self.request.GET
        if g.get("area"):
            qs = qs.filter(programa__maquina__area_id=g["area"])
        if g.get("maquina"):
            qs = qs.filter(programa__maquina_id=g["maquina"])
        if g.get("desde"):
            qs = qs.filter(fecha__gte=g["desde"])
        if g.get("hasta"):
            qs = qs.filter(fecha__lte=g["hasta"])
        if g.get("q"):
            qs = qs.filter(
                Q(observaciones__icontains=g["q"]) | Q(hallazgos__icontains=g["q"])
                | Q(programa__actividad__nombre__icontains=g["q"])
            )
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["areas"] = Area.objects.all()
        ctx["maquinas"] = Maquina.objects.select_related("area")
        ctx["g"] = self.request.GET
        return ctx


class ServicioDetail(LoginRequiredMixin, DetailView):
    model = Servicio
    template_name = "mantenimiento/servicio_detail.html"
    context_object_name = "servicio"


class ServicioFormMixin:
    model = Servicio
    form_class = ServicioForm
    template_name = "mantenimiento/servicio_form.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        if self.request.POST:
            ctx["formset"] = EvidenciaFormSet(
                self.request.POST, self.request.FILES, instance=self.object
            )
        else:
            ctx["formset"] = EvidenciaFormSet(instance=self.object)
        return ctx

    def form_valid(self, form):
        ctx = self.get_context_data()
        formset = ctx["formset"]
        if not form.instance.realizado_por_id and not form.instance.tecnico_externo:
            form.instance.realizado_por = self.request.user
        self.object = form.save()
        formset.instance = self.object
        if formset.is_valid():
            formset.save()
        messages.success(self.request, "Servicio guardado correctamente.")
        return redirect(self.object.get_absolute_url())


class ServicioCreate(LoginRequiredMixin, ServicioFormMixin, CreateView):
    extra_context = {"titulo": "Registrar servicio"}

    def get_initial(self):
        ini = super().get_initial()
        if "programa" in self.request.GET:
            ini["programa"] = self.request.GET["programa"]
        return ini


class ServicioUpdate(LoginRequiredMixin, ServicioFormMixin, UpdateView):
    extra_context = {"titulo": "Editar servicio"}


class ServicioDelete(LoginRequiredMixin, DeleteView):
    model = Servicio
    template_name = "mantenimiento/confirm_delete.html"
    success_url = reverse_lazy("servicio_list")


# ---------------------------------------------------------------------------
# Exportación
# ---------------------------------------------------------------------------
@login_required
def exportar_servicios(request):
    resp = HttpResponse(content_type="text/csv; charset=utf-8")
    resp["Content-Disposition"] = 'attachment; filename="historial_servicios.csv"'
    resp.write("\ufeff")
    w = csv.writer(resp)
    w.writerow([
        "Fecha", "Área", "Máquina", "Controlador", "Actividad", "Frecuencia",
        "Estado", "Atendido por", "Duración (min)", "Hallazgos", "Observaciones",
        "Seguimiento", "Evidencias",
    ])
    for s in Servicio.objects.select_related(
        "programa__maquina__area", "programa__actividad", "realizado_por"
    ):
        w.writerow([
            s.fecha, s.programa.maquina.area.nombre, s.programa.maquina.nombre,
            s.programa.maquina.controlador, s.programa.actividad.nombre,
            s.programa.actividad.get_frecuencia_display(), s.get_estado_display(),
            s.atendido_por, s.duracion_min or "", s.hallazgos, s.observaciones,
            "Sí" if s.requiere_seguimiento else "No",
            "Sí" if s.tiene_evidencia else "No",
        ])
    return resp


@login_required
def exportar_pendientes(request):
    resp = HttpResponse(content_type="text/csv; charset=utf-8")
    resp["Content-Disposition"] = 'attachment; filename="pendientes.csv"'
    resp.write("\ufeff")
    w = csv.writer(resp)
    w.writerow([
        "Área", "Máquina", "Controlador", "Actividad", "Frecuencia",
        "Último servicio", "Próxima fecha", "Días restantes", "Estado",
    ])
    for p in programas_ordenados():
        w.writerow([
            p.maquina.area.nombre, p.maquina.nombre, p.maquina.controlador,
            p.actividad.nombre, p.actividad.get_frecuencia_display(),
            p.ultima_fecha or "", p.proxima_fecha, p.dias_restantes, p.estado_label,
        ])
    return resp

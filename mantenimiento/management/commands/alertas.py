"""Reporte de mantenimientos vencidos y por vencer. Ideal para un cron diario.

    python manage.py alertas --dias 7
    python manage.py alertas --dias 7 --email jefe@empresa.com --email tecnico@empresa.com
"""
from django.core.mail import send_mail
from django.core.management.base import BaseCommand
from django.utils import timezone

from mantenimiento.models import Programa


class Command(BaseCommand):
    help = "Lista mantenimientos vencidos y próximos a vencer."

    def add_arguments(self, parser):
        parser.add_argument("--dias", type=int, default=7,
                            help="Ventana de anticipación en días (default 7).")
        parser.add_argument("--email", action="append", default=[],
                            help="Destinatario del reporte. Se puede repetir.")

    def handle(self, *args, **opts):
        hoy = timezone.localdate()
        programas = (
            Programa.objects.filter(activo=True, maquina__activa=True, actividad__activa=True)
            .select_related("maquina__area", "actividad")
        )
        pendientes = sorted(
            (p for p in programas if p.dias_restantes <= opts["dias"]),
            key=lambda p: p.dias_restantes,
        )

        lineas = [f"Reporte de mantenimiento — {hoy}", ""]
        for p in pendientes:
            marca = "VENCIDO" if p.dias_restantes < 0 else f"faltan {p.dias_restantes} d"
            lineas.append(
                f"[{marca}] {p.maquina.area.nombre} · {p.maquina.nombre} "
                f"({p.maquina.controlador}) → {p.actividad.nombre} "
                f"[{p.actividad.get_frecuencia_display()}] vence {p.proxima_fecha}"
            )
        if not pendientes:
            lineas.append("Sin pendientes en la ventana indicada.")
        texto = "\n".join(lineas)
        self.stdout.write(texto)

        if opts["email"]:
            send_mail(
                subject=f"Mantenimiento PRIVA/VIALUX — {len(pendientes)} pendientes ({hoy})",
                message=texto,
                from_email=None,
                recipient_list=opts["email"],
                fail_silently=False,
            )
            self.stdout.write(self.style.SUCCESS("Correo enviado."))

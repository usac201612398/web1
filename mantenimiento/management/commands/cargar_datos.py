"""Carga el catálogo inicial: áreas, 25 máquinas, actividades y programación.

Uso:
    python manage.py cargar_datos
    python manage.py cargar_datos --reset   # borra y vuelve a cargar
"""
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone

from mantenimiento.models import Actividad, Area, Maquina, Programa

# (área, máquina, controlador)
MAQUINAS = [
    ("Cecilio", "Priva 2", "Conext"),
    ("Cecilio", "Priva 3", "Conext"),
    ("Cecilio", "Vialux", "Intégro"),
    ("CIP", "Priva 4", "Conext"),
    ("CIP", "Priva 7", "Conext"),
    ("Provalle", "Priva 1", "Conext"),
    ("Provalle", "Vialux", "Conext"),
    ("Rio", "Priva 1", "Intégro"),
    ("Rio", "Priva 2", "Intégro"),
    ("Rio", "Priva 3", "Intégro"),
    ("Rio", "Vialux", "Intégro"),
    ("Valle", "Priva 1", "Intégro"),
    ("Valle", "Priva 2", "Intégro"),
    ("Valle", "Priva 3", "Intégro"),
    ("Valle", "Priva 4", "Intégro"),
    ("Valle", "Priva 5", "Intégro"),
    ("Valle", "Priva 7", "Compact"),
    ("Valle", "Priva 8", "Compact"),
    ("Valle", "Vialux 1", "Intégro"),
    ("Valle", "Vialux 2", "Intégro"),
    ("Valle", "Vialux 3", "Intégro"),
    ("SL", "Priva 1", "Compact"),
    ("SL", "Priva 2", "Compact"),
    ("SL", "Priva 4", "Compact"),
    ("SL", "Vialux", "Compact"),
]

# (nombre, frecuencia, descripción, requiere_evidencia)
ACTIVIDADES = [
    (
        "Comprobar que no hayan fugas y ruidos anormales en la bomba",
        Actividad.SEMANAL,
        "Inspección visual y auditiva de la bomba: revisar sellos, acoples y "
        "tuberías en busca de fugas; escuchar ruidos anormales (cavitación, "
        "rodamientos, vibración).",
        True,
    ),
    (
        "Comprobar la cantidad de agua de riego utilizada por las plantas",
        Actividad.SEMANAL,
        "Para cada válvula de riego, colocar un número de goteros en vasos de "
        "plástico. Después del ciclo de riego, agregar el contenido de los vasos "
        "en un beaker y leer el volumen. Dividir este volumen entre el número de "
        "vasos para determinar el promedio por gotero.",
        False,
    ),
    (
        "Mantener la unidad y el entorno limpios",
        Actividad.SEMANAL,
        "Limpieza general de la unidad y su área circundante: retirar residuos, "
        "polvo y derrames de fertilizante.",
        True,
    ),
    (
        "Limpiar filtro de la línea",
        Actividad.MENSUAL,
        "Aflojar el acoplamiento y retirar el elemento filtrante de la carcasa. "
        "Enjuagar el elemento filtrante debajo del grifo hasta que esté limpio. "
        "Colocar el elemento y apretar.",
        True,
    ),
    (
        "Limpiar el filtro de dosificación",
        Actividad.MENSUAL,
        "Cerrar la válvula de la línea de fertilizante correspondiente. Colocar un "
        "recipiente de plástico debajo del filtro. Desenroscar la tapa del filtro y "
        "retirar el elemento filtrante de la carcasa. Enjuagar el elemento debajo "
        "del grifo hasta que esté limpio. Colocar el elemento y atornillar.",
        True,
    ),
    (
        "Verificar la presión de la bomba del sistema en funcionamiento",
        Actividad.MENSUAL,
        "Con el sistema en funcionamiento, leer el manómetro en la tubería y "
        "registrar la presión. Comparar contra el valor nominal de la máquina.",
        False,
    ),
    (
        "Limpiar sensores de pH",
        Actividad.MENSUAL,
        "Limpiar la membrana de vidrio y la carcasa con un cepillo suave o un paño "
        "limpio humedecido en solución jabonosa. Enjuagar la membrana con agua "
        "destilada. Sumergir el sensor durante 30 minutos en una mezcla 50/50 de "
        "tampón de pH 4. Recalibrar después de la limpieza.",
        True,
    ),
    (
        "Limpiar el sensor de flujo",
        Actividad.ANUAL,
        "Vaciar la línea de presión. Desenroscar el sensor de flujo de la pieza en "
        "T. Limpiar la rueda de paletas con un cepillo pequeño y suave. Aplicar un "
        "poco de grasa sin ácido a las juntas tóricas de goma. Colocar el sensor y "
        "atornillar.",
        True,
    ),
    (
        "Comprobar el funcionamiento de los canales de dosificación",
        Actividad.ANUAL,
        "Verificar canal por canal la inyección de fertilizante, tiempos de "
        "apertura y respuesta de la válvula dosificadora.",
        False,
    ),
    (
        "Verificar el interruptor de nivel bajo en el tanque de mezcla",
        Actividad.ANUAL,
        "Simular condición de nivel bajo y confirmar que el interruptor active la "
        "alarma y detenga la bomba.",
        False,
    ),
    (
        "Comprobar el flotador de control en el tanque de mezcla",
        Actividad.ANUAL,
        "Revisar libertad de movimiento, estado del flotador y correcta señal hacia "
        "el controlador.",
        False,
    ),
    (
        "Comprobar la válvula de llenado",
        Actividad.ANUAL,
        "Verificar apertura y cierre completos, ausencia de fugas y tiempo de "
        "llenado del tanque.",
        False,
    ),
    (
        "Limpiar tableros, gabinetes, flipones eléctricos y transferencia",
        Actividad.ANUAL,
        "Sopletear y, con el líquido especializado, limpiar contactos. Revisar "
        "estado de flipones y del equipo de transferencia.",
        True,
    ),
    (
        "Limpiar paneles eléctricos",
        Actividad.ANUAL,
        "Sopletear y, con el líquido especializado, limpiar contactos de los "
        "paneles eléctricos.",
        True,
    ),
    (
        "Revisar borneras y ajustar",
        Actividad.ANUAL,
        "Revisar el torque de las borneras y ajustar las conexiones flojas. "
        "Verificar señales de calentamiento o decoloración.",
        True,
    ),
]


class Command(BaseCommand):
    help = "Carga áreas, máquinas, actividades y programación inicial."

    def add_arguments(self, parser):
        parser.add_argument(
            "--reset", action="store_true",
            help="Elimina programación, máquinas, actividades y áreas antes de cargar.",
        )

    @transaction.atomic
    def handle(self, *args, **opts):
        if opts["reset"]:
            Programa.objects.all().delete()
            Maquina.objects.all().delete()
            Actividad.objects.all().delete()
            Area.objects.all().delete()
            self.stdout.write(self.style.WARNING("Datos anteriores eliminados."))

        # Áreas
        areas = {}
        for nombre in dict.fromkeys(a for a, _, _ in MAQUINAS):
            areas[nombre], _ = Area.objects.get_or_create(nombre=nombre)
        self.stdout.write(self.style.SUCCESS(f"Áreas: {len(areas)}"))

        # Máquinas
        n_maq = 0
        maquinas = []
        for area, nombre, controlador in MAQUINAS:
            tipo = Maquina.TIPO_VIALUX if "vialux" in nombre.lower() else Maquina.TIPO_PRIVA
            m, creada = Maquina.objects.get_or_create(
                area=areas[area], nombre=nombre,
                defaults={"controlador": controlador, "tipo": tipo},
            )
            maquinas.append(m)
            n_maq += int(creada)
        self.stdout.write(self.style.SUCCESS(f"Máquinas nuevas: {n_maq} (total {len(maquinas)})"))

        # Actividades
        actividades = []
        n_act = 0
        for nombre, frecuencia, desc, evidencia in ACTIVIDADES:
            a, creada = Actividad.objects.get_or_create(
                nombre=nombre,
                defaults={
                    "frecuencia": frecuencia,
                    "descripcion": desc,
                    "requiere_evidencia": evidencia,
                },
            )
            actividades.append(a)
            n_act += int(creada)
        self.stdout.write(self.style.SUCCESS(f"Actividades nuevas: {n_act}"))

        # Programación: todas las actividades a todas las máquinas
        hoy = timezone.localdate()
        n_prog = 0
        for m in maquinas:
            for a in actividades:
                if a.aplica_a != "TODAS" and a.aplica_a != m.tipo:
                    continue
                _, creado = Programa.objects.get_or_create(
                    maquina=m, actividad=a, defaults={"fecha_base": hoy}
                )
                n_prog += int(creado)
        self.stdout.write(self.style.SUCCESS(f"Programas nuevos: {n_prog}"))
        self.stdout.write(self.style.SUCCESS("Carga inicial completa."))

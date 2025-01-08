from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from datetime import time 
from django.core.mail import send_mail
from .models import Ingresop

@receiver(post_save, sender=Ingresop)
def verificar_entrada_tras_salida(sender, instance, created, **kwargs):
    if instance.evento == 'Salida':
        ahora = timezone.now()  # Esto es un datetime consciente

        # Asegúrate de que 'instance.marcat' sea consciente (si es ingenuo)
        if instance.marcat.tzinfo is None:  # Si es ingenuo (sin zona horaria)
            print("Marcat es ingenuo, convirtiendo a consciente")
            instance.marcat = timezone.make_aware(instance.marcat, timezone.get_current_timezone())

        # Verificar si han pasado más de 30 minutos
        if ahora - instance.marcat > timezone.timedelta(minutes=30):
            print(f"Han pasado más de 30 minutos desde la salida de {instance.nombrep}")
            # Verificar si es antes de las 5 PM
            if ahora.hour < 17:
                print("Es antes de las 5 PM")
                # Verificar si no se ha registrado una entrada después de la salida
                if not Ingresop.objects.filter(codigop=instance.codigop, evento='Entrada', marcat__gt=instance.marcat).exists():
                    print(f"No se ha registrado una entrada después de la salida de {instance.nombrep}")
                    # Enviar correo electrónico
                    send_mail(
                        'Alerta: Entrada no registrada',
                        f'La persona {instance.nombrep} no ha registrado su entrada después de más de 30 minutos de salida.',
                        'brandrenz99@gmail.com.gt',  # Tu dirección de correo
                        ['brandon.portillo@popoyan.com.gt'],  # Correo del usuario
                    )
                else:
                    print(f"Ya se ha registrado una entrada después de la salida de {instance.nombrep}")

@receiver(post_save, sender=Ingresop)
def verificar_primera_entrada(sender, instance, created, **kwargs):
    if instance.evento == 'Entrada':  # Solo nos interesa cuando es una entrada
        ahora = timezone.now()
        fecha_entrada = instance.marcat.date()

        # Verificar si es la primera entrada del día para ese usuario
        primera_entrada = not Ingresop.objects.filter(nombrep=instance.nombrep, evento='Entrada', marcat__date=fecha_entrada).exclude(id=instance.id).exists()

        if primera_entrada:
            # Verificar si la hora de la entrada es posterior a las 7:15 AM
            if instance.marcat.time() > time(7, 15):  # Usamos time() de datetime
                # Enviar correo si se cumple la condición
                send_mail(
                    'Alerta: Entrada tarde',
                    f'La persona {instance.nombrep} ha registrado su entrada después de las 7:15 AM. A la hora {instance.marcat.time()}',
                    'brandrenz99@gmail.com',  # Tu dirección de correo
                    ['brandon.portillo@popoyan.com.gt'],  # Correo del usuario
                )

from django.apps import AppConfig


class App1Config(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app1'

    def ready(self):
        # Importar el archivo signals.py donde definimos la señal
        import app1.signals  # Asegúrate de que el nombre de la app sea correcto
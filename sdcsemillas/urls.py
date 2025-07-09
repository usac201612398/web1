# semillassdc/urls.py
from django.urls import path
from .views import conteoplantas as cp

app_main ="sdcsemillas"

urlpatterns = [
    path('conteoplantas/', cp.ConteoPlantasList.as_view(), name='conteoplantas_list'),
    path('conteoplantas/nuevo/', cp.ConteoPlantasCreate.as_view(), name='conteoplantas_create'),
    path('conteoplantas/<int:pk>/editar/', cp.ConteoPlantasUpdate.as_view(), name='conteoplantas_update'),
    path('conteoplantas/<int:pk>/borrar/', cp.ConteoPlantasDelete.as_view(), name='conteoplantas_delete'),
]
# semillassdc/urls.py
from django.urls import path
from . import views


app_main = 'sdcsemillas'

urlpatterns = [

#    path('', views.index, name='index'),  # Página principal
    path("lotes",views.lotes_list,name='lotes_list'),
    path('lotes/<int:pk>/', views.lotes_detail, name='lotes_detail'),
    path('lotes/new/', views.lotes_create, name='lotes_create'),
    path('lotes/<int:pk>/edit/', views.lotes_update, name='lotes_update'),
    path('lotes/<int:pk>/delete/', views.lotes_delete, name='lotes_delete'),

]
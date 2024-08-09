from django.urls import path
from plantaE import views
#from app1.views import *

app_main ="plantaE"

urlpatterns = [
#    path("homepage/", views.homepage, name="homepage"),
#    path('logout/', views.logout_view, name='logout'),
    path("",views.article_list,name='salidasFruta_list'),
    path('salidasFruta/<int:pk>/', views.article_detail, name='salidasFruta_detail'),
    path('salidasFruta/new/', views.article_create, name='salidasFruta_create'),
    path('salidasFruta/<int:pk>/edit/', views.article_update, name='salidasFruta_update'),
    path('salidasFruta/<int:pk>/delete/', views.article_delete, name='salidasFruta_delete'),
]

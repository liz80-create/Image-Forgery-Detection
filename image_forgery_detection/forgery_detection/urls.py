from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('splicing/', views.splicing, name='splicing'),
    path('copy_move/', views.copy_move, name='copy_move'),
    path('signature/', views.signature, name='signature'),
    path('compression/', views.compression, name='compression'),
]
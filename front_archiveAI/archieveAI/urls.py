from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('sqlchat/', views.sqlchat_proxy, name='sqlchat_proxy'),
    path('resposta/', views.resposta, name='resposta'),
]
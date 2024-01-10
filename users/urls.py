from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_api_view),
    path('authorize/', views.authorize_api_view),
]
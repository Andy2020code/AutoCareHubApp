from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('generate-response/<str:user_input>', views.get_response, name='get_user_input'),
]
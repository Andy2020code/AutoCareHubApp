from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('send-info/<str:user_input>', views.predict_intent, name='get_user_input'),
    path('get-keywords/<str:keywords>', views.handle_message, name='send_receive_keywords'),
]
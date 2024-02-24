from django.urls import path
from . import views

app_name = 'chatbot'
urlpatterns = [
    path('chat/', views.chat, name='chat'),
    path('get-response/', views.get_response, name='get_response'),
    path('get-user-data/', views.get_user_data, name='get_user_data'),
    path('dictionary/', views.dictionary, name='dictionary')
]

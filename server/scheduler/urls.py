from django.urls import path
from. import views

app_name = 'scheduler'
urlpatterns = [
    path('', views.index, name='index'),
    path('schedule/', views.index, name='schedule'),
    path('step-02/', views.step_02, name='step_02'),
    path('update-car-info/', views.update_car_info, name='update_car_info'),
    path('step-03/', views.step_03, name='step_03'),
    path('appointment-scheduled/', views.success_schedule, name='success_schedule'),
]

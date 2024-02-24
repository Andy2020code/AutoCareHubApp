from django.urls import path
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView
from . import views


app_name = 'main'
urlpatterns = [
    path('', views.home, name='home'),
    path('how-it-works', views.how_it_works, name='how_it_works'),
    path('forum', views.forum, name='forum'),
    path('user-home', views.user_home, name='user-home'),
    path('about', views.about, name='about'),
    path('coming-soon', views.coming_soon, name='coming_soon'),
    path('browse-services', views.Browse_Services, name='browse_services'),
    path('sign-up', views.sign_up, name='sign-up'),
    path('login', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login_user'),
    path('logout', auth_views.LogoutView.as_view(), name='logout'),
    path('create-post', views.create_post, name='create_post'),
    path('delete_post/<int:post_id>/', views.delete_post, name='delete_post'),
    path('car-info', views.car_info, name='car_info'),
    path('service_request', views.service_request_view, name='service_request_view'),
    path('service_list', views.service_request_list, name='service_request_list'),
    path('available-mechanics', views.available_mechanics, name='available_mechanics'),
    path('about-mechanic', views.about_mechanic, name='about_mechanic'),
    path('last_maintenance', views.most_recent_maintenace, name='last_maintenance'),
    path('success_newsletter', views.home, name='success_newsletter'),


    path('user_data/<str:username>/', views.user_data, name='user_data'),
    path('update_upcoming_maintenance/<int:owner>/', views.update_upcoming_maintenance, name='edit_post'),
    path('update_car_info/<int:owner>/', views.update_car_info, name='edit_car_info'),


    path('bussiness_creation_form', views.BussinessCreation, name='bussiness_creation_form'),
    path('leave_review_front_page', views.LeaveReviewIntroPage, name='leave_review_front_page'),


    path('robots.txt', TemplateView.as_view(template_name='main/robots.txt', content_type='text/plain')),

    path('oil-change-service', views.oil_change_service, name='oil_change_service'),
    path('break-pads-service', views.break_pads_service, name='break_pads_service'),
    path('alternator-service', views.alterantor_repair_service, name='alternator_service'),
    path('check-engine-light-service', views.check_engine_light_service, name='alternator_service'),
    path('diagnostics-service', views.diagnostics_service, name='diagnostics_service'),
    path('electrical-repair-service', views.electrical_repair_service, name='electrical_repair_service'),


]
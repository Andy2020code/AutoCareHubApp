from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Post, Car_Information, ServiceRequest, LeaveReview, MostRecentMaintenance, Subscriber, BussinessCreationModel, LeaveReviewFrontPage

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("email", "username", "password1", "password2")



class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'description')



class Car_info_form(forms.ModelForm):
    class Meta:
        model = Car_Information
        fields = ['car_model', 'car_make', 'car_year', 'car_vin']



class ServiceRequestForm(forms.ModelForm):
    class Meta:
        model = ServiceRequest
        fields = ['client_full_name', 'client_birthdate','client_email', 'client_phone', 'vehicle_make', 'vehicle_model', 'vehicle_year', 'service_requested']



class leave_review_form(forms.ModelForm):
    class Meta:
        model = LeaveReview
        fields = ['review_content']


class leave_review_form_front_page(forms.ModelForm):
    class Meta:
        model = LeaveReviewFrontPage
        fields = ['review_content']



class upcoming_maintenance_form(forms.ModelForm):
    class Meta:
        model = MostRecentMaintenance
        fields = ['last_service_requested', 'date_of_service']



class SubscriptionForm(forms.ModelForm):
    class Meta:
        model = Subscriber
        fields = ['email']





# Form to BussinessCreationModel
        
class BusinessCreationForm(forms.ModelForm):
    class Meta:
        model = BussinessCreationModel
        fields = ['BussinessName', 'BussinessAddress', 'BussinessPhoneNumber', 'BussinessEmail', 'BussinessWebsite']
        
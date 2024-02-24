from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title + "\n" + self.description
    


class Car_Information(models.Model):
    car_year = models.CharField(max_length=4)
    car_make = models.CharField(max_length=20)
    car_model = models.CharField(max_length=20)
    car_vin = models.CharField(max_length=17, blank=True, null=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=False)

    def __str__(self):
        return self.car_model + "\n" + self.car_make + "\n" + self.car_year + "\n" + self.owner.username
    


class ServiceRequest(models.Model):
    service_requested = models.CharField(max_length=100)
    client_full_name = models.CharField(max_length=100, default='Peter Parker')
    client_username_id = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    client_birthdate = models.DateField(max_length=8, default='YYYY-MM-DD')
    client_email = models.EmailField(max_length=254, default='name@domain.com')
    client_phone = models.CharField(max_length=10, default='555-555-5555')

    vehicle_make = models.CharField(max_length=50, default='Ford')
    vehicle_model = models.CharField(max_length=50, default='F150')
    vehicle_year = models.CharField(max_length=4, default='2020')

    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    

    def __str__(self):
        return self.service_requested + "\n" + self.client_full_name
    


class LeaveReview(models.Model):
    client_username_id = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    review_content = models.TextField(max_length=500)
    created_on = models.DateTimeField(auto_now_add=True)

class LeaveReviewFrontPage(models.Model):
    client_username_id = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    review_content = models.TextField(max_length=500)
    created_on = models.DateTimeField(auto_now_add=True)

  


class MostRecentMaintenance(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    last_service_requested = models.CharField(max_length=100)
    date_of_service = models.DateField(max_length=8, default='MM/DD/YYYY')




class Subscriber(models.Model):
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.email
    





#Bussiness Models
    
# 1st model MERCEDES BENZ Of BUCKHEAD
    
class BussinessCreationModel(models.Model):
    BussinessName = models.CharField(max_length=100)
    BussinessAddress = models.CharField(max_length=1000)
    BussinessPhoneNumber = models.CharField(max_length=100)
    BussinessEmail = models.EmailField(max_length=100)
    BussinessWebsite = models.CharField(max_length=100)

    def __str__(self):
        return self.BussinessName + "\n" + self.BussinessAddress + "\n" + self.BussinessPhoneNumber + "\n" + self.BussinessEmail + "\n" + self.BussinessWebsite

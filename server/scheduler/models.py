from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Event(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    date = models.CharField(max_length=100)
    desired_time = models.TimeField(default='00:00')
    service_desired = models.CharField(max_length=100)
    street_address = models.CharField(max_length=100, default='123 Main St')
    zip_code = models.CharField(max_length=10, default='30303')
    city = models.CharField(max_length=100, default='Atlanta')
    state = models.CharField(max_length=100, default='GA')

    class Meta:
        unique_together = ['date', 'desired_time', 'service_desired']
        
    def __str__(self):
        return f"{self.user} - {self.date} - {self.desired_time} - {self.service_desired} - {self.street_address} - {self.zip_code} - {self.city} - {self.state}"
from django.db import models

class Intents_model_00(models.Model):
    id = models.AutoField(primary_key=True)
    tag = models.CharField(max_length=100)
    patterns = models.TextField()
    responses = models.TextField()
    context = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        ordering = ['created_at']


class user_input(models.Model):
    id = models.AutoField(primary_key=True)
    user_input_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']
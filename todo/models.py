from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Task(models.Model):

     status_choices = (
          ('PENDING', 'Pending'),
          ('COMPLETED', 'Completed'),
          ('IN PROGRESS', 'In Progress'),
     )

     user = models.ForeignKey(User, on_delete=models.CASCADE)
     title = models.CharField(max_length=200)
     description = models.TextField()
     created_at = models.DateTimeField(auto_now_add=True)
     updated_at = models.DateTimeField(auto_now=True)
     status = models.CharField(max_length=20, choices=status_choices, default='PENDING')
     category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True)

     def __str__(self):
          return self.title

class Category(models.Model):
     name = models.CharField(max_length=200)
     description = models.TextField()

     def __str__(self):
          return self.name


from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Attend(models.Model):
  attender = models.ForeignKey(User, on_delete=models.CASCADE)
  datetime = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return str(str(self.attender.username)+ " " + str(self.datetime)[:19])

class Face(models.Model):
  images = models.ImageField(upload_to='training_images')


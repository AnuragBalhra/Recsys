from django.db import models
from django.contrib.auth import models 
# Create your models here.

class User(models.AbstractUser):
	
	def attrs(self):
		for field in self._meta.fields:
			yield field.name, getattr(self, field.name)
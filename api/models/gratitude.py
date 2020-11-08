from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.
class Gratitude(models.Model):
  # define fields
  # https://docs.djangoproject.com/en/3.0/ref/models/fields/
  text = models.CharField(max_length=250)
  owner = models.ForeignKey(
      get_user_model(),
      on_delete=models.CASCADE
  )
  created_at = models.DateField(auto_now_add=True)

  def __str__(self):
    # This must return a string
    return f"The gratitude created on '{self.created_at}' by {self.owner} was {self.text}."

  def as_dict(self):
    """Returns dictionary version of Mango models"""
    return {
        'id': self.id,
        'text': self.text,
        'owner': self.owner,
        'created_at': self.created_at
    }

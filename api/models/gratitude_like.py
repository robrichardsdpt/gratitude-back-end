from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.
class Gratitude_like(models.Model):
  # define fields
  # https://docs.djangoproject.com/en/3.0/ref/models/fields/
  like = models.IntegerField(default = 0)
  owner = models.ForeignKey(
      get_user_model(),
      on_delete=models.CASCADE
  )
  gratitude = models.ForeignKey(
        'Gratitude',
        on_delete=models.CASCADE
        )
  created_at = models.DateField(auto_now_add=True)

  def __str__(self):
    # This must return a string
    return f"{self.owner} liked {self.gratitude} on {self.created_at}."

  def as_dict(self):
    """Returns dictionary version of Like models"""
    return {
        'owner': self.owner,
        'gratitude': self.gratitude,
        'created_at': self.created_at
    }

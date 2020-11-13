from django.db import models
from django.contrib.auth import get_user_model
from .comment_like import Comment_like

# Create your models here.
class Comment(models.Model):
  # define fields
  # https://docs.djangoproject.com/en/3.0/ref/models/fields/
  text = models.CharField(max_length=250)
  owner = models.ForeignKey(
      get_user_model(),
      on_delete=models.CASCADE
  )
  created_at = models.DateTimeField(auto_now_add=True)

  gratitude = models.ForeignKey(
        'Gratitude',
        on_delete=models.CASCADE
        )

  likes = models.ManyToManyField(
    'User',
    through=Comment_like,
    through_fields=('comment', 'owner'),
    related_name='comment_likes',
    blank=True
  )

  def __str__(self):
    # This must return a string
    return f"The comment created on '{self.created_at}' by {self.owner} was {self.text}."

  def as_dict(self):
    """Returns dictionary version of Comment like models"""
    return {
        'id': self.id,
        'text': self.text,
        'owner': self.owner,
        'created_at': self.created_at
    }

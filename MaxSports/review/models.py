from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    review_star = models.IntegerField(blank=True, null=True)
    review_data = models.CharField(blank=True)

    def __str__(self):
        return self.review_star

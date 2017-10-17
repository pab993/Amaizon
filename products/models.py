from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import datetime
from django.core.validators import MaxValueValidator,  MinValueValidator


# Create your models here.

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
    price = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(100000.0)])
    picture = models.FileField()
    pub_date = models.DateTimeField()

    def __str__(self):
        return self.name

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now


class Assessment(models.Model):
    comment = models.CharField(max_length=250)
    score = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)])
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User)

    def __str__(self):
        return self.comment + " - " + self.score

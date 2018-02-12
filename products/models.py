from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime, timedelta
from django.core.validators import MaxValueValidator,  MinValueValidator


# Create your models here.
class ControlPanel(models.Model):
    threshold = models.FloatField(validators=[MinValueValidator(-1.0), MaxValueValidator(1.0)])


class Neighbours(models.Model):
    user = models.ForeignKey(User)
    idUser = models.IntegerField(null=True)
    sim = models.FloatField(null=True)


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    picture = models.FileField(blank=True)


class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
    price = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(100000.0)])
    picture = models.FileField()
    pub_date = models.DateTimeField()

    def __str__(self):
        return self.name

    @property
    def was_published_recently(self):
        now = timezone.now()
        if now - timedelta(days=15) <= self.pub_date <= now:
            return True
        else:
            return False

    @property
    def avg_rating(self):
        totalscore = 0
        total = 0
        if len(self.assessment_set.all()) != 0:
            for a in self.assessment_set.all():
                totalscore = totalscore + a.score
                total = total + 1
            return int(totalscore/total)
        else:
            return -1

    @property
    def number_of_assessments(self):
        return len(self.assessment_set.all())

    @property
    def assessments(self):
        return self.assessment_set.all()


class Assessment(models.Model):
    comment = models.CharField(max_length=250)
    score = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    post_date = models.DateTimeField(default=datetime.now())
    user = models.ForeignKey(User)

    def __str__(self):
        return self.comment + " - " + str(self.score)

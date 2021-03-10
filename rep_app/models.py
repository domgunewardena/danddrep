from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.

class Manager(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return  self.restaurant.name + ' - ' + self.user.first_name + ' ' + self.user.last_name

class OpsDirector(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return  self.user.first_name + ' ' + self.user.last_name

class Restaurant(models.Model):

    manager = models.OneToOneField(Manager, on_delete=models.CASCADE)
    ops_director = models.OneToOneField(OpsDirector, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

class Review(models.Model):

    source = models.CharField(max_length=11)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    title = models.CharField(max_length=50, default='')
    date = models.DateField()
    score = models.IntegerField()
    food = models.IntegerField(null=True)
    service = models.IntegerField(null=True)
    value = models.IntegerField(null=True)
    ambience = models.IntegerField(null=True)
    text = models.TextField(max_length=10000, null=True)
    link = models.TextField(max_length=300, null=True)
    comment = models.TextField(max_length=10000, null=True)
    replied = models.BooleanField(default=False)
    reviewed = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("rep_app:review_detail",kwargs={'pk':self.pk})

class Note(models.Model):

    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    text = models.TextField(max_length=1000, default='')

    def __str__(self):
        return self.restaurant





# class Comment(models.Model):
#
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     review = models.ForeignKey(Review, on_delete=models.CASCADE)
#     date = models.DateTimeField(auto_now_add=True)
#     text = models.TextField(max_length=1000)
#
#     def get_absolute_url(self):
#         return reverse("rep_app:review_detail",kwargs={'pk':self.review_id})

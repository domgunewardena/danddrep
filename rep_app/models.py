from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

from statistics import mean
from datetime import date, time, datetime, timedelta

def monday(date):
    return date - timedelta(date.weekday())

def weeks_ago(date, n):
    return date - timedelta(7*n)

def months_ago(date, n):
    return date - timedelta(28*n)

def one_year_ago(date):
    return date - timedelta(364)

today = one_year_ago(date.today())
monday_this = monday(today)
monday_last = weeks_ago(monday_this, 1)
monday_last_month = months_ago(monday_this, 1)

# Create your models here.

class Manager(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return  self.user.first_name + ' ' + self.user.last_name

class OpsDirector(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return  self.user.first_name + ' ' + self.user.last_name

class Restaurant(models.Model):

    name = models.CharField(max_length=30)
    opsdirector = models.ForeignKey(OpsDirector, on_delete=models.CASCADE)
    manager = models.ForeignKey(Manager, on_delete=models.CASCADE, default=1)

    score_categories = ['total','food','service','ambience','value']
    date_strings = [period + '_' + duration if period == 'last' else period + '_' + duration + 's' for duration in ['week', 'month'] for period in ['last','two','three','four']]

    def __str__(self):
        return str(self.name)

    def my_mean(self, values):
        return round(mean(values),1) if values else 0

    def my_divide(self, x,y):
        return x/y if y != 0 else 0

    def get_last_week_reviews(self):
        return Review.objects.filter(restaurant=self.id, date__gte = monday_last, date__lt = monday_this).order_by('score').only('score','food','service','value','ambience','reviewed')

    def get_last_week_unsubmitted_reviews(self):
        return Review.objects.filter(restaurant=self.id, date__gte = monday_last,date__lt = monday_this, reviewed = False, score__lt = 4).order_by('score').only('score','food','service','value','ambience','reviewed')

    def get_reviews_by_date(self, greater_than_equal_date,less_than_date):
        return Review.objects.filter(restaurant=self.id, date__gte = greater_than_equal_date, date__lt = less_than_date)

    def get_reviews_dict(self, reviews):

        return [
            {
                'total':getattr(review,'score'),
                'food':getattr(review,'food'),
                'service':getattr(review,'service'),
                'value':getattr(review,'value'),
                'ambience':getattr(review,'ambience'),
                'submitted':getattr(review, 'reviewed')
            } for review in reviews
        ]

    def get_scores_dict(self, reviews):

        reviews_dict = self.get_reviews_dict(reviews)

        return {
            category: {
                'total': len([review[category] for review in reviews_dict if review[category] > 0]),
                'average': self.my_mean([review[category] for review in reviews_dict if review[category] > 0])
            } for category in self.score_categories
        }

    def get_stats(self):

        reviews = self.get_last_week_reviews()
        reviews_dict = self.get_reviews_dict(reviews)

        return {
            'scores': {
                category:{
                    'total': len([review[category] for review in reviews_dict if review[category] > 0]),
                    'average': self.my_mean([review[category] for review in reviews_dict if  review[category] > 0])
                } for category in self.score_categories
            },
            'submissions': {
                'submitted_reviews': len([review['total'] for review in reviews_dict if review['submitted'] and review['total'] < 4]),
                'unsubmitted_reviews': len([review['total'] for review in reviews_dict if not review['submitted'] and review['total'] < 4]),
                'submitted_p': round(self.my_divide(len([review['total'] for review in reviews_dict if review['submitted'] and review['total'] < 4]), len([review['total'] for review in reviews_dict if review['total'] < 4]))*100)
            },
            'below_4': {
                'reviews_below_4': len([review['total'] for review in reviews_dict if review['total'] < 4]),
                'reviews_below_4_p': round(self.my_divide(len([review['total'] for review in reviews_dict if review['total'] < 4]), len([review['total'] for review in reviews_dict]))*100),
            }
        }

    def get_scores(self):

        weeks_scores = [self.get_scores_dict(self.get_reviews_by_date(weeks_ago(monday_last,i), weeks_ago(monday_this,i))) for i in range(4)]
        months_scores = [self.get_scores_dict(self.get_reviews_by_date(months_ago(monday_last_month, i),months_ago(monday_this,i))) for i in range(4)]
        all_scores = weeks_scores + months_scores

        scores_dict = {self.date_strings[i]:all_scores[i] for i in range(8)}

        return {
            category.capitalize():{
                date_string:{
                    'reviews':scores_dict[date_string][category.lower()]['total'],
                    'score':scores_dict[date_string][category.lower()]['average']
                } for date_string in self.date_strings
            } for category in self.score_categories
        }


class Review(models.Model):

    source = models.CharField(max_length=11)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    title = models.CharField(max_length=50, default='')
    date = models.DateField()
    visit_date = models.CharField(max_length=20, null=True)
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
        return str(self.title)

    def get_absolute_url(self):
        return reverse("rep_app:review_detail",kwargs={'pk':self.pk})

class Note(models.Model):

    restaurant = models.OneToOneField(Restaurant, on_delete=models.CASCADE)
    text = models.TextField(max_length=1000, default='')

    def __str__(self):
        return str(self.restaurant)





# class Comment(models.Model):
#
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     review = models.ForeignKey(Review, on_delete=models.CASCADE)
#     date = models.DateTimeField(auto_now_add=True)
#     text = models.TextField(max_length=1000)
#
#     def get_absolute_url(self):
#         return reverse("rep_app:review_detail",kwargs={'pk':self.review_id})

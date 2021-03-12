from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse, reverse_lazy
from django.views.generic import View, TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView

from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required

from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail

from rep_app import models
from rep_app.models import Manager, OpsDirector, Restaurant, Review, Note

from datetime import date, time, datetime, timedelta
from statistics import mean

from rep_app.restaurant_list import restaurant_list
restaurant_list = list(restaurant_list.keys())

from rep_app.emails import AppEmail, NoteNotification

# Date Variables
# today = date.today()
today = date.today()-timedelta(365)
monday_this = today - timedelta(today.weekday())
monday_last = monday_this - timedelta(7)

def my_mean(values):
    return round(mean(values),1) if values else 0

def my_divide(x,y):
    return x/y if y != 0 else 0

def get_restaurant_stats(reviews):

    review_scores = [
        {
            'restaurant':getattr(review,'restaurant'),
            'total':getattr(review,'score'),
            'food':getattr(review,'food'),
            'service':getattr(review,'service'),
            'value':getattr(review,'value'),
            'ambience':getattr(review,'ambience'),
            'submitted':getattr(review, 'reviewed')
        } for review in reviews
    ]

    categories = ['total','food','service','ambience','value']

    restaurant_stats = {
        restaurant: {
            'scores': {
                category:{
                    'total': len([review[category] for review in review_scores if review['restaurant'] == restaurant and review[category] > 0]),
                    'average': my_mean([review[category] for review in review_scores if review['restaurant'] == restaurant and review[category] > 0])
                } for category in categories
            },
            'submissions': {
                'submitted_reviews': len([review['total'] for review in review_scores if review['restaurant'] == restaurant and review['submitted'] and review['total'] < 4]),
                'unsubmitted_reviews': len([review['total'] for review in review_scores if review['restaurant'] == restaurant and not review['submitted'] and review['total'] < 4]),
                'submitted_p': round(my_divide(len([review['total'] for review in review_scores if review['restaurant'] == restaurant and review['submitted'] and review['total'] < 4]), len([review['total'] for review in review_scores if review['restaurant'] == restaurant and review['total'] < 4]))*100),
            },
            'below_4': {
                'reviews_below_4': len([review['total'] for review in review_scores if review['restaurant'] == restaurant and review['total'] < 4]),
                'reviews_below_4_p': round(my_divide(len([review['total'] for review in review_scores if review['restaurant'] == restaurant and review['total'] < 4]), len([review['total'] for review in review_scores if review['restaurant'] == restaurant]))*100),
            }
        } for restaurant in restaurant_list
    }

    return restaurant_stats

def get_restaurant_scores(reviews):

    review_scores = [
        {
            'restaurant':getattr(review,'restaurant'),
            'total':getattr(review,'score'),
            'food':getattr(review,'food'),
            'service':getattr(review,'service'),
            'value':getattr(review,'value'),
            'ambience':getattr(review,'ambience'),
        } for review in reviews
    ]

    categories = ['total','food','service','value','ambience']

    restaurant_scores = {
        restaurant:{
            category: {
                'total': len([review[category] for review in review_scores if review['restaurant'] == restaurant and review[category] > 0]),
                'average': my_mean([review[category] for review in review_scores if review['restaurant'] == restaurant and review[category] > 0])
            } for category in categories
        } for restaurant in restaurant_list
    }

    return restaurant_scores

# Create your views here.

def test_view(request):

    restaurants = Restaurant.objects.all()
    notes = Note.objects.all()
    context = {'restaurants':restaurants, 'notes':notes}

    return render(request, 'rep_app/test.html', context)

@login_required
def home_view(request):

    restaurants = Restaurant.objects.all()
    reviews = Review.objects.filter(date__lt = monday_this, date__gte = monday_last).order_by('score', 'restaurant')

    # If user is manager or staff, filter reviews by unsubmitted and below 4
    # If user is manager, also filter reviews by restaurant

    try:
        reviews = reviews.filter(reviewed = False, score__lt = 4, restaurant = request.user.manager.restaurant_set.first()) # If user is manager
    except ObjectDoesNotExist:
        if request.user.is_staff:
            reviews = reviews.filter(reviewed = False, score__lt = 4) # If user is staff
        else:
            pass # If user isn't manager or staff

    context = {'restaurants':restaurants,'reviews':reviews}

    return render(request, 'rep_app/home_page.html', context)

@login_required
def reviews_view(request):

    restaurants = Restaurant.objects.all()
    reviews = Review.objects.filter(date__lt = monday_this, date__gte = monday_last).order_by('score', 'restaurant')

    # If user is manager, filter reviews by restaurant
    try:
        reviews = reviews.filter(restaurant = request.user.manager.restaurant_set.first())
    except ObjectDoesNotExist:
        pass

    context = {'reviews':reviews,'restaurants':restaurants}

    return render(request, 'rep_app/reviews.html', context)

@login_required
def scores_view(request):

    restaurants = Restaurant.objects.all()
    context = {'restaurants':restaurants}

    return render(request, 'rep_app/scores.html', context)

# @login_required
# def scores_view_old(request):
#
#     start = datetime.now()
#
#     monday_this = date.today() - timedelta(365)
#
#     weeks_scores = [get_restaurant_scores(Review.objects.filter(date__lt = monday_this, date__gte = (monday_this - timedelta(7) - timedelta(7)*i)).order_by('score', 'restaurant')) for i in range(4)]
#     months_scores = [get_restaurant_scores(Review.objects.filter(date__lt = monday_this, date__gte = (monday_this - timedelta(30) - timedelta(30)*i)).order_by('score', 'restaurant')) for i in range(4)]
#     all_scores = weeks_scores + months_scores
#
#     duration_strings = ['week', 'month']
#     period_strings = ['last','two','three','four']
#     date_strings = [period + '_' + duration + 's' if period != 'last' else period + '_' + duration for duration in duration_strings for period in period_strings]
#     categories = ['Total','Food','Service','Value','Ambience']
#
#     scores_dict = {date_strings[i]:all_scores[i] for i in range(8)}
#     stats = {
#         restaurant:{
#             category.capitalize():{
#                 date_string:{
#                     'reviews':scores_dict[date_string][restaurant]['total_' + category.lower()],
#                     'score':scores_dict[date_string][restaurant]['average_' + category.lower()]
#                 } for date_string in date_strings
#             } for category in categories
#         } for restaurant in restaurant_list
#     }
#
#     context = {
#         'restaurant_list':restaurant_list,
#         'stats':stats,
#         'date_strings':date_strings,
#         'categories':categories,
#     }
#
#     return render(request, 'rep_app/scores.html', context)

@login_required
def submit_review(request, review_id):

    if request.method == "POST":
        review = get_object_or_404(Review, pk=review_id)
        review.comment = request.POST['comment']
        review.reviewed = True
        review.save()

    return home_page(request)

@login_required
def update_note(request, note_id):

    if request.method == "POST":

        note = get_object_or_404(Note, pk=note_id)
        note.text = request.POST['note']
        note.save()

        manager = note.restaurant.manager.user.first_name
        restaurant = note.restaurant.name
        app_url = 'http://127.0.0.1:8000/'
        email_note = NoteNotification(restaurant, manager, note.text, app_url)

        subject = restaurant + ' has a new note'
        recipient = 'domgunewardena@gmail.com'
        html = email_note.html
        text = email_note.text

        email = AppEmail(subject, recipient, html, text)

        email.send()

    return reviews_view(request)


# User Login Views

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('home_page'))

def register(request):

    registered = False

    if request.method == "POST":
        user_form = UserForm(data=request.POST)

        if user_form.is_valid():

            user = user_form.save()
            user.set_password(user.password)
            user.save()

            registered = True

        else:
            print(user_form.errors)
    else:
        user_form = UserForm()

    context = {
        'user_form':user_form,
        'registered':registered
    }

    return render(request,'registration.html',context)

def user_login(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username,password=password)

        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('home_page'))

            else:
                return HttpReponse('ACCOUNT NOT ACTIVE')
        else:
            print('Someone tried to login and failed!')
            print('Username: {} and password {}'.format(username,password))
            return HttpResponse('Invalid login details supplied!')
    else:
        return render(request,'rep_app/login.html',{})

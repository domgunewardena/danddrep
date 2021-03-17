from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse, reverse_lazy
from django.views.generic import View, TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView

from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required

from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail

from rep_app.models import Manager, OpsDirector, Restaurant, Review, Note
from rep_app.emails import AppEmail, NoteNotification

from datetime import date, time, datetime, timedelta

# Date Variables

today = date.today()
today = date.today()-timedelta(365)
monday_this = today - timedelta(today.weekday())
monday_last = monday_this - timedelta(7)

# Filtering functions

def filter_restaurants(request):

    try:
        restaurants = request.user.manager.restaurant_set.all()
    except ObjectDoesNotExist:
        try:
            restaurants = request.user.opsdirector.restaurant_set.all()
        except:
            restaurants = Restaurant.objects.all()

    return restaurants

def filter_reviews_by_restaurant(request,reviews):

    try:
        reviews = reviews.filter(restaurant = request.user.manager.restaurant_set.first())
    except ObjectDoesNotExist:
        try:
            reviews = reviews.filter(restaurant__in = request.user.manager.restaurant_set.all())
        except ObjectDoesNotExist:
            pass

    return reviews

def filter_reviews_by_submitted(request,reviews):

    try:
        request.user.manager
        reviews = reviews.filter(reviewed = False)
    except ObjectDoesNotExist:
        if request.user.is_staff:
            reviews = reviews.filter(reviewed = False)
        else:
            pass

    return reviews


# Create your views here.

def test_view(request):

    restaurants = Restaurant.objects.all()
    # notes = Note.objects.all()
    context = {'restaurants':restaurants}

    return render(request, 'rep_app/test.html', context)

@login_required
def home_view(request):

    reviews = Review.objects.filter(
        date__lt = monday_this,
        date__gte = monday_last,
        score__lt = 4
    ).order_by('score', 'restaurant')

    restaurants = filter_restaurants(request)
    reviews = filter_reviews_by_restaurant(request,reviews)
    reviews = filter_reviews_by_submitted(request,reviews)

    context = {'restaurants':restaurants,'reviews':reviews}

    return render(request, 'rep_app/home_page.html', context)

@login_required
def reviews_view(request):

    reviews = Review.objects.filter(
        date__lt = monday_this,
        date__gte = monday_last
    ).order_by('score', 'restaurant')

    restaurants = filter_restaurants(request)
    reviews = filter_reviews_by_restaurant(request,reviews)

    context = {'reviews':reviews,'restaurants':restaurants}

    return render(request, 'rep_app/reviews.html', context)

@login_required
def scores_view(request):

    restaurants = filter_restaurants(request)

    context = {'restaurants':restaurants}

    return render(request, 'rep_app/scores.html', context)

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
    return HttpResponseRedirect(reverse('rep_app:home_page'))

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
                return HttpResponseRedirect(reverse('rep_app:home_page'))

            else:
                return HttpReponse('ACCOUNT NOT ACTIVE')
        else:
            print('Someone tried to login and failed!')
            print('Username: {} and password {}'.format(username,password))
            return HttpResponse('Invalid login details supplied!')
    else:
        return render(request,'rep_app/login.html',{})

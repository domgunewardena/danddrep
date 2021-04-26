from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse, reverse_lazy
from django.views.generic import View, TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView

from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required

from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail

from rep_app.models import Manager, OpsDirector, Restaurant, Review, Note, Tag
from rep_app.emails import AppEmail, NoteNotification, NudgeNotification, SubmittedNotification, ReviewsNotification

from datetime import date, time, datetime, timedelta

# Date Variables

today = date.today()
monday_this = today - timedelta(today.weekday())
monday_last = monday_this - timedelta(7)

# App URL

app_url = 'http://127.0.0.1:8000/'

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
            reviews = reviews.filter(restaurant__in = request.user.opsdirector.restaurant_set.all())
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

def filter_reviews_by_text(reviews):

    return reviews.exclude(text = '')


# Create your views here.

def test_view(request):

    restaurants = Restaurant.objects.all()
    context = {'restaurants':restaurants}

    # reviews = Review.objects.filter(date__gte=today)
    # context = {'reviews':reviews}

    # notes = Note.objects.all()
    # context = {'restaurants':restaurants}

    return render(request, 'rep_app/test.html', context)

@login_required
def home_view(request):

    reviews = Review.objects.filter(
        date__lt = monday_this,
        date__gte = monday_last,
        score__lt = 4,
        tagged = False,
    ).order_by('score', 'restaurant')

    restaurants = filter_restaurants(request)
    reviews = filter_reviews_by_restaurant(request,reviews)
    reviews = filter_reviews_by_submitted(request,reviews)
    reviews = filter_reviews_by_text(reviews)
    tags = Tag.objects.all().order_by('text')

    reviews = reviews[:100]

    context = {
        'restaurants':restaurants,
        'reviews':reviews,
        'tags':tags
    }

    try:
        request.user.manager
    except ObjectDoesNotExist:
        try:
            request.user.opsdirector
        except ObjectDoesNotExist:
            if not request.user.is_staff:
                context = {'restaurants':restaurants}

    return render(request, 'rep_app/home_page.html', context)

@login_required
def reviews_view(request):

    reviews = Review.objects.filter(
        date__lt = monday_this,
        date__gte = monday_last
    ).order_by('score', 'restaurant')

    restaurants = filter_restaurants(request)
    reviews = filter_reviews_by_restaurant(request,reviews)
    tags = Tag.objects.all().order_by('text')

    context = {
        'reviews':reviews,
        'restaurants':restaurants,
        'tags':tags
    }

    return render(request, 'rep_app/reviews.html', context)

@login_required
def scores_view(request):

    restaurants = filter_restaurants(request)

    context = {'restaurants':restaurants}

    return render(request, 'rep_app/scores.html', context)

@login_required
def tag_review(request, review_id):

    if request.method == "POST":

        review = get_object_or_404(Review, pk=review_id)
        tag_objects = Tag.objects.all()

        for tag_object in tag_objects:
            is_tag = request.POST.get(tag_object.text, False)
            if is_tag:
                review.tags.add(tag_object)
            else:
                review.tags.remove(tag_object)

        review.tagged = True
        review.save()

    return redirect('rep_app:review_detail', pk=review_id)

class ReviewDetailView(DetailView):
    model = Review

@login_required
def submit_review(request, review_id):

    if request.method == "POST":

        review = get_object_or_404(Review, pk=review_id)
        review.comment = request.POST['comment']
        review.reviewed = True
        review.save()

        ops_director = review.restaurant.opsdirector
        no_of_unsubmitted_reviews = sum([len(restaurant.get_last_week_unsubmitted_reviews()) for restaurant in ops_director.restaurant_set.all()])

        if no_of_unsubmitted_reviews == 0:

            subject = 'Your reviews have been submitted'
            recipient = 'domgunewardena@gmail.com'
            email_text = SubmittedNotification(ops_director.user.first_name, app_url)
            html = email_text.html
            text = email_text.text

            email = AppEmail(subject, recipient, html, text)
            email.send()

        no_of_unsubmitted_reviews = sum([len(restaurant.get_last_week_unsubmitted_reviews()) for restaurant in Restaurant.objects.all()])

        if no_of_unsubmitted_reviews == 0:

            subject = 'All reviews have been submitted'
            recipient = 'domgunewardena@gmail.com'
            email_text = SubmittedNotification('Annabel', app_url)
            html = email_text.html
            text = email_text.text

            email = AppEmail(subject, recipient, html, text)
            email.send()

    return redirect('rep_app:home_page')

@login_required
def update_note(request, note_id):

    if request.method == "POST":

        note = get_object_or_404(Note, pk=note_id)
        note.text = request.POST['note']
        note.save()

        if request.POST['note'] != '':

            manager = note.restaurant.manager.user.first_name
            restaurant = note.restaurant.name

            subject = restaurant + ' has a new note'
            # recipient = 'domgunewardena@gmail.com'
            recipient = 'annabels@danddlondon.com'
            email_text = NoteNotification(restaurant, manager, note.text, app_url)
            html = email_text.html
            text = email_text.text

            email = AppEmail(subject, recipient, html, text)
            email.send()

    return redirect('rep_app:reviews')

@login_required
def nudge_view(request):

    restaurants = Restaurant.objects.all()

    for restaurant in restaurants:

        if len(restaurant.get_last_week_unsubmitted_reviews()) > 0:

            restaurant_name = restaurant.name
            manager = restaurant.manager.user.first_name

            subject = 'Annabel has nudged you'
            # recipient = 'domgunewardena@gmail.com'
            recipient = 'annabels@danddlondon.com'
            email_text = NudgeNotification(restaurant_name, manager, app_url)
            html = email_text.html
            text = email_text.text

            email = AppEmail(subject, recipient, html, text)
            email.send()

    return redirect('home_page')

# User Login Views

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('rep_app:home_page'))

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

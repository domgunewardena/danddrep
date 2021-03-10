"""rep_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path, include
from rep_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home_view,name='home_page'),
    path('reviews/',views.reviews_view,name='reviews'),
    path('scores/',views.scores_view,name='scores'),
    path('test/',views.test_view,name='test_view'),
    re_path('submit_review/', include('rep_app.urls', namespace='submit')),
    re_path('update_note/', include('rep_app.urls', namespace='rep_app')),
    re_path(r'login/',views.user_login,name='user_login'),
    re_path(r'logout/$',views.user_logout,name='logout'),

]

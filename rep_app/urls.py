from rep_app import views
from django.urls import path, re_path, include

app_name = 'rep_app'

urlpatterns = [
    path('submit_review/<int:review_id>/',views.submit_review, name='submit_review'),
    path('update_note/<int:note_id>/',views.update_note, name='update_note'),
    # path('', views.index, name='index'),
]

from rep_app import views
from django.urls import path

app_name = 'rep_app'

urlpatterns = [
    path('',views.home_view,name='home_page'),
    path('reviews/',views.reviews_view,name='reviews'),
    path('scores/',views.scores_view,name='scores'),
    path('test/',views.test_view,name='test_view'),
    path('submit_review/<int:review_id>/',views.submit_review, name='submit_review'),
    path('update_note/<int:note_id>/',views.update_note, name='update_note'),
    path('nudge/',views.nudge_view,name='nudge'),
]

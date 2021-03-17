from rep_app import views
from django.urls import path, re_path, include

app_name = 'rep_app'

urlpatterns = [
    path('submit_review/<int:review_id>/',views.submit_review, name='submit_review'),
    path('update_note/<int:note_id>/',views.update_note, name='update_note'),
    # path('', views.index, name='index'),
    path('',views.home_view,name='home_page'),
    path('reviews/',views.reviews_view,name='reviews'),
    path('scores/',views.scores_view,name='scores'),
    path('test/',views.test_view,name='test_view'),
    # re_path('submit_review/', include('rep_app.urls', namespace='submit')),
    # re_path('update_note/', include('rep_app.urls', namespace='rep_app')),
]

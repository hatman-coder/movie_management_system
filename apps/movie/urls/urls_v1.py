from django.urls import path
from ..views.views_v1 import *

urlpatterns = [

    # ------------------------------ Movie API ----------------------------- #
    path('create-movie/', MovieViewSet. as_view({'post': 'create_movie'}), name='create_movie'),
    path('my-movies/', MovieViewSet.as_view({'get': 'my_movies'}), name='my_movies'),
    path('movies_list/', MovieViewSet.as_view({'get': 'movies_list'}), name='movies_list'),
    path('retrieve-movie/<str:id>/', MovieViewSet.as_view({'get': 'retrieve_movie'}), name='retrieve_movie'),
    path('update-movie/<str:id>/', MovieViewSet.as_view({'put': 'update_movie'}), name='update_movie'),

    # ------------------------------ Rating API ----------------------------- #
    path('submit-rating/', RatingViewSet.as_view({'post': 'submit_rating'}), name='submit_rating'),
    path('update-rating/<str:id>/', RatingViewSet.as_view({'put': 'update_rating'}), name='update_rating'),
    path('rated-movie-list/', RatingViewSet.as_view({'get': 'rated_movie_list'}), name='rated_movie_list'),

    # ------------------------------ Report API ----------------------------- #
    path('report-movie/', ReportedMovieViewSet.as_view({'post': 'report_movie'}), name='report_movie'),
    path('reported-movie-list/', ReportedMovieViewSet.as_view({'get': 'reported_movie_list'}), name='reported_movie_list'),
    path('review-report/<str:id>/', ReportedMovieViewSet.as_view({'put': 'review_report'}), name='review_report')

]
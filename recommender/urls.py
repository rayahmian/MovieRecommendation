from django.urls import path
from . import views

urlpatterns = [
    path('recommender/', views.recommend_movies, name='recommend_movies'),
    path('recommendations/<str:encoded_recommendation_data>/', views.show_recommendations, name='show_recommendations'),
]

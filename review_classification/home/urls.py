from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="home"),
    path('reviews/<str:app_id>/', views.review, name="reviews")
]

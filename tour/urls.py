from django.urls import path
from . import views

urlpatterns = [
    path('tour/',views.tour_list,name='tour_list'),
    path('recommend/', views.tour_recommendation,name="tour_recommendation")
]
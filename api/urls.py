from django.urls import path
from api import api_views

urlpatterns = [
    path('venues', api_views.venue_list),
    path('venues/<str:code>', api_views.venue_detail),
    path('hku-members', api_views.hku_member_list),
    path('hku-members/<str:hku_id>', api_views.hku_member_detail),
    path('visits', api_views.visit_list),
    path('visits/<int:visit_id>', api_views.visit_detail),
]

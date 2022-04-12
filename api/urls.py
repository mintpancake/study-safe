from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from api import api_views

urlpatterns = [
    path('token-auth', obtain_auth_token, name='api_token_auth'),
    path('venues', api_views.VenueList.as_view(), name='venue_list'),
    path('venues/<str:pk>', api_views.VenueDetail.as_view(), name='venue_detail'),
    path('hku-members', api_views.HkuMemberList.as_view(), name='hku_member_list'),
    path('hku-members/<str:pk>', api_views.HkuMemberDetail.as_view(), name='hku_member_detail'),
    path('visits', api_views.VisitList.as_view(), name='visit_list'),
    path('visits/<int:visit_id>', api_views.VisitDetail.as_view(), name='visit_detail'),
    path('visited-by/<str:hku_id>/<str:date>', api_views.VisitBy.as_view(), name='info'),
    path('close-contact/<str:hku_id>/<str:date>', api_views.CloseContact.as_view(), name='info'),
]

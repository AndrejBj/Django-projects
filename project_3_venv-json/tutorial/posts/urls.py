#dodajemo ovaj fajl urls.py

from django.urls import path
from posts import views
from rest_framework.urlpatterns import format_suffix_patterns      #format_suffix_patterns sluzi da mozemo putanje da pravimo na slobodniji nacin

urlpatterns = format_suffix_patterns([
    path('posts/',views.PostList.as_view(),name='post-list'),
    path('posts/<int:pk>/',views.PostDetail.as_view(),name='post-detail'),    #path u linku za id posle posts, npr posts/1, posts/2...
    path('users/',views.UserList.as_view(),name='user-list'),                 #ubacujemo taj i sledece path za usere
    path('users/<int:pk>/',views.UserDetail.as_view(),name='user-detail'),
    path('',views.api_root),                                                  #ubaceno path za api_root (strana na aplikaciji za navigaciju), gde imamo api_root funkciju u views
])
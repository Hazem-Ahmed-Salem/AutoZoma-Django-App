from django.urls import path 
from .views import (login_view ,RegisterView ,logout_view ,ProfileView ,profile_others_view)


urlpatterns = [
    path('login/' , login_view, name='login'),
    path('register/' , RegisterView.as_view(), name='register'),
    path('profile/' , ProfileView.as_view(), name='profile'),
    path('profile/<str:id>/', profile_others_view , name='profile_other' ),
    path('logout/' , logout_view, name='logout'),
    

]
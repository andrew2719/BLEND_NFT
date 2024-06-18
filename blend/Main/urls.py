from . import views
from django.contrib import admin
from django.urls import path

urlpatterns = [
    # test
    path('test_api/',views.test_api,name="test_api"),
    # main
    path('',views.index,name="index"),
    path('register/',views.register,name="register"), 
    path('login/',views.login_,name="login"),
    path('logout/',views.logout_,name="logout"),
    path('home/',views.home,name="home"),
]
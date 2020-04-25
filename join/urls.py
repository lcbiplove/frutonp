from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup, name="signup"),
    path('login/', views.login, name="login"),
    path('logout/', views.logout, name="logout"),
    path('aj_ch_em/', views.ajax_email, name="ajax_email"),
    path('check/', views.check, name="check"),

] 

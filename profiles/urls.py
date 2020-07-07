from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name="profile"),
    path('<int:id>/', views.index, name="profile"),
    path('profile-post/', views.profilePost, name="profilePost"),
    path('<int:id>/profile-post/', views.profilePost, name="profilePost"),
    path('edit/', views.changePhoneLocDesc, name="changePhoneLocDesc"),
    path('upload-pp/', views.uploadPP, name="uploadPP"),
    path('<int:id>/upload-pp/', views.uploadPP, name="uploadPP"),
    path('delete-pp/', views.deletePP, name="deletePP"),
    path('<int:id>/delete-pp/', views.deletePP, name="deletePP"),
    path('change-name/', views.changeName, name="changeName"),
    path('change-phone/', views.changePhone, name="changePhone"),
    path('change-password/', views.changePassword, name="changePassword"),
] 

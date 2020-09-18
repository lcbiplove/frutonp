from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup, name="signup"),
    path('login/', views.login, name="login"),
    path('logout/', views.logout, name="logout"),
    path('aj_ch_em/', views.ajax_email, name="ajax_email"),
    path('check/', views.check, name="check"),
    path('activate/<slug:uidb64>/<slug:token>/', views.activate, name='activate'),
    path('send-activation-email/', views.sendActivationEmail, name='sendActivationEmail'),
    path('password/reset/', views.passwordReset, name='passwordReset'),
    path('password/reset/confirm/<slug:uidb64>/<slug:token>/', views.passwordResetConfirm, name='passwordResetConfirm'),
] 

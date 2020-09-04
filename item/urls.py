from django.urls import path
from . import views

urlpatterns = [
    path('vegetables/', views.veg, name="itemVegetable"),
    path('vegetable/<str:veg_name>/', views.vegName, name="itemVegetableName"),
    path('fruits/', views.fruit, name="itemFruit"),
    path('fruit/<str:fruit_name>/', views.fruitName, name="itemFruitName"),
] 

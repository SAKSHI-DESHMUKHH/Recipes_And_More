from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('photo/<str:pk>/', views.viewFood, name='food'),
    path('add/', views.addFood, name='add'),
    path('update/<str:pk>/', views.updateRecipes, name='update_recipes'),
    path('delete/<str:pk>/', views.deleteRecipes, name='delete_recipes'),
]
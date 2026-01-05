from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('create-category/', views.create_category, name='create_category'),
    path('category/<slug:slug>/', views.category_detail, name='category_detail'),
    
    
    path('category/<slug:slug>/create/', views.create_post, name='create_post'),
]
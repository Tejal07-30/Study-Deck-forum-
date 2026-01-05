from django.urls import path
from . import views

urlpatterns = [
    # Homepage
    path('', views.home, name='home'),
    # Thread List (The one you made earlier)
    path('category/<slug:slug>/', views.thread_list, name='thread_list'),
]
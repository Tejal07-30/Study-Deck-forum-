from django.urls import path
from .views import (
    home,
    category_detail,
    create_post,
    thread_detail,
    add_reply,
)

urlpatterns = [
    path('', home, name='home'),
    path('category/<slug:slug>/', category_detail, name='category_detail'),
    path('category/<slug:slug>/new/', create_post, name='create_post'),
    path('thread/<int:thread_id>/', thread_detail, name='thread_detail'),
    path('thread/<int:thread_id>/reply/', add_reply, name='add_reply'),
]

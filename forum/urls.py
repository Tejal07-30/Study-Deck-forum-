from django.urls import path
from django.shortcuts import render

from .views import (
    home,
    category_detail,
    create_post,
    thread_detail,
    add_reply,
    signup,
    user_login,
    admin_login,
    delete_reply,
    toggle_thread_lock,
    toggle_reply_upvote,
    report_reply,
    delete_thread,
    edit_reply,
)

urlpatterns = [
    # Landing page
    path("", lambda r: render(r, "registration/landing.html"), name="landing"),

    # Auth
    path("login/user/", user_login, name="user_login"),
    path("login/admin/", admin_login, name="admin_login"),
    path("signup/", signup, name="signup"),

    # Forum
    path("home/", home, name="home"),
    path("category/<slug:slug>/", category_detail, name="category_detail"),
    path("category/<slug:slug>/new/", create_post, name="create_post"),
    path("thread/<int:thread_id>/", thread_detail, name="thread_detail"),
    path("thread/<int:thread_id>/reply/", add_reply, name="add_reply"),

    # Permissions
    path("reply/<int:reply_id>/delete/", delete_reply, name="delete_reply"),
    path("thread/<int:thread_id>/lock/", toggle_thread_lock, name="toggle_thread_lock"),
    path('reply/<int:reply_id>/upvote/', toggle_reply_upvote, name='toggle_reply_upvote'),
    path('reply/<int:reply_id>/report/', report_reply, name='report_reply'),
    path('thread/<int:thread_id>/delete/', delete_thread, name='delete_thread'),
    path('reply/<int:reply_id>/edit/', edit_reply, name='edit_reply'),

]

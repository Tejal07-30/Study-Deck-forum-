from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from .models import Category, Thread, Reply


def home(request):
    categories = Category.objects.all()
    return render(request, 'forum/home.html', {
        'categories': categories
    })


def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    threads = Thread.objects.filter(category=category).order_by('-created_at')

    return render(request, 'forum/category_detail.html', {
        'category': category,
        'threads': threads
    })


@login_required
def create_post(request, slug):
    category = get_object_or_404(Category, slug=slug)

    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')

        Thread.objects.create(
            category=category,
            title=title,
            content=content,
            author=request.user
        )

        return redirect('category_detail', slug=slug)

    return render(request, 'forum/create_post.html', {
        'category': category
    })


def thread_detail(request, thread_id):
    thread = get_object_or_404(Thread, id=thread_id)
    replies = thread.replies.all().order_by('created_at')

    return render(request, 'forum/thread_detail.html', {
        'thread': thread,
        'replies': replies
    })


@login_required
def add_reply(request, thread_id):
    thread = get_object_or_404(Thread, id=thread_id)

    if request.method == 'POST':
        content = request.POST.get('content')

        Reply.objects.create(
            thread=thread,
            author=request.user,
            content=content
        )

    return redirect('thread_detail', thread_id=thread.id)

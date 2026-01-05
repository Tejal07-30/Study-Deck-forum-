from django.shortcuts import render, get_object_or_404
from .models import Category, Thread

# This is the view for the Homepage
def home(request):
    categories = Category.objects.all()
    return render(request, 'forum/home.html', {'categories': categories})

# This is the view for the Thread List (inside a category)
def thread_list(request, slug):
    category = get_object_or_404(Category, slug=slug)
    threads = category.threads.all()
    return render(request, 'forum/thread_list.html', {'category': category, 'threads': threads})
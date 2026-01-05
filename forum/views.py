from django.shortcuts import render, redirect, get_object_or_404
from django.utils.text import slugify
from .models import Category, Post

def home(request):
    categories = Category.objects.all()
    context = {'categories': categories}
    return render(request, 'forum/home.html', context)

def create_category(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        slug = slugify(name)
        Category.objects.create(name=name, description=description, slug=slug)
        return redirect('home')
    return render(request, 'forum/create_category.html')

def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    # Get all posts for this category, newest first
    posts = category.posts.all().order_by('-created_at')
    context = {'category': category, 'posts': posts}
    return render(request, 'forum/category_detail.html', context)

def create_post(request, slug):
    category = get_object_or_404(Category, slug=slug)
    
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        
        # Save the new post inside this specific category
        Post.objects.create(category=category, title=title, content=content)
        
        # Go back to the category page to see the new post
        return redirect('category_detail', slug=slug)
        
    return render(request, 'forum/create_post.html', {'category': category})
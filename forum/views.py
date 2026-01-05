from django.shortcuts import render, redirect, get_object_or_404
from django.utils.text import slugify
from .models import Category
from django.http import HttpResponse
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
    context = {'category': category}
    return render(request, 'forum/category_detail.html', context)
def clean_db(request):
    Category.objects.all().delete()
    return HttpResponse("<h1>Database Wiped Successfully. Go back to Home now.</h1>")
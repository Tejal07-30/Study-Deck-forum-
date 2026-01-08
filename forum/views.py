from django.shortcuts import render
from .models import Category, Thread
from django.shortcuts import render, get_object_or_404, redirect
from .forms import ReplyForm


def home(request):
    categories = Category.objects.prefetch_related("threads")
    return render(request, "forum/home.html", {
        "categories": categories
    })

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
def thread_detail(request, thread_id):
    thread = get_object_or_404(Thread, id=thread_id)

    if request.method == "POST":
        form = ReplyForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.thread = thread
            reply.author = request.user
            reply.save()
            return redirect("thread_detail", thread_id=thread.id)
    else:
        form = ReplyForm()

    return render(request, "forum/thread_detail.html", {
        "thread": thread,
        "form": form
    })


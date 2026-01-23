from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.http import HttpResponseForbidden
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from .models import Category, Thread, Reply
from django.contrib import messages
from django.contrib.auth.models import User
from .models import ReplyVote
from .models import ReplyReport



@login_required
def home(request):
    categories = Category.objects.all()
    return render(request, 'forum/home.html', {
        'categories': categories
    })

@login_required
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

@login_required
def thread_detail(request, thread_id):
    thread = get_object_or_404(Thread, id=thread_id)
    replies = thread.replies.select_related('author').prefetch_related('children')

    return render(request, 'forum/thread_detail.html', {
        'thread': thread,
        'replies': replies
    })



@login_required
def add_reply(request, thread_id):
    thread = get_object_or_404(Thread, id=thread_id)

    if thread.is_locked:
        return HttpResponse("This thread is locked.")

    if request.method == 'POST':
        content = request.POST.get('content')
        parent_id = request.POST.get('parent_id')

        parent = None
        if parent_id:
            parent = Reply.objects.get(id=parent_id)

        Reply.objects.create(
            thread=thread,
            author=request.user,
            content=content,
            parent=parent
        )

    return redirect('thread_detail', thread_id=thread.id)



def test_view(request):
    return HttpResponse("FORUM HIT")

def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")
    else:
        form = UserCreationForm()

    return render(request, "registration/signup.html", {"form": form})
def user_login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username=username, password=password)

        if user is not None and not user.is_staff:
            login(request, user)
            return redirect("home")
        else:
            return render(request, "registration/user_login.html", {
                "error": "Invalid user credentials"
            })

    return render(request, "registration/user_login.html")


def admin_login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username=username, password=password)

        if user is not None and user.is_staff:
            login(request, user)
            return redirect("/admin/")
        else:
            return render(request, "registration/admin_login.html", {
                "error": "Admin credentials required"
            })

    return render(request, "registration/admin_login.html")
@login_required
def delete_reply(request, reply_id):
    reply = get_object_or_404(Reply, id=reply_id)

    # permission check
    if request.user != reply.author and not request.user.is_superuser:
        return HttpResponseForbidden("You are not allowed to delete this reply.")

    thread_id = reply.thread.id
    reply.delete()
    return redirect('thread_detail', thread_id=thread_id)
    
@login_required
def edit_reply(request, reply_id):
    reply = get_object_or_404(Reply, id=reply_id)

    # Permission check
    if request.user != reply.author and not request.user.is_superuser:
        return HttpResponseForbidden("You cannot edit this reply.")

    if request.method == "POST":
        new_content = request.POST.get("content")
        reply.content = new_content
        reply.save()
        return redirect("thread_detail", thread_id=reply.thread.id)

    return render(request, "forum/edit_reply.html", {
        "reply": reply
    })

@login_required
def toggle_thread_lock(request, thread_id):
    if not request.user.is_superuser:
        return HttpResponse("Unauthorized", status=403)

    thread = get_object_or_404(Thread, id=thread_id)
    thread.is_locked = not thread.is_locked
    thread.save()

    return redirect('thread_detail', thread_id=thread.id)
@login_required
def toggle_reply_upvote(request, reply_id):
    reply = get_object_or_404(Reply, id=reply_id)

    vote = ReplyVote.objects.filter(reply=reply, user=request.user)

    if vote.exists():
        vote.delete()   # remove upvote
    else:
        ReplyVote.objects.create(reply=reply, user=request.user)

    return redirect('thread_detail', thread_id=reply.thread.id)
@login_required
def report_reply(request, reply_id):
    reply = get_object_or_404(Reply, id=reply_id)

    if request.method == "POST":
        reason = request.POST.get("reason")

        # Prevent duplicate reports
        if not ReplyReport.objects.filter(reply=reply, reported_by=request.user).exists():
            ReplyReport.objects.create(
                reply=reply,
                reported_by=request.user,
                reason=reason
            )

    return redirect('thread_detail', thread_id=reply.thread.id)
from django.http import HttpResponseForbidden

@login_required
def delete_thread(request, thread_id):
    thread = get_object_or_404(Thread, id=thread_id)

    # Permission check
    if request.user != thread.author and not request.user.is_superuser:
        return HttpResponseForbidden("You are not allowed to delete this thread.")

    category_slug = thread.category.slug
    thread.delete()

    return redirect('category_detail', slug=category_slug)

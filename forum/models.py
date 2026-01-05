from django.db import models
from django.contrib.auth.models import User
from base.models import Course

class Category(models.Model):
    # PDF Requirement: Name and unique slug for URL [cite: 70]
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

class Thread(models.Model):
    # PDF Requirement: Title, Content, Author, Timestamp [cite: 75]
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='threads')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='threads')
    
    # PDF Requirement: Contextual Linking (Course Tag) [cite: 76]
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # PDF Requirement: Likes [cite: 86]
    likes = models.ManyToManyField(User, related_name='liked_threads', blank=True)

    def total_likes(self):
        return self.likes.count()

    def __str__(self):
        return self.title

class Reply(models.Model):
    # PDF Requirement: Replies connected to threads [cite: 80]
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE, related_name='replies')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reply by {self.author} on {self.thread}"
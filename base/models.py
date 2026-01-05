from django.db import models

class Course(models.Model):
    # PDF Requirement: Course Code, Title, Department [cite: 52-55]
    code = models.CharField(max_length=20, unique=True, help_text="e.g., CS F111")
    title = models.CharField(max_length=200, help_text="e.g., Computer Programming")
    department = models.CharField(max_length=100, help_text="e.g., Computer Science")

    def __str__(self):
        return f"{self.code} - {self.title}"

class Resource(models.Model):
    # PDF Requirement: Resource Title, Type, Link [cite: 56-59]
    TYPE_CHOICES = [
        ('PDF', 'PDF'),
        ('VIDEO', 'Video'),
        ('LINK', 'Link'),
    ]
    
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='resources')
    title = models.CharField(max_length=200)
    resource_type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    link = models.URLField()

    def __str__(self):
        return self.title
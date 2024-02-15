# blog/models.py
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Blog(models.Model):
    CATEGORY_CHOICES = (
        ('Mental Health', 'Mental Health'),
        ('Heart Disease', 'Heart Disease'),
        ('Covid19', 'Covid19'),
        ('Immunization', 'Immunization'),
    )

    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='blog_images/')
    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES)
    summary = models.CharField(max_length=500)
    content = models.TextField()
    draft = models.BooleanField(default=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def get_summary(self):
        # Function to get truncated summary
        words = self.summary.split()
        if len(words) > 15:
            return ' '.join(words[:15]) + '...'
        else:
            return self.summary

    def publish(self):
        self.draft = False
        self.save()

    def __str__(self):
        return self.title

from django.db import models

from django.contrib.auth.models import User



STATUS_CHOICES = (
    (0, "Draft"),
    (1, "Publish"),
)


class Post(models.Model):
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    updated_on = models.DateTimeField(auto_now=True)
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS_CHOICES, default=0)



class Meta:
    ordering = ['-created_on']


def __str__(self):
    return self.title


class Counter(models.Model):
    name = models.CharField(max_length=100, unique=True)
    value = models.IntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'counter'

    def __str__(self):
        return f"{self.name}: {self.value}"
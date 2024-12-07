from django.db import models


class Category(models.Model):
    title = models.CharField(max_length=150, unique=True)

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title


class Gallery(models.Model):
    category = models.ForeignKey(Category, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images')
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.image.url


class Contact(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.name}"


class InstagramPost(models.Model):
    image_url = models.URLField()
    caption = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField()
    category = models.ForeignKey('Category', on_delete=models.CASCADE, default=None)

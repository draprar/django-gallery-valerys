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
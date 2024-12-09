from django.contrib import admin

from .models import Category, Gallery, InstagramPost

admin.site.register(Category)
admin.site.register(Gallery)
admin.site.register(InstagramPost)

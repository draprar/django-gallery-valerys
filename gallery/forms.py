from django import forms
from .models import Category, Gallery


class GalleryForm(forms.ModelForm):
    class Meta:
        model = Gallery
        fields = "__all__"


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = "__all__"

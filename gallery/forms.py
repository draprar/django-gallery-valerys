from django import forms
from .models import Category, Gallery, Contact


class GalleryForm(forms.ModelForm):
    class Meta:
        model = Gallery
        fields = ['category', 'image', 'title', 'description', 'created_at']


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['title']


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Your Email'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Your Message', 'rows': 5}),
        }

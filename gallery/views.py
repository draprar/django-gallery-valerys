from django.views import generic
from django.urls import reverse_lazy
from .models import Category, Gallery
from .forms import GalleryForm, CategoryForm


class Home(generic.ListView):
    model = Gallery
    template_name = 'home.html'
    queryset = Gallery.objects.all()

    def get_queryset(self):
        queryset = super().get_queryset()
        category = self.request.GET.get('category', None)
        if category:
            queryset = queryset.filter(category__title=category)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = self.request.GET.get('category', None)
        context['selected_category'] = category if category else "All"
        return context

class UploadImage(generic.CreateView):
    model = Gallery
    template_name = 'upload-image.html'
    form_class = GalleryForm
    success_url = reverse_lazy('home')


class CreateCategory(generic.CreateView):
    model = Category
    template_name = 'create-category.html'
    form_class = CategoryForm
    success_url = reverse_lazy('upload-image')
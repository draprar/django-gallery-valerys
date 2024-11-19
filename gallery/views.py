from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.views import generic, View
from django.urls import reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404
from .models import Category, Gallery
from .forms import GalleryForm, CategoryForm, ContactForm
from django.contrib.auth.mixins import UserPassesTestMixin


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
        context['categories'] = Category.objects.all()
        return context


class AdminOnlyMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff

    def handle_no_permission(self):
        messages.error(self.request, "You do not have permission to perform this action.")
        return redirect('home')


class UploadImage(AdminOnlyMixin, generic.CreateView):
    model = Gallery
    template_name = 'upload-image.html'
    form_class = GalleryForm
    success_url = reverse_lazy('home')


class DeleteImage(AdminOnlyMixin, generic.DeleteView):
    model = Gallery
    template_name = 'delete-image.html'
    success_url = reverse_lazy('home')

    def get_object(self, queryset=None):
        return get_object_or_404(Gallery, pk=self.kwargs['pk'])


class CreateCategory(AdminOnlyMixin, generic.CreateView):
    model = Category
    template_name = 'create-category.html'
    form_class = CategoryForm
    success_url = reverse_lazy('upload-image')


class ContactView(View):
    template_name = 'contact.html'

    def get(self, request):
        form = ContactForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = ContactForm(request.POST)
        if form.is_valid():
            # Save to the database
            form.save()

            # Send email notification (configure settings in settings.py)
            send_mail(
                'New Contact Form Submission',
                f"Message from {form.cleaned_data['name']} ({form.cleaned_data['email']}):\n\n{form.cleaned_data['message']}",
                settings.DEFAULT_FROM_EMAIL,
                [settings.EMAIL_HOST_USER],
            )

            messages.success(request, 'Your message has been sent successfully!')
            return redirect('contact')
        return render(request, self.template_name, {'form': form})

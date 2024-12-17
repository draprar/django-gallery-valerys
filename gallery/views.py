from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail, BadHeaderError
from django.views import generic, View
from django.urls import reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404
from .models import Category, Gallery, InstagramPost
from .forms import GalleryForm, CategoryForm, ContactForm
from django.contrib.auth.mixins import UserPassesTestMixin


class Home(generic.ListView):
    """
    Displays the homepage with a list of Gallery images.
    Allows filtering by category using GET parameters.
    """

    model = Gallery
    template_name = 'home.html'
    queryset = Gallery.objects.all()

    def get_queryset(self):
        """
        Optionally filters images by the selected category.
        """
        queryset = super().get_queryset()
        category = self.request.GET.get('category', None)
        if category:
            queryset = queryset.filter(category__title=category)
        return queryset

    def get_context_data(self, **kwargs):
        """
        Adds categories and Instagram posts to the context.
        """
        context = super().get_context_data(**kwargs)
        category = self.request.GET.get('category', None)
        context['selected_category'] = category if category else "All"
        context['categories'] = Category.objects.all()

        # Include Instagram posts in context
        if category:
            context['instagram_posts'] = InstagramPost.objects.filter(category__title=category).order_by('-created_at')
        else:
            context['instagram_posts'] = InstagramPost.objects.all().order_by('-created_at')

        return context


class AdminOnlyMixin(UserPassesTestMixin):
    """
    Mixin to restrict access to admin-only views.
    """
    def test_func(self):
        return self.request.user.is_staff

    def handle_no_permission(self):
        """
        Redirects unauthorized users to the home page with an error message.
        """
        messages.error(self.request, "You do not have permission to perform this action.")
        return redirect('home')


class UploadImage(AdminOnlyMixin, generic.CreateView):
    """
    View for admins to upload a new image to the gallery.
    """
    model = Gallery
    template_name = 'upload-image.html'
    form_class = GalleryForm
    success_url = reverse_lazy('home')


class DeleteImage(AdminOnlyMixin, generic.DeleteView):
    """
    View for admins to delete an existing image from the gallery.
    """
    model = Gallery
    template_name = 'delete-image.html'
    success_url = reverse_lazy('home')

    def get_object(self, queryset=None):
        """
        Retrieves the image object based on the primary key.
        """
        return get_object_or_404(Gallery, pk=self.kwargs['pk'])


class CreateCategory(AdminOnlyMixin, generic.CreateView):
    """
    View for admins to create a new image category.
    """
    model = Category
    template_name = 'create-category.html'
    form_class = CategoryForm
    success_url = reverse_lazy('upload-image')


class ContactView(View):
    """
    Handles displaying and processing of the contact form.
    """

    template_name = 'contact.html'

    def get(self, request):
        """
        Renders an empty contact form.
        """
        form = ContactForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        """
        Processes the submitted contact form.
        Sends an email and saves the data to the database.
        """
        form = ContactForm(request.POST)
        if form.is_valid():
            try:
                # Save to the database
                form.save()

                # Send email notification
                send_mail(
                    'New Contact Form Submission',
                    f"Message from {form.cleaned_data['name']} ({form.cleaned_data['email']}):\n\n{form.cleaned_data['message']}",
                    settings.DEFAULT_FROM_EMAIL,
                    [settings.EMAIL_HOST_USER],
                )
                messages.success(request, 'Your message has been sent successfully!')
            except BadHeaderError:
                messages.error(request, "Invalid header found.")
            except Exception as e:
                messages.error(request, "An error occurred while sending the email. Please try again later.")
            return redirect('contact')
        return render(request, self.template_name, {'form': form})

import pytest
import tempfile
from django.test import override_settings
from django.urls import reverse
from django.contrib.auth.models import User
from gallery.models import Category, Gallery, InstagramPost, Contact
from django.core import mail
from django.core.files.uploadedfile import SimpleUploadedFile


@pytest.mark.django_db
class TestViews:
    def test_home_view(self, client):
        category = Category.objects.create(title="Nature")
        gallery_item = Gallery.objects.create(category=category, image="images/test.jpg")
        response = client.get(reverse('home'))

        assert response.status_code == 200
        assert 'categories' in response.context
        assert 'selected_category' in response.context
        assert 'instagram_posts' in response.context
        assert gallery_item in response.context['object_list']

    def test_home_view_filtered_by_category(self, client):
        category = Category.objects.create(title="Nature")
        other_category = Category.objects.create(title="Animals")
        Gallery.objects.create(category=category, image="images/nature.jpg")
        Gallery.objects.create(category=other_category, image="images/animals.jpg")

        response = client.get(reverse('home') + '?category=Nature')

        assert response.status_code == 200
        assert len(response.context['object_list']) == 1
        assert response.context['object_list'][0].category.title == "Nature"

    def test_upload_image_view_get(self, client):
        user = User.objects.create_user(username='admin', password='password', is_staff=True)
        client.login(username='admin', password='password')

        response = client.get(reverse('upload-image'))

        assert response.status_code == 200
        assert 'form' in response.context

    @override_settings(MEDIA_ROOT=tempfile.gettempdir())  # Use a temp directory for media
    def test_upload_image_view_post(self, client):
        user = User.objects.create_user(username='admin', password='password', is_staff=True)
        category = Category.objects.create(title="Nature")
        client.login(username='admin', password='password')

        # Use an in-memory image file
        test_image = SimpleUploadedFile(
            "test_image.jpg",
            b"\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x80\x00\x00\x00\x00\x00\xFF\xFF\xFF\x21\xF9\x04\x01\x0A\x00\x01\x00\x2C\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02\x4C\x01\x00\x3B",
            content_type="image/jpeg"
        )

        response = client.post(reverse('upload-image'), {
            'category': category.id,
            'image': test_image,
            'description': 'Test Image'
        })

        # Assertions
        assert response.status_code == 302  # Redirect after success
        assert Gallery.objects.count() == 1
        uploaded_image = Gallery.objects.first()
        assert uploaded_image.image.name.startswith('images/test_image')

    def test_delete_image_view(self, client):
        user = User.objects.create_user(username='admin', password='password', is_staff=True)
        category = Category.objects.create(title="Nature")
        gallery_item = Gallery.objects.create(category=category, image="images/test.jpg")
        client.login(username='admin', password='password')

        response = client.post(reverse('delete-image', args=[gallery_item.id]))
        assert response.status_code == 302  # Redirect after deletion
        assert Gallery.objects.count() == 0

    def test_create_category_view(self, client):
        user = User.objects.create_user(username='admin', password='password', is_staff=True)
        client.login(username='admin', password='password')

        response = client.post(reverse('create-category'), {'title': 'New Category'})

        assert response.status_code == 302  # Redirect after success
        assert Category.objects.count() == 1
        assert Category.objects.first().title == 'New Category'

    def test_contact_view_get(self, client):
        response = client.get(reverse('contact'))
        assert response.status_code == 200
        assert 'form' in response.context

    def test_contact_view_post_valid(self, client, settings):
        settings.DEFAULT_FROM_EMAIL = 'test@example.com'
        settings.EMAIL_HOST_USER = 'host@example.com'

        response = client.post(reverse('contact'), {
            'name': 'John Doe',
            'email': 'john@example.com',
            'message': 'Test message'
        })

        assert response.status_code == 302  # Redirect after success
        assert Contact.objects.count() == 1
        assert len(mail.outbox) == 1
        assert mail.outbox[0].subject == 'New Contact Form Submission'

    def test_contact_view_post_invalid(self, client):
        response = client.post(reverse('contact'), {
            'name': '',
            'email': 'invalid-email',
            'message': ''
        })

        assert response.status_code == 200
        assert Contact.objects.count() == 0
        assert 'form' in response.context

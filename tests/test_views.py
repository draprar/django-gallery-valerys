import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from gallery.models import Category, Gallery
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core import mail


@pytest.mark.django_db
class TestViews:
    def test_home_view_with_category_filter(self, client):
        category1 = Category.objects.create(title="Nature")
        category2 = Category.objects.create(title="Urban")
        Gallery.objects.create(
            image=SimpleUploadedFile("nature.jpg", b"file_content", content_type="image/jpeg"),
            description="Nature image",
            category=category1,
        )
        Gallery.objects.create(
            image=SimpleUploadedFile("urban.jpg", b"file_content", content_type="image/jpeg"),
            description="Urban image",
            category=category2,
        )

        response = client.get(reverse('home'), {'category': 'Nature'}, follow=True)
        assert response.status_code == 200
        assert "Nature image" in response.content.decode()
        assert "Urban image" not in response.content.decode()

    def test_upload_image_view_invalid_post(self, client):
        admin = User.objects.create_superuser(username="admin", password="password")
        client.login(username="admin", password="password")
        response = client.post(reverse('upload-image'), {}, follow=True)
        assert response.status_code == 200
        assert "This field is required" in response.content.decode()

    def test_contact_view_get(self, client):
        response = client.get(reverse('contact'), follow=True)
        assert response.status_code == 200
        assert "Contact" in response.content.decode()

    def test_contact_view_post_valid(self, client, settings):
        settings.DEFAULT_FROM_EMAIL = "test@example.com"
        settings.EMAIL_HOST_USER = "admin@example.com"

        response = client.post(
            reverse('contact'),
            {
                'name': 'John Doe',
                'email': 'john.doe@example.com',
                'message': 'This is a test message.',
            }, follow=True
        )
        assert response.status_code == 200
        assert len(mail.outbox) == 1
        assert mail.outbox[0].subject == "New Contact Form Submission"
        messages = list(response.wsgi_request._messages)
        assert any("Your message has been sent successfully!" in str(msg) for msg in messages)

    def test_contact_view_post_invalid(self, client):
        response = client.post(reverse('contact'), {'name': '', 'email': '', 'message': ''}, follow=True)
        assert response.status_code == 200
        assert "This field is required" in response.content.decode()

    def test_delete_image_view_nonexistent(self, client):
        admin = User.objects.create_superuser(username="admin", password="password")
        client.login(username="admin", password="password")
        response = client.post(reverse('delete-image', args=[999]), follow=True)  # Non-existent ID
        assert response.status_code == 404

    def test_create_category_view_invalid_post(self, client):
        admin = User.objects.create_superuser(username="admin", password="password")
        client.login(username="admin", password="password")
        response = client.post(reverse('create-category'), {'title': ''}, follow=True)  # Invalid data
        assert response.status_code == 200
        assert "This field is required" in response.content.decode()

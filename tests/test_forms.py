from io import BytesIO
from PIL import Image
from django.core.files.uploadedfile import SimpleUploadedFile
import pytest
from gallery.forms import GalleryForm, ContactForm, CategoryForm
from gallery.models import Category


# Fixture for creating test images
@pytest.fixture
def create_test_image():
    def _create_test_image(name="test_image.jpg", format="JPEG"):
        image = Image.new("RGB", (100, 100), color="red")
        buffer = BytesIO()
        image.save(buffer, format=format)
        buffer.seek(0)
        return SimpleUploadedFile(name, buffer.read(), content_type=f"image/{format.lower()}")

    return _create_test_image


# Tests for GalleryForm
@pytest.mark.django_db
@pytest.mark.parametrize("file, is_valid, error", [
    (None, False, 'image'),  # Missing image file
    ("valid", True, None),  # Valid image
    (
            SimpleUploadedFile(
                "test_image.txt",
                b"file_content",
                content_type="text/plain"
            ),
            False,
            'image'
    ),
    (
            SimpleUploadedFile(
                "large_image.jpg",
                b"x" * (5 * 1024 * 1024 + 1),  # 5MB + 1 byte (exceeds limit)
                content_type="image/jpeg"
            ),
            False,
            'image'
    ),
])
def test_gallery_form(file, is_valid, error, create_test_image):
    category = Category.objects.create(title="Drawings")
    data = {
        'description': 'A beautiful drawing.',
        'category': category.id,
    }
    if file == "valid":
        file = create_test_image()

    files = {'image': file} if file else {}
    form = GalleryForm(data=data, files=files)
    print(form.errors)
    assert form.is_valid() == is_valid
    if not is_valid:
        assert error in form.errors


# Tests for ContactForm
@pytest.mark.parametrize("data, is_valid, error_fields", [
    ({'name': '', 'email': '', 'message': ''}, False, ['name', 'email', 'message']),  # All fields missing
    ({'name': 'John', 'email': '', 'message': 'Hello'}, False, ['email']),  # Missing email
    ({'name': 'John', 'email': 'invalid-email', 'message': 'Hello'}, False, ['email']),  # Invalid email
    ({'name': 'John', 'email': 'john@example.com', 'message': ''}, False, ['message']),  # Missing message
    ({'name': 'John', 'email': 'john@example.com', 'message': 'Hello'}, True, []),  # Valid form
])
def test_contact_form(data, is_valid, error_fields):
    form = ContactForm(data=data)
    print(form.errors)
    assert form.is_valid() == is_valid
    if not is_valid:
        for field in error_fields:
            assert field in form.errors


# Tests for CategoryForm
@pytest.mark.django_db
@pytest.mark.parametrize("data, is_valid, error_fields", [
    ({'title': ''}, False, ['title']),  # Missing title
    ({'title': 'Paintings'}, True, []),  # Valid form
])
def test_category_form(data, is_valid, error_fields):
    form = CategoryForm(data=data)
    print(form.errors)
    assert form.is_valid() == is_valid
    if not is_valid:
        for field in error_fields:
            assert field in form.errors

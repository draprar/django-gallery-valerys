from io import BytesIO
from PIL import Image
from django.core.files.uploadedfile import SimpleUploadedFile
import pytest
from gallery.forms import GalleryForm
from gallery.models import Category


@pytest.fixture
def create_test_image():
    def _create_test_image(name="test_image.jpg", format="JPEG"):
        # Create an image in memory
        image = Image.new("RGB", (100, 100), color="red")
        buffer = BytesIO()
        image.save(buffer, format=format)
        buffer.seek(0)
        return SimpleUploadedFile(name, buffer.read(), content_type=f"image/{format.lower()}")

    return _create_test_image


@pytest.mark.django_db
@pytest.mark.parametrize("file, is_valid, error", [
    # Test gallery form with valid and invalid image uploads
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
    # Create a category to link with the gallery item
    category = Category.objects.create(title="Drawings")

    # Prepare form data
    data = {
        'description': 'A beautiful drawing.',
        'category': category.id,
    }

    # Use dynamically created image if file is "valid"
    if file == "valid":
        file = create_test_image()

    files = {'image': file} if file else {}

    # Instantiate form
    form = GalleryForm(data=data, files=files)

    # Print form errors for debugging purposes
    print(form.errors)

    # Check if the form validation matches expectations
    assert form.is_valid() == is_valid

    # If invalid, verify the expected error field is in form errors
    if not is_valid:
        assert error in form.errors

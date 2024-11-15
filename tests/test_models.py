import pytest
from gallery.models import Category, Gallery


@pytest.mark.django_db
def test_category_creation():
    # Create a category
    category = Category.objects.create(title="Drawings")

    # Assert category fields
    assert category.title == "Drawings"
    assert str(category) == "Drawings"


@pytest.mark.django_db
def test_gallery_creation():
    # Create a category
    category = Category.objects.create(title="Drawings")

    # Create a gallery item
    gallery = Gallery.objects.create(
        category=category,
        image="test_image.jpg",
        description="A beautiful drawing."
    )

    # Assert gallery fields
    assert gallery.description == "A beautiful drawing."
    assert gallery.category == category
    assert gallery.image.name == "test_image.jpg"
    assert str(gallery) == gallery.image.url

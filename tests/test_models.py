import pytest
from gallery.models import Category, Gallery, Contact
from datetime import datetime
from django.utils.timezone import now
from django.core.exceptions import ValidationError


@pytest.mark.django_db
def test_category_creation():
    # Create a category
    category = Category.objects.create(title="Drawings")

    # Assert category fields
    assert category.title == "Drawings"
    assert str(category) == "Drawings"


@pytest.mark.django_db
def test_category_unique_constraint():
    # Create a category
    Category.objects.create(title="Drawings")

    # Attempt to create a category with the same title
    with pytest.raises(ValidationError):
        category = Category(title="Drawings")
        category.full_clean()  # Validate the model instance


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


@pytest.mark.django_db
def test_gallery_ordering():
    # Create a category
    category = Category.objects.create(title="Drawings")

    # Create multiple gallery items
    gallery1 = Gallery.objects.create(category=category, image="image1.jpg", created_at=now())
    gallery2 = Gallery.objects.create(category=category, image="image2.jpg", created_at=now())

    # Assert ordering by ID
    galleries = list(Gallery.objects.all())
    assert galleries[0] == gallery1
    assert galleries[1] == gallery2


@pytest.mark.django_db
def test_gallery_deletion_with_category():
    # Create a category
    category = Category.objects.create(title="Drawings")

    # Create a gallery item linked to the category
    gallery = Gallery.objects.create(
        category=category,
        image="test_image.jpg",
        description="A beautiful drawing."
    )

    # Delete the category
    category.delete()

    # Assert the gallery item is deleted
    assert Gallery.objects.count() == 0


@pytest.mark.django_db
def test_contact_creation():
    # Create a contact message
    contact = Contact.objects.create(
        name="John Doe",
        email="johndoe@example.com",
        message="Hello, I am interested in your gallery."
    )

    # Assert contact fields
    assert contact.name == "John Doe"
    assert contact.email == "johndoe@example.com"
    assert contact.message == "Hello, I am interested in your gallery."
    assert isinstance(contact.submitted_at, datetime)
    assert str(contact) == "Message from John Doe"


@pytest.mark.django_db
def test_contact_str_representation():
    # Create a contact message
    contact = Contact.objects.create(
        name="Jane Doe",
        email="janedoe@example.com",
        message="I'd like to collaborate."
    )

    # Assert string representation
    assert str(contact) == "Message from Jane Doe"


@pytest.mark.django_db
def test_contact_required_fields():
    # Attempt to create a Contact with missing required fields
    contact = Contact(name="", email="", message="")
    with pytest.raises(ValidationError):
        contact.full_clean()  # Explicitly validate the model instance

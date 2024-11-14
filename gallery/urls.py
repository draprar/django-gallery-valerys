from django.urls import path
from .views import Home, UploadImage, DeleteImage, CreateCategory, ContactView

urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('upload-image/', UploadImage.as_view(), name='upload-image'),
    path('delete-image/<int:pk>', DeleteImage.as_view(), name='delete-image'),
    path('create-category/', CreateCategory.as_view(), name='create-category'),
    path('contact/', ContactView.as_view(), name='contact'),
]
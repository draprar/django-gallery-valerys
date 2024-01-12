from django.urls import path
from .views import Home, UploadImage, CreateCategory

urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('upload-image/', UploadImage.as_view(), name='upload-image'),
    path('create-category/', CreateCategory.as_view(), name='create-category')
]

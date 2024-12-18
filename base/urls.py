from django.contrib import admin
from django.conf import settings
from django.urls import path, include
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('gallery.urls')),
]

# Static and media files in development
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Define error handlers
if not settings.DEBUG:  # Error handlers only apply in production
    from gallery.views import custom_404, custom_500
    handler404 = custom_404
    handler500 = custom_500

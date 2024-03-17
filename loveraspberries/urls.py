from django.contrib import admin
from django.urls import path, include
from . import settings
from django.conf.urls.static import static
from products.views import page_not_found


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('products.urls', namespace='products')),
    path('', include('users.urls', namespace='users')),
    path('', include('reviews.urls', namespace='reviews')),
    path('', include('basket.urls', namespace='basket')),
    path('', include('orders.urls', namespace='orders')),
]

handler404 = page_not_found

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

from django.urls import path
from .views import *

app_name = 'feedbacks'

urlpatterns = [
    path('catalog/<slug:subcategory_slug>/feedbacks/<int:product_id>/', FeedBacks.as_view(), name='reviews'),
]

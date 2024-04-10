from django.urls import path
from .views import *

app_name = 'reviews'

urlpatterns = [
    path('catalog/<slug:subcategory_slug>/feedbacks/<int:product_id>/', FeedBacks.as_view(), name='product_reviews'),
    path('profile/reviews/', UsersReviews.as_view(), name='reviews'),
]

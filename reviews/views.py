from django.views.generic import DetailView, ListView
from products.mixins import BaseMixin
from products.models import Product, SubCategory
from django.db.models import Avg, Count
# Create your views here.

class FeedBacks(BaseMixin, ListView):
    model = Product
    template_name = 'reviews/feedbacks.html'
    context_object_name = 'reviews'
    pk_url_kwarg = 'product_id'
    
    def get_queryset(self):
        return Product.objects.get(pk=self.kwargs['product_id']).reviews.all()
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['subcategory'] = SubCategory.objects.get(slug=self.kwargs['subcategory_slug'])
        context['product_avg_rating'] = context['reviews'].aggregate(avg_rating=Avg('rating'))['avg_rating']
        context['every_counts_stars'] = context['reviews'].values('rating').order_by('rating').annotate(count=Count('rating'))[::-1]
        context['all_count_reviews'] = context['reviews'].count()
        context['product'] = Product.objects.get(pk=self.kwargs['product_id'])
        return context
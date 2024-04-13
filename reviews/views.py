from typing import Any
from django.db.models.query import QuerySet
from django.views.generic import DetailView, ListView
from products.mixins import BaseMixin
from products.models import Product, SubCategory
from django.db.models import Avg, Count
from orders.models import Order
from reviews.models import Review
from users.models import User
from .forms import ReviewForm
from django.shortcuts import redirect
from django.http import JsonResponse


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

class UsersReviews(BaseMixin, ListView):
    model = Order
    template_name = 'reviews/userreviews.html'
    context_object_name = 'products'

    def get_queryset(self) -> QuerySet[Any]:
        # return Order.objects.filter(initiator=self.request.user, status=Order.RECEIVED)
        return Product.objects.all() #временно эту модель сделаю, пока не сделаем модель покупок или не доработаем модель Order
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reviews'] = Review.objects.filter(user=self.request.user).select_related('product')
        context['form'] = ReviewForm()
        return context
    
    
    def post(self, request, *args, **kwargs):
        form = ReviewForm(data=request.POST)
        if form.is_valid():
            user = User.objects.get(pk=request.user.pk)
            try:
                review, created = user.reviews.get_or_create(product=Product.objects.get(pk=int(request.POST.get('product'))))
                review.rating = int(form.cleaned_data['rating'])
                review.description = form.cleaned_data['description']
                review.save()
            except:
                user.reviews.create(product=Product.objects.get(pk=int(request.POST.get('product'))),
                                    rating=int(form.cleaned_data['rating']),
                                    description = form.cleaned_data['description'])
            
            return JsonResponse({'success': True, 'form_errors': form.errors, })
        else:
            print('Не прошло валидацию')
            return JsonResponse({'success': False, 'form_errors': form.errors, })
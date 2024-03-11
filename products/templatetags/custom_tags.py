from django import template
from reviews.models import Review

register = template.Library()

@register.simple_tag
def custom_range(count):
    return range(int(count))


@register.simple_tag
def width_line_rating(product_id, value, all_count):
    count = Review.objects.filter(product=product_id, rating=int(value)).count()
    return [count, int(count)/int(all_count)*100] #the first its common count, the second for rating_line


@register.simple_tag
def find_product_in_basket(product, basket):
    try:
        return basket.get(product=product)
    except:
        return False
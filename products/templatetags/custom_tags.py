from django import template

register = template.Library()

@register.simple_tag
def custom_range(count):
    return range(count)

@register.simple_tag
def width_line_rating(count, all_count):
    return int(count)/int(all_count)*100
from django.contrib import admin
from orders.models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'status',)
    fields = (
        'id', 'created',
        ('first_name',), ('last_name'), ('email', 'address'),
         'status', 'initiator', 'basket_history')
    readonly_fields = ('id', 'created')

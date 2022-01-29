from django.contrib import admin

from orders.models import OrderProduct, Order, Payment


admin.site.register(Payment)

admin.site.register(Order)

admin.site.register(OrderProduct)

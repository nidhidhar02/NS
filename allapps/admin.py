from django.contrib import admin
from .models import Customer, CustomerCredit, Product, Order, OrderDetails, Payment, EmiDetails, Cart, PinCode
# Register your models here.
admin.site.register(Customer)
admin.site.register(CustomerCredit)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderDetails)
admin.site.register(Payment)
admin.site.register(EmiDetails)
admin.site.register(Cart)
admin.site.register(PinCode)

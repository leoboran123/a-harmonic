from django.contrib import admin

from .models import Coupon, UserCoupon, Order, OrderProduct

# Register your models here.

class CouponAdmin(admin.ModelAdmin):
    list_display = ('name', 'discount', 'category_id', 'code')

admin.site.register(Coupon, CouponAdmin)

class UserCouponAdmin(admin.ModelAdmin):
    list_display = ('coupon', 'user', 'status',)

admin.site.register(UserCoupon, UserCouponAdmin)

admin.site.register(Order)
admin.site.register(OrderProduct)


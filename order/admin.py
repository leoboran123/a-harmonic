from django.contrib import admin

from .models import Coupon

# Register your models here.

class CouponAdmin(admin.ModelAdmin):
    list_display = ('name', 'discount', 'category_id')

admin.site.register(Coupon, CouponAdmin)

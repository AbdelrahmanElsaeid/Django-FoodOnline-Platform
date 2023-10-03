from django.contrib import admin
from .models import Cart, Tax
# Register your models here.


class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'fooditem', 'quantity', 'updated_at')



admin.site.register(Cart, CartAdmin)


class TaxAdmin(admin.ModelAdmin):
    list_display = ('tax_type', 'tax_percentage', 'is_active')


admin.site.register(Tax, TaxAdmin)
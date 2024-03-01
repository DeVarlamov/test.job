from django.contrib import admin

from product.models import Product, Lesson, Group, Purchase

admin.site.register(Product)
admin.site.register(Lesson)
admin.site.register(Group)
admin.site.register(Purchase)

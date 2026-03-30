from django.contrib import admin

from ministore.models import Category, Product

# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name","price","stock","category")
    list_filter = ("category",)
    search_fields = ("name",)

admin.site.register(Product,ProductAdmin)
admin.site.register(Category)
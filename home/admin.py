from django.contrib import admin

# Register your models here.
from home.models import Category, Home


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'status']
    list_filter = ['status']
class HomeAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'price', 'status']
    list_filter = ['status']

admin.site.register(Category, CategoryAdmin)
admin.site.register(Home, HomeAdmin)

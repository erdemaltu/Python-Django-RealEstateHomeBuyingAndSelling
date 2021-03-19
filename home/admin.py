from django.contrib import admin

# Register your models here.
from home.models import Category
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'status']
    list_filter = ['status']

admin.site.register(Category, CategoryAdmin)

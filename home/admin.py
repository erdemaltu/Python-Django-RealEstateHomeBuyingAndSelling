from django.contrib import admin

# Register your models here.
from home.models import Category, Home, Images

class HomeImageInline(admin.TabularInline):
    model = Images
    extra = 5

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'status']
    list_filter = ['status']
class HomeAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'price', 'status']
    list_filter = ['status']
    inlines = [HomeImageInline]
class ImageAdmin(admin.ModelAdmin):
    list_display = ['title', 'home', 'image']

admin.site.register(Category, CategoryAdmin)
admin.site.register(Home, HomeAdmin)
admin.site.register(Images, ImageAdmin)

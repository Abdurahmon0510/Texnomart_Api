from django.contrib import admin
from .models import Product, Category, AttributeKey, AttributeValue, Comment, Image


class AttributeValueInline(admin.TabularInline):
    model = AttributeValue
    extra = 1



@admin.register(AttributeKey)
class AttributeKeyAdmin(admin.ModelAdmin):
    list_display = ('id', 'key')
    inlines = [AttributeValueInline]


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category', 'price', 'is_liked', 'comment_count')
    search_fields = ('name', 'category__name')
    list_filter = ('category', 'is_liked')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)


admin.site.register(Comment)
admin.site.register(Image)
admin.site.register(AttributeValue)

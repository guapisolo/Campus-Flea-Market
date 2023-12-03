from django import forms
from django.contrib import admin
from mptt.admin import MPTTModelAdmin

admin.site.site_header = 'UESTC跳蚤市场管理'
admin.site.site_title = 'UESTC跳蚤市场管理'
admin.site.index_title = '首页'

from .models import (
    Category,
    Product,
    ProductImage,
)

admin.site.register(Category, MPTTModelAdmin)

class ProductImageInline(admin.TabularInline):
    model = ProductImage

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [
        ProductImageInline,
    ]
    search_fields=['title']  
    list_filter=['category']  #右侧栏过滤器，按作者进行筛选
    date_hierarchy = 'created_at'    # 详细时间分层筛选


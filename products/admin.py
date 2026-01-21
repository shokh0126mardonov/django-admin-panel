from django.contrib import admin
from django.utils.html import format_html

from .models import Category
from .forms import CategoryForm


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('colored_name', 'image_preview', 'is_active', 'created_at')
    prepopulated_fields = {'slug': ('name',)}
    list_display_links = ('colored_name',)
    list_filter = ('is_active', 'created_at')
    list_per_page = 20
    search_fields = ('name', 'description')
    date_hierarchy = 'created_at'
    empty_value_display = '-empty-'
    fieldsets = (
        ('Required', {
            'fields': ('name', 'slug', 'image', 'is_active')
        }),
        (
            'Information', {
                'fields': ('description', 'color_code'),
                'classes': ('collapse',),
            }
        ),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )
    readonly_fields = ('created_at', 'updated_at')
    form = CategoryForm
    actions = ['make_active', 'make_inactive']

    @admin.display(description='Name', ordering='name')
    def colored_name(self, obj):
        return format_html(
            '<span style="color: {};">{}</span>',
            obj.color_code,
            obj.name
        )
    
    @admin.display(description='Image Preview')
    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="width: 50px; height: 50px; object-fit: cover; border-radius: 4px;" />',
                obj.image.url
            )
        return format_html('<span style="color: #888888;">No Image</span>')

    @admin.action(description='Mark selected categories as active')
    def make_active(self, request, queryset):
        updated_count = queryset.update(is_active=True)
        self.message_user(
            request,
            f'{updated_count} category(ies) were successfully marked as active.'
        )

    @admin.action(description='Mark selected categories as inactive')
    def make_inactive(self, request, queryset):
        updated_count = queryset.update(is_active=False)
        self.message_user(
            request,
            f'{updated_count} category(ies) were successfully marked as inactive.'
        )

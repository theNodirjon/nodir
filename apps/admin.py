from django.contrib import admin
from apps.models import Book, Category, Author, Review, OrderItem, Cart
from django.utils.html import format_html

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name', 'description')
    ordering = ('name',)

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name', 'bio')
    search_fields = ('name', 'bio')
    ordering = ('name',)

@admin.register(Book)
class BooksAdmin(admin.ModelAdmin):
    list_display = ('title','image_preview', 'author', 'price', 'availability', 'format','quantity', 'average_rating', 'owner')
    list_filter = ('availability', 'format', 'category', 'author', 'publisher')
    search_fields = ('title', 'author__name', 'category__name', 'owner__username')
    autocomplete_fields = ('author', 'category', 'owner')
    fieldsets = (
        ('General Information', {
            'fields': ('title', 'author', 'price', 'category', 'availability', 'format', 'quantity', 'isbn')
        }),
        ('Additional Info', {
            'fields': ('publisher', 'language', 'pages', 'owner', 'description', )
        }),
        ('Media', {
            'fields': ('book_image', 'book_pdf')
        })
    )

    def image_preview(self, obj: Book):
        if obj.book_image:  # Fayl borligini tekshiradi
            return format_html(
                f'<img src="{obj.book_image.url}" style="width:100px; border-radius:10px;" alt="{obj.title}">'
            )
        return "No image"  # Agar fayl biriktirilmagan bo'lsa, bu matn qaytariladi

    image_preview.short_description = "Image Preview"

@admin.register(Review)
class ReviewsAdmin(admin.ModelAdmin):
    list_display = ('book', 'user', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('book__title', 'user__username', 'text')
    autocomplete_fields = ('book', 'user')

@admin.register(OrderItem)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['book__title', 'order_status', 'quantity']
    list_filter = ('book__title', )
    search_fields = 'book__title',

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user__username', 'cart_status')
    list_filter = ('user__username', 'cart_status')
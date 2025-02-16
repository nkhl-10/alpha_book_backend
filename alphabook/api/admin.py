from django.contrib import admin
from .models import User, Category, Address, Book, Transaction, BookReadAccess

# User Admin
from .models.book import BookImage


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'password', 'email', 'is_active', 'created_at')
    search_fields = ('username', 'email')
    list_filter = ('is_active', 'created_at')


# Category Admin
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'created_at')
    search_fields = ('name',)


# Address Admin
@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'city', 'state', 'zip_code', 'created_at')
    search_fields = ('city', 'state')
    list_filter = ('state',)


# Book Admin
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'seller', 'category', 'price', 'book_type', 'read_access', 'created_at')
    search_fields = ('title', 'author', 'seller__username')
    list_filter = ('book_type', 'read_access', 'category')


# Transaction Admin
@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('id', 'book', 'buyer', 'amount', 'status', 'transaction_date')
    search_fields = ('book__title', 'buyer__username')
    list_filter = ('status',)


# BookReadAccess Admin
@admin.register(BookReadAccess)
class BookReadAccessAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'book', 'access_granted', 'accessed_at')
    search_fields = ('user__username', 'book__title')
    list_filter = ('access_granted',)


# BookImages Admin
@admin.register(BookImage)
class BookImageAdmin(admin.ModelAdmin):
    list_display = ('image',)

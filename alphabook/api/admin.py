from django.contrib import admin
from .models import User, Category, Address, Book, Transaction, BookReadAccess, SyllabusBook

# User Admin
from .models.book import BookImage


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'is_active', 'name','phone','avatar')
    search_fields = ('username', 'email')
    list_editable  = ('username', 'email','avatar','name','phone')
    list_filter = ('is_active', 'created_at')


# Category Admin
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'created_at')
    search_fields = ('name',)


# Address Admin
@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('user', 'city', 'state', 'zip_code','latitude','longitude')
    search_fields = ('city', 'state')
    list_filter = ('state',)
    list_editable = ('latitude','longitude')

# Book Admin
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'is_sold','location','seller', 'category', 'price', 'book_type', 'read_access', 'created_at')
    search_fields = ('title', 'author', 'is_sold', 'seller__username')
    list_filter = ('book_type', 'read_access', 'is_sold', 'category')
    list_editable = ('seller','is_sold','location')


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

@admin.register(SyllabusBook)
class SyllabusBookAdmin(admin.ModelAdmin):
    list_display = ('course_name', 'book', 'university_name', 'semester')

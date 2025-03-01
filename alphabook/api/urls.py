from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import (
    register, login, UserListCreateAPIView,
    BookListCreateAPIView, TransactionListCreateAPIView,
    BookImagesListCreateAPIView, BookDetailView, AvailableBooksAPIView, CategoryListAPIView,
    BooksByCategoryAPIView, BooksByUserAPIView, OrderedBooksAPIView, SearchBookAPIView,BuyBookAPIView,
)

urlpatterns = [
    path('register', register, name='register'),
    path('login', login, name='login'),
    path('users/<int:pk>/', UserListCreateAPIView.as_view(), name='users'),
    path('books', BookListCreateAPIView.as_view(), name='book-list-create'),
    path('transactions', TransactionListCreateAPIView.as_view(), name='transaction-list-create'),
    path('getBooks/<int:pk>/', BookDetailView.as_view(), name='book-detail'),

    path('buyBook', BuyBookAPIView.as_view(), name='buy-book'),
    path('getBooks', AvailableBooksAPIView.as_view(), name='getBookList'),
    path('categories/', CategoryListAPIView.as_view(), name='getCategory'),
    path('categories/<int:category_id>/', BooksByCategoryAPIView.as_view(), name='getCategoryByBook'),
    path('userByBooks/<int:user_id>', BooksByUserAPIView.as_view(), name='getBookByUser'),
    path('userByOrderedBooks/<int:user_id>/', OrderedBooksAPIView.as_view(), name='getBookOrdered'),

    path('search/', SearchBookAPIView.as_view(), name='search-books'),
] +  static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
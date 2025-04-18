from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import (
    register, login, UserListCreateAPIView,
    BookListCreateAPIView, TransactionListCreateAPIView, BookDetailView, AvailableBooksAPIView, CategoryListAPIView,
    BooksByCategoryAPIView, BooksByUserAPIView, OrderedBooksAPIView, SearchBookAPIView, BuyBookAPIView, upload_avatar,
    AddressListCreateView, UserAddressListView, SearchCategory, AddressUpdateAPIView, AddressDeleteAPIView,
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
                  path('searchCategories/', SearchCategory.as_view(), name='searchCategories'),

                  path('categories/<int:category_id>/', BooksByCategoryAPIView.as_view(), name='getCategoryByBook'),
                  path('userByBooks/<int:user_id>', BooksByUserAPIView.as_view(), name='getBookByUser'),
                  path('userByOrderedBooks/<int:user_id>/', OrderedBooksAPIView.as_view(), name='getBookOrdered'),
                  path('uploadAvatar/', upload_avatar, name='upload-avatar'),

                  path('search/', SearchBookAPIView.as_view(), name='search-books'),
                  path('addresses/', AddressListCreateView.as_view(), name='address-list-create'),  # GET, POST
                  path('addressesUpdate/<int:id>/', AddressUpdateAPIView.as_view(), name='address-update'),
                  path('addressesDelete/<int:id>/', AddressDeleteAPIView.as_view(), name='address-delete'),


                  path('addresses/<int:user_id>/', UserAddressListView.as_view(), name='address-detail'),  # GET, PUT, DELETE

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

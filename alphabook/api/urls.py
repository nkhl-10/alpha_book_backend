from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import register, login, UserListCreateAPIView, BookListCreateAPIView, TransactionListCreateAPIView, \
    BookImagesListCreateAPIView

urlpatterns = [
    path('register', register, name='register'),
    path('login', login, name='login'),
    path('users', UserListCreateAPIView.as_view(), name='users'),
    path('books', BookListCreateAPIView.as_view(), name='book-list-create'),
    path('transactions', TransactionListCreateAPIView.as_view(), name='transaction-list-create'),
    path('book_images', BookImagesListCreateAPIView.as_view(), name='book-image-list-create')
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

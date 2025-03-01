from django.contrib.auth import authenticate
from django.db.models import Q
from django.template.context_processors import request
from rest_framework import generics
from rest_framework import status
from rest_framework.authtoken.models import Token  # Correct import
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import ValidationError
from rest_framework.generics import RetrieveAPIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response

from .models import User, Book, Transaction, BookReadAccess, Category
from .models.book import BookImage
from .serializers import RegisterSerializer, BookImageSerializer, CategorySerializer
from .serializers import UserSerializer, BookSerializer, TransactionSerializer


@api_view(['POST'])
def register(request):
    serializer = RegisterSerializer(data=request.data)

    # Validate the input data
    if serializer.is_valid():
        user = serializer.save()  # Save the user
        # token, _ = Token.objects.get_or_create(user=user)  # Create authentication token
        return Response({
            # "token": token.key,
            "username": user.username
        }, status=status.HTTP_201_CREATED)

    # If data is invalid, return the validation errors
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Login API
@api_view(['POST'])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)

    if user:
        # token, _ = Token.objects.get_or_create(user=user)  # Ensure correct import
        return Response({
            # 'token': token.key,
            'username': user.username,
            'id': user.id
        }, status=status.HTTP_200_OK)

    return Response({'error': 'Invalid Credentials'}, status=status.HTTP_400_BAD_REQUEST)


# User API
class UserListCreateAPIView(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


# Book API
class BookListCreateAPIView(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    parser_classes = [MultiPartParser, FormParser]

    def create(self, request, *args, **kwargs):
        images_data = request.FILES.getlist('images')
        book_data = request.data
        book_serializer = self.get_serializer(data=book_data)
        book_serializer.is_valid(raise_exception=True)
        book = book_serializer.save()

        for image_data in images_data:
            BookImage.objects.create(book=book, image=image_data)

        return Response(book_serializer.data, status=status.HTTP_201_CREATED)


# Transaction API
class TransactionListCreateAPIView(generics.ListCreateAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer


class BuyBookAPIView(generics.CreateAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

    def perform_create(self, serializer):
        data = self.request.data
        user_id = data.get("buyerId")
        book_id = data.get("bookId")
        amount = data.get("amount")
        if not user_id or not book_id:
            raise ValidationError({"error": "user_id and book_id are required."})
        try:
            user = User.objects.get(id=user_id)
            book = Book.objects.get(id=book_id)
        except User.DoesNotExist:
            raise ValidationError({"error": "Invalid user ID."})
        except Book.DoesNotExist:
            raise ValidationError({"error": "Invalid book ID."})
        if book.seller == user:
            raise ValidationError({"error": "You cannot buy your own book."})
        if book.book_type in ["free_book", "pdf"] and book.read_access == "free":
            return Response(
                {"message": "You can access this book for free.",
                 "pdf_url": book.pdf_file.url if book.pdf_file else None},
                status=status.HTTP_200_OK,
            )
        if amount is None: amount = book.price
        transaction = Transaction.objects.create(
            buyer=user,
            book=book,
            amount=amount,
            status="pending"
        )
        return Response({"message": "Transaction created.", "transaction_id": transaction.id},
                        status=status.HTTP_201_CREATED)


# Book API
class BookImagesListCreateAPIView(generics.ListCreateAPIView):
    queryset = BookImage.objects.all()
    serializer_class = BookImageSerializer


class BookDetailView(RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class OrderedBooksAPIView(generics.ListAPIView):
    serializer_class = TransactionSerializer

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        return Transaction.objects.filter(buyer_id=user_id, status='completed')


class BooksByUserAPIView(generics.ListAPIView):
    serializer_class = BookSerializer

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        return Book.objects.filter(seller_id=user_id)


class BooksByCategoryAPIView(generics.ListAPIView):
    serializer_class = BookSerializer

    def get_queryset(self):
        category_id = self.kwargs['category_id']
        return Book.objects.filter(category_id=category_id, book_type__in=['resell', 'new']).exclude(
            transactions__status='completed'
        ) | Book.objects.filter(category_id=category_id, book_type='pdf')


class CategoryListAPIView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class AvailableBooksAPIView(generics.ListAPIView):
    queryset = Book.objects.filter(book_type__in=['resell', 'new']).exclude(
        transactions__status='completed'
    ) | Book.objects.filter(book_type='pdf')  # PDFs are always available
    serializer_class = BookSerializer


class SearchBookAPIView(generics.ListAPIView):
    serializer_class = BookSerializer

    def get_queryset(self):
        query = self.request.query_params.get('q', '')  # Get search keyword
        return Book.objects.filter(
            Q(title__icontains=query) |  # Search in book title
            Q(description__icontains=query) |  # Search in description
            Q(category__name__icontains=query)  # Search in category name
        ).exclude(
            id__in=Transaction.objects.filter(book__book_type__in=['resell', 'new'], status='completed').values_list(
                'book_id', flat=True)
        )

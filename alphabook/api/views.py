from django.contrib.auth import authenticate
from django.db import IntegrityError
from django.db.models import Q
from rest_framework import generics
from rest_framework import status
from rest_framework.decorators import api_view, parser_classes
from rest_framework.exceptions import ValidationError
from rest_framework.generics import RetrieveAPIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import User, Book, Transaction, Category, Address
from .models.book import BookImage
from .serializers import RegisterSerializer, BookImageSerializer, CategorySerializer, UserAvatarSerializer, \
    AddressSerializer, BookUploadSerializer
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
    queryset = Book.objects.filter(is_sold=False)
    serializer_class = BookUploadSerializer
    parser_classes = [MultiPartParser, FormParser]

    def create(self, request, *args, **kwargs):
        try:
            images_data = request.FILES.getlist('images')
            book_data = request.data
            book_serializer = self.get_serializer(data=book_data)
            book_serializer.is_valid(raise_exception=True)
            book = book_serializer.save()
            for image_data in images_data:
                BookImage.objects.create(book=book, image=image_data)

            return Response(book_serializer.data, status=status.HTTP_201_CREATED)

        except ValidationError as e:
            print(str(e))
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        except IntegrityError as e:
            print(str(e))
            return Response({"error": "Database error: " + str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        except Exception as e:
            print(str(e))
            return Response({"error": "Something went wrong: " + str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# Transaction API
class TransactionListAPIView(generics.RetrieveAPIView):
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

            if book.is_sold:
                raise ValidationError({"error": "This book has already been sold."})

                # ✅ Set the book as sold
            book.is_sold = True
            book.save()

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


class OrderedBooksAPIView(generics.ListAPIView):
    serializer_class = TransactionSerializer

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        return Transaction.objects.filter(buyer_id=user_id, status='pending')


class SoldBookAPIView(generics.ListAPIView):
    serializer_class = TransactionSerializer

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        return Transaction.objects.filter(book__seller_id=user_id, status='pending')


class TransactionAPIView(generics.ListAPIView):
    serializer_class = TransactionSerializer

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        return Transaction.objects.filter(book__seller_id=user_id, status='pending')


class YourBookApiView(generics.ListAPIView):
    serializer_class = BookSerializer

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        return Book.objects.filter(seller_id=user_id, is_sold=False)


class BooksByCategoryAPIView(generics.ListAPIView):
    serializer_class = BookSerializer

    def get_queryset(self):
        category_id = self.kwargs['category_id']
        return Book.objects.filter(category_id=category_id, is_sold=False)


class CategoryListAPIView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class SearchCategory(APIView):
    def get(self, request):
        query = request.GET.get("query", "")  # Get search query from request
        categories = Category.objects.filter(Q(name__icontains=query))  # Search in category name
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)


class BookDetailView(RetrieveAPIView):
    queryset = Book.objects.filter(is_sold=False)
    serializer_class = BookSerializer


class AvailableBooksAPIView(generics.ListAPIView):
    queryset = Book.objects.filter(is_sold=False)
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


@api_view(["POST"])  # Change from UpdateAPIView to a function-based view
@parser_classes([MultiPartParser, FormParser])
def upload_avatar(request):
    user_id = request.data.get("user_id")
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = UserAvatarSerializer(user, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()
        return Response(
            {"message": "Avatar uploaded successfully", "avatar": user.avatar.url},
            status=status.HTTP_200_OK
        )

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AddressListCreateView(generics.ListCreateAPIView):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer


class AddressUpdateAPIView(generics.RetrieveUpdateAPIView):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    lookup_field = 'id'  # This allows editing by address ID


class AddressDeleteAPIView(generics.DestroyAPIView):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    lookup_field = 'id'  # Delete by address ID


class UserAddressListView(generics.ListAPIView):
    serializer_class = AddressSerializer

    def get_queryset(self):
        user = self.kwargs['user_id']
        return Address.objects.filter(user=user)


class ConfirmTransactionView(RetrieveAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

    def post(self, request):
        transaction_id = request.data.get('transaction_id')
        otp = request.data.get('otp')
        if not transaction_id or not otp:
            return Response({'error': 'Transaction ID and OTP are required.'}, status=status.HTTP_400_BAD_REQUEST)
        transaction = self.get_queryset().filter(id=transaction_id).first()
        if not transaction:
            return Response({'message': 'Transaction not found.'}, status=status.HTTP_404_NOT_FOUND)
        if transaction.otp != otp:
            return Response({'message': 'Invalid OTP!'}, status=status.HTTP_400_BAD_REQUEST)
        transaction.status = 'completed'
        transaction.book.is_sold = True
        transaction.save()
        transaction.book.save()
        return Response({'message': 'Transaction completed successfully!'}, status=status.HTTP_200_OK)

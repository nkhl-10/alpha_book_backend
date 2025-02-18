from django.contrib.auth import authenticate
from rest_framework import generics
from rest_framework import status
from rest_framework.authtoken.models import Token  # Correct import
from rest_framework.decorators import api_view, permission_classes
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response

from .models import User, Book, Transaction
from .models.book import BookImage
from .serializers import RegisterSerializer, BookImageSerializer
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
            'username': user.username}, status=status.HTTP_200_OK)

    return Response({'error': 'Invalid Credentials'}, status=status.HTTP_400_BAD_REQUEST)



# User API
class UserListCreateAPIView(generics.ListCreateAPIView):
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

# Book API
class BookImagesListCreateAPIView(generics.ListCreateAPIView):
    queryset = BookImage.objects.all()
    serializer_class = BookImageSerializer
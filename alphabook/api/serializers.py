from rest_framework import serializers

from .models import User, Category, Address, Book, Transaction, BookReadAccess, SyllabusBook
from .models.book import BookImage


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'required': True},
        }

    def create(self, validated_data):
        """Create a new user."""
        return User.objects.create_user(**validated_data)


# Category Serializer
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description']


# Address Serializer
class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['id', 'user', 'street', 'city', 'state', 'zip_code', 'latitude', 'longitude']


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'phone', 'avatar','name']


class BookImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookImage
        fields = ['id', 'image']


class SyllabusBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = SyllabusBook
        fields = ['course_name',  'university_name', 'semester', 'subjects']


class BookSerializer(serializers.ModelSerializer):
    images = BookImageSerializer(many=True, required=False)
    category = CategorySerializer(read_only=False)
    location = AddressSerializer(read_only=False)
    syllabus = SyllabusBookSerializer(read_only=False)

    class Meta:
        model = Book
        fields = '__all__'
        read_only_fields = ['id',  'created_at', 'updated_at']


class BookUploadSerializer(serializers.ModelSerializer):
    images = BookImageSerializer(many=True, required=False)

    class Meta:
        model = Book
        fields = '__all__'
        extra_kwargs = {'pdf_file': {'required': False}}
        read_only_fields = ['id',  'created_at', 'updated_at']

    def create(self, validated_data):
        images_data = validated_data.pop('images', [])
        book = Book.objects.create(**validated_data)
        for image_data in images_data:
            BookImage.objects.create(book=book, **image_data)
        return book


# Transaction Serializer
class TransactionSerializer(serializers.ModelSerializer):
    book = BookSerializer(read_only=True)
    buyer = UserSerializer(read_only=True)

    class Meta:
        model = Transaction
        fields = ['id', 'book', 'buyer', 'amount', 'status', 'transaction_date','otp']


# BookReadAccess Serializer
class BookReadAccessSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    book = BookSerializer(read_only=True)

    class Meta:
        model = BookReadAccess
        fields = ['id', 'user', 'book', 'access_granted', 'payment', 'accessed_at']



class UserAvatarSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['avatar']

    def update(self, instance, validated_data):
        instance.avatar = validated_data.get('avatar', instance.avatar)
        instance.save()
        return instance
from rest_framework import serializers

from .models import User, Category, Address, Book, Transaction, BookReadAccess
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
        fields = ['id', 'username', 'email', 'password', 'phone', 'avatar']


class BookImageSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = BookImage
        fields = ['id', 'image_url']

    def get_image_url(self, obj):
        request = self.context.get('request')
        if obj.image and request:
            return request.build_absolute_uri(obj.image.url)
        return None


class BookSerializer(serializers.ModelSerializer):
    images = BookImageSerializer(many=True, required=False)
    category = CategorySerializer(read_only=True)
    location = AddressSerializer(read_only=True)
    pdf_file = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = '__all__'
        extra_kwargs = {'pdf_file': {'required': False}}
        read_only_fields = ['id', 'category', 'seller', 'created_at', 'updated_at']

    def create(self, validated_data):
        images_data = validated_data.pop('images', [])
        book = Book.objects.create(**validated_data)
        for image_data in images_data:
            BookImage.objects.create(book=book, **image_data)
        return book

    def get_pdf_file(self, obj):
        request = self.context.get('request')
        if obj.pdf_file and request:
            return request.build_absolute_uri(obj.pdf_file.url)
        return None


# Transaction Serializer
class TransactionSerializer(serializers.ModelSerializer):
    book = BookSerializer(read_only=True)
    buyer = UserSerializer(read_only=True)

    class Meta:
        model = Transaction
        fields = ['id', 'book', 'buyer', 'amount', 'status', 'transaction_date']


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
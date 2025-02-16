from django.db import models


class Book(models.Model):
    BOOK_TYPE_CHOICES = [
        ('resell', 'Resell'),
        ('new', 'New'),
        ('pdf', 'PDF'),
    ]
    READ_ACCESS_CHOICES = [
        ('free', 'Free'),
        ('paid', 'Paid'),
    ]
    CONDITION_CHOICES = [
        ('excellent', 'Excellent'),
        ('very_good', 'Very Good'),
        ('good', 'Good'),
        ('average', 'Average'),
        ('poor', 'Poor'),
    ]
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True)
    seller = models.ForeignKey('User', on_delete=models.SET_NULL, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    condition = models.CharField(max_length=10, choices=CONDITION_CHOICES, default='good')
    book_type = models.CharField(max_length=10, choices=BOOK_TYPE_CHOICES, default='resell')
    pdf_file = models.FileField(upload_to='book_pdfs/', blank=True, null=True)
    read_access = models.CharField(max_length=10, choices=READ_ACCESS_CHOICES, blank=True, null=True)
    location = models.ForeignKey('Address', on_delete=models.SET_NULL, null=True, related_name='books')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class BookImage(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='images')
    user = models.ForeignKey('User', on_delete=models.CASCADE, null=True, blank=True)
    image = models.ImageField(upload_to='book_images/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for {self.book.title}"

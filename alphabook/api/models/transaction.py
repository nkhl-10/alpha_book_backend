import random

from django.db import models


class Transaction(models.Model):
    TRANSACTION_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    id = models.AutoField(primary_key=True)
    book = models.OneToOneField('Book', on_delete=models.CASCADE , related_name='transactions')
    buyer = models.ForeignKey('User', on_delete=models.CASCADE, related_name='purchases')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10, choices=TRANSACTION_STATUS_CHOICES, default='pending')
    otp = models.CharField(max_length=6, editable=False, blank=True,null=True)
    transaction_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Transaction {self.id} - {self.status}"

    def save(self, *args, **kwargs):
        # ✅ Generate OTP only when creating new row
        if not self.otp:
            self.otp = f"{random.randint(100000, 999999)}"
        super().save(*args, **kwargs)
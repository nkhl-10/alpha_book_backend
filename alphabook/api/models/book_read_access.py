from django.db import models


class BookReadAccess(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='read_access')
    book = models.ForeignKey('Book', on_delete=models.CASCADE, related_name='read_access_users')
    access_granted = models.BooleanField(default=False)
    payment = models.ForeignKey('Transaction', on_delete=models.SET_NULL, null=True, blank=True, related_name='read_access')
    accessed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Access to {self.book.title} by {self.user.username}"
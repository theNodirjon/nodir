from django.db import models

from .base import BaseModel


class OrderItem(BaseModel):
    class OrderStatus(models.TextChoices):
        new = 'New', 'New'
        sent = 'Sent', 'Sent'
        canceled = 'Canceled', 'Canceled'

    book = models.OneToOneField('apps.Book', on_delete=models.CASCADE, related_name='book_orders')
    order_status = models.CharField(max_length=250, choices=OrderStatus.choices, default=OrderStatus.new)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity}-{self.book}"


class Cart(BaseModel):
    class CartStatus(models.TextChoices):
        saved = 'Saved', 'Saved'
        sent = 'Sent', 'Sent'
        canceled = 'Canceled', 'Canceled'

    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='carts')
    orders = models.ManyToManyField(OrderItem, related_name='carts', blank=True)
    cart_status = models.CharField(max_length=250, choices=CartStatus.choices, default=CartStatus.saved)

    def __str__(self):
        return f"Cart_id:{self.id} - {self.user.username}"

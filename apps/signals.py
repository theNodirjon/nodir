from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from .models import Review


@receiver(post_save, sender=Review)
def update_book_rating_on_save(sender, instance, **kwargs):
    """
    Sharh qo'shilganda yoki yangilanganida kitobning o'rtacha reytingini yangilash.
    """
    instance.book.update_average_rating()

@receiver(post_delete, sender=Review)
def update_book_rating_on_delete(sender, instance, **kwargs):
    """
    Sharh o'chirilganda kitobning o'rtacha reytingini yangilash.
    """
    instance.book.update_average_rating()
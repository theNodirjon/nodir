from decimal import Decimal

from django.core.validators import FileExtensionValidator, MinValueValidator, MaxValueValidator
from django.db import models
from django_resized import ResizedImageField
from apps.utils.validators import validate_file_type

from accounts.models import User
from .authors import Author
from .base import BaseModel
from .categories import Category


class Book(BaseModel):
    class Availability(models.TextChoices):
        in_stock = 'In stock', 'In stock'
        out_of_stock = 'Out of stock', 'Out of stock'
        on_sale = 'On sale', 'On sale'
        new = 'New', 'New'

    class Format(models.TextChoices):
        standard = 'Standard', 'Standard'
        downloadable = 'Downloadable', 'Downloadable'
        external = 'External', 'External'

    title = models.CharField(max_length=250)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ManyToManyField(Category, related_name='categories', blank=True)
    availability = models.CharField(max_length=250, choices=Availability.choices)
    format = models.CharField(max_length=250, choices=Format.choices)
    book_image = ResizedImageField(size=[219, 317], crop=['middle', 'center'], upload_to='images/',
                                   validators=[FileExtensionValidator(['jpg', 'jpeg', 'png', 'bmp', 'webp'])],
                                   null=True, blank=True)
    book_pdf = models.FileField(upload_to='books_pdf/',
                                validators=[validate_file_type], null=True, blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='books')
    average_rating = models.DecimalField(max_digits=3, decimal_places=1, default=0)  # todo chagne
    language = models.CharField(max_length=250, null=True, blank=True)
    pages = models.PositiveIntegerField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    publisher = models.CharField(max_length=250, null=True, blank=True)
    isbn = models.CharField(max_length=250)
    quantity = models.PositiveIntegerField()

    def update_average_rating(self):
        reviews = self.reviews.all()
        if reviews.exists():
            total_rating = sum(review.rating for review in reviews if review.rating is not None)
            self.average_rating = round(Decimal(total_rating) / Decimal(reviews.count()), 1)
        else:
            self.average_rating = 0
        self.save()

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-pk']


class Review(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    text = models.TextField()
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user}-{self.book}"

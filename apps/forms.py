from django import forms
from django.forms import ModelForm
from apps.models import Book, Review


class CommentForm(forms.Form):
    text = forms.CharField()


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = [
            'title',
            'author',
            'price',
            'category',
            'format',
            'availability',
            'book_image',
            'description',
            'publisher',
            'isbn',
            'quantity',
        ]
class ReviewCreateForm(ModelForm):
    class Meta:
        model = Review
        fields = ('rating', 'text')
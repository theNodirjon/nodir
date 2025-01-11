from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from .modellar.book_models import Book, Cart

class IndexView(TemplateView):
    template_name = 'index.html'


def my_books(request):
    books = Book.objects.all()
    return render(request, 'books/my_books.html', {'books': books})

def book_detail(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    return render(request, 'books/book_detail.html', {'book': book})

def cart(request):
    return render(request, 'books/cart.html')


# @login_required
# def cart(request):
#     cart_items = Cart.objects.filter(user=request.user)
#     return render(request, 'books/cart.html', {'cart_items': cart_items})

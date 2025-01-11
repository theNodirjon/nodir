from django.urls import path

from .views import my_books, book_detail, cart

urlpatterns = [
    path('', my_books, name='my_books'),
    path('<int:book_id>/', book_detail, name='book_detail'),
    path('cart/', cart, name='cart'),

]

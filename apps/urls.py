from django.urls import path
from apps.views import AllBooksListView, BookCreateView, MyBooksListView, BookDeleteView
from accounts.views import AuthFormView
from accounts.views.register import RegisterFormView
from apps.views.books import BookDetailView, BookUpdateView

urlpatterns = [
    path('all/', AllBooksListView.as_view(), name='all_books'),
    path('create/', BookCreateView.as_view(), name='book_create'),
    path('my_profile/', MyBooksListView.as_view(), name='my_books'),
    path('delete/<int:pk>', BookDeleteView.as_view(), name='book_delete'),
    path('update/<int:pk>', BookUpdateView.as_view(), name='book_update'),
    path('detail/<int:pk>', BookDetailView.as_view(), name='book_detail'),

]

from urllib import request

from django.shortcuts import render
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.urls.base import reverse
from django.views.generic import ListView, CreateView, DeleteView, FormView, DetailView, UpdateView
from accounts.models import User
from accounts.mixins import LoginAndVerificationRequiredMixin
from apps.forms import BookForm, ReviewCreateForm
from apps.models import Book, Category, Review


class AllBooksListView(ListView):
    model = Book
    context_object_name = 'books'
    template_name = 'booksaw/all_books.html'
    categories = Category.objects.all()
    extra_context = {
        'categories': categories,
    }


class BookCreateView(LoginAndVerificationRequiredMixin, CreateView):
    model = Book
    form_class = BookForm
    template_name = 'booksaw/book_create.html'
    success_url = reverse_lazy('apps:my_books')

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            form.instance.owner = request.user
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class MyBooksListView(LoginAndVerificationRequiredMixin, ListView):
    model = Book
    context_object_name = 'books'
    template_name = 'booksaw/my_books.html'

    def get_queryset(self, **kwargs):
        """Foydalanuvchiga tegishli kitoblarni olish."""
        return self.request.user.books.all()

    def get_context_data(self, **kwargs):
        """Qo'shimcha kontekst ma'lumotlarni qo'shish."""
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['profile'] = self.request.user  # Profilni olish
        return context



class BookDeleteView(LoginAndVerificationRequiredMixin, DeleteView):
    model = Book
    success_url = reverse_lazy('apps:my_books')
    template_name = 'booksaw/confirm_book_delete.html'

    def dispatch(self, request, *args, **kwargs):
        book = self.get_object()
        if book.owner != request.user:
            raise PermissionDenied("You do not have permission to delete this book.")
        return super().dispatch(request, *args, **kwargs)

class BookDetailView(LoginAndVerificationRequiredMixin,FormView, DetailView):
    model = Book
    template_name = 'booksaw/book_detail.html'
    context_object_name = 'book'
    form_class = ReviewCreateForm
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        book = self.object
        context['categories'] = book.category.all()
        context['reviews'] = Review.objects.filter(book=book).order_by('-created_at')
        return context
    def form_valid(self, form):
        book = self.get_object()
        review = form.save(commit=False)
        review.book = book
        review.user = self.request.user
        review.save()
        return HttpResponseRedirect(self.request.path_info)

    def get_success_url(self):
        return reverse('book_detail', kwargs={'pk': self.object.pk})

class BookUpdateView(LoginAndVerificationRequiredMixin, UpdateView):
    model = Book
    form_class = BookForm
    template_name = 'booksaw/book_update.html'
    success_url = reverse_lazy('my_books')
    def post(self, request, *args, **kwargs):
        book = self.get_object()
        if book.owner != request.user:
            return PermissionDenied("You do not have permission to delete this book.")
        form = self.form_class(request.POST, request.FILES, instance=book)
        if form.is_valid():
            form.save()
            return  HttpResponseRedirect(self.success_url)
        return render(request, self.template_name, {'form': form})
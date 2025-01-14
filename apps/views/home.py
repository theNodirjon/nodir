from django.views.generic import ListView

from apps.models import Book, Category, Cart

"""
GENERIC VIEWS

TemplateView

ListView
CreateView

FormView
DetailView
UpdateView
DeleteView

"""


class HomeTemplateView(ListView):
    model = Book
    categories = Category.objects.all()
    queryset = Book.objects.filter(availability='On sale').order_by('-id')[:8]
    context_object_name = 'books'
    last_books = Book.objects.filter(availability='On sale').order_by('-average_rating')[:10]
    featured_books = Book.objects.filter(average_rating__gte=4, average_rating__lte=5,
                                         availability='On sale').order_by('-average_rating')[:4]
    extra_context = {
        'last_books': last_books,
        'featured_books': featured_books,
        'categories': categories,
    }
    template_name = 'booksaw/index.html'

    def post(self, request, *args, **kwargs):
        cart = self.request.session.get('cart', None)


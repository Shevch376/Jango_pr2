from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.views.generic import ListView

from . import forms
from .models import Book, Author, BookInstance, Genre
from django.views import generic, View
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse
import datetime


def catalog_view(request):
    # логика представления
    return render(request, 'catalog.html')


def logout_view(request):
    logout(request)
    return redirect('base_generic')


def index(request):
    """
    Функция отображения для домашней страницы сайта.
    """
    # Генерация "количеств" некоторых главных объектов
    num_genres = Genre.objects.all().count()
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    # Доступные книги (статус = 'a')
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()
    num_authors = Author.objects.count()  # Метод 'all()' применён по умолчанию.
    num_books_with_word = Book.objects.filter(title__icontains='счастье').count()

    # Number of visits to this view, as counted in the session variable.
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    # Отрисовка HTML-шаблона index.html с данными внутри переменной контекста context
    return render(
        request,
        'index.html',
        context={
            'num_books': num_books,
            'num_instances': num_instances,
            'num_instances_available': num_instances_available,
            'num_authors': num_authors,
            'num_genres': num_genres,  # Количество жанров
            'num_books_with_word': num_books_with_word,
            'num_visits': num_visits,  # num_visits appended
        }
    )


class BookListView(generic.ListView):
    model = Book
    template_name = 'catalog/book_list.html'
    context_object_name = 'book_list'


class BookDetailView(generic.DetailView):
    model = Book
    template_name = 'catalog/book_detail.html'
    context_object_name = 'book'


class AuthorListView(generic.ListView):
    model = Author
    template_name = 'catalog/author_list.html'
    context_object_name = 'authors'


class AuthorDetailView(generic.DetailView):
    model = Author
    template_name = 'catalog/author_detail.html'
    context_object_name = 'author'


class BorrowedBooksListView(PermissionRequiredMixin, generic.ListView):
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_user.html'
    permission_required = 'catalog.can_mark_returned'

    def get_queryset(self):
        # Возвращаем только книги, которые были взяты на прокат
        return BookInstance.objects.filter(status='b')


class MyView(LoginRequiredMixin, View):
    login_url = 'login/'
    redirect_field_name = 'redirect_to'

    # Поля для отображения и фильтрации
    list_display = ('book', 'status', 'borrower', 'due_back', 'id')
    list_filter = ('status', 'due_back')

    fieldsets = (
        (None, {
            'fields': ('book', 'imprint', 'id')
        }),
        ('Доступность', {
            'fields': ('status', 'due_back', 'borrower')
        }),
    )


from django.contrib.auth.decorators import permission_required
from .forms import RenewBookForm, BookForm


@permission_required('catalog.can_mark_returned')
def renew_book_librarian(request, pk):
    """
    View function for renewing a specific BookInstance by librarian
    """
    book_inst = get_object_or_404(BookInstance, pk=pk)

    # If this is a POST request then process the Form data
    if request.method == 'POST':
        # Create a form instance and populate it with data from the request (binding):
        form = RenewBookForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            book_inst.due_back = form.cleaned_data['renewal_date']
            book_inst.save()

            # redirect to a new URL:
            return HttpResponseRedirect(reverse('all-borrowed'))

    # If this is a GET (or any other method) create the default form.
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'renewal_date': proposed_renewal_date})

    return render(request, 'catalog/book_renew_librarian.html', {'form': form, 'bookinst': book_inst})


class AllBorrowedView(ListView):
    model = BookInstance
    template_name = 'catalog/all_borrowed.html'
    context_object_name = 'books'

    def get_queryset(self):
        # Возврат всех взятых книг
        return BookInstance.objects.filter(status='b')


class RenewBookView(View):
    def post(self, request, book_id):
        book_instance = get_object_or_404(BookInstance, id=book_id)
        renewal_date = request.POST.get('renewal_date')

        # Изменение даты возврата
        if renewal_date:
            book_instance.due_back = timezone.datetime.strptime(renewal_date, '%Y-%m-%d').date()
            book_instance.save()
            # Перенаправить на список всех взятых книг после продления
            return redirect('all-borrowed')

        # В случае ошибки, вы можете обработать это по-своему
        return redirect('all-borrowed')  # Или возвращать ошибку

from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Author

class AuthorCreate(CreateView):
    model = Author
    fields = '__all__'
    initial={'date_of_death':'12/10/2016',}

class AuthorUpdate(UpdateView):
    model = Author
    fields = ['first_name','last_name','date_of_birth','date_of_death']

class AuthorDelete(DeleteView):
    model = Author
    success_url = reverse_lazy('authors')

def create_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('book_list')  # Измените на нужный вам URL
    else:
        form = BookForm()
    return render(request, 'catalog/book_form.html', {'form': form})

def update_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('book_detail', pk=book.pk)  # Измените на нужный вам URL
    else:
        form = BookForm(instance=book)
    return render(request, 'catalog/book_form.html', {'form': form})

def delete_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        book.delete()
        return redirect('book_list')  # Измените на нужный вам URL
    return render(request, 'catalog/book_confirm_delete.html', {'book': book})
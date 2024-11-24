from django.urls import path, include
from . import views
from .views import BorrowedBooksListView, catalog_view
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('catalog/', views.catalog_view, name='catalog'),
    path('', views.index, name='index'),  # Путь для главной страницы
    path('books/', views.BookListView.as_view(), name='book_list'),  # Перечень книг
    path('book/<int:pk>/', views.BookDetailView.as_view(), name='book_detail'),  # Детальная информация о книге
    path('authors/', views.AuthorListView.as_view(), name='author_list'),  # Путь для списка авторов
    path('author/<int:pk>/', views.AuthorDetailView.as_view(), name='author_detail'),  # Путь для деталей автора
    path('borrowed/', BorrowedBooksListView.as_view(), name='borrowed_books'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('borrowed/list/', BorrowedBooksListView.as_view(), name='borrowed_books_list'),
]

urlpatterns += [
    path('book/<int:pk>/renew/', views.renew_book_librarian, name='renew-book-librarian'),
]

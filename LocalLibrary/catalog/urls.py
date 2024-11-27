from django.urls import path, include
from . import views
from .views import BorrowedBooksListView, catalog_view, RenewBookView, AllBorrowedView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('catalog/', views.catalog_view, name='catalog'),
    path('', views.index, name='index'),  # Путь для главной страницы
    path('book/', views.BookListView.as_view(), name='book_list'),  # Перечень книг
    path('book/<int:pk>/', views.BookDetailView.as_view(), name='book_detail'),  # Детальная информация о книге
    path('author/', views.AuthorListView.as_view(), name='author_list'),  # Путь для списка авторов
    path('author/<int:pk>/', views.AuthorDetailView.as_view(), name='author_detail'),  # Путь для деталей автора
    path('borrowed/', BorrowedBooksListView.as_view(), name='borrowed_books'),
    path('logged_out/', auth_views.LogoutView.as_view(), name='logged_out'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('borrowed/list/', BorrowedBooksListView.as_view(), name='borrowed_books_list'),
    path('all-borrowed/', AllBorrowedView.as_view(), name='all-borrowed'),  # URL для всех взятых книг
    path('book/<uuid:book_id>/renew/', RenewBookView.as_view(), name='book_renew_librarian')
]

urlpatterns += [
    path('book/<uuid:pk>/renew/', views.renew_book_librarian, name='book_renew_librarian'),
    path('author/create/', views.AuthorCreate.as_view(), name='author_create'),
    path('author/<int:pk>/update/', views.AuthorUpdate.as_view(), name='author_update'),
    path('author/<int:pk>/delete/', views.AuthorDelete.as_view(), name='author_delete'),
    path('book/create/', views.create_book, name='book_create'),
    path('book/<int:pk>/update/', views.update_book, name='book_update'),
    path('book/<int:pk>/delete/', views.delete_book, name='book_delete'),

]

from django.contrib import admin  # Импортируем админский интерфейс Django
from .models import Author, Genre, Book, BookInstance  # Импортируем необходимые модели

admin.site.register(Genre)  # Регистрация модели Genre в админке


class AuthorAdmin(admin.ModelAdmin):  # Определяем класс для настройки админки модели Author
    list_display = ('last_name', 'first_name', 'date_of_birth', 'date_of_death')  # Поля, отображаемые в списке авторов
    fields = ['first_name', 'last_name', ('date_of_birth', 'date_of_death')]  # Поля, редактируемые на странице автора

    class BooksInline(admin.TabularInline):  # Встроенный класс для отображения книг, связанных с автором
        model = Book  # Указываем, что это модель Book
        extra = 0  # Количество пустых форм для добавления новых книг (0 означает отсутствие пустых форм)

    inlines = [BooksInline]  # Добавление встроенного списка книг на страницу редактирования автора


admin.site.register(Author, AuthorAdmin)  # Регистрация AuthorAdmin для модели Author


class BooksInstanceInline(admin.TabularInline):  # Встроенный класс для отображения экземпляров книг
    model = BookInstance  # Указываем, что это модель BookInstance
    extra = 0  # Количество пустых форм для добавления новых экземпляров книги


class BookAdmin(admin.ModelAdmin):  # Определяем класс для настройки админки модели Book
    list_display = ('title', 'author', 'display_genre')  # Поля, отображаемые в списке книг
    search_fields = ('title', 'author__last_name', 'genre__name')  # Поля для поиска по книгам
    list_filter = ('author', 'genre')  # Фильтры для удобства поиска
    inlines = [BooksInstanceInline]  # Встраивание экземпляров книги на страницу редактирования книги

    def display_genre(self, obj):  # Метод для отображения жанров книг в виде строки
        return ', '.join(str(genre) for genre in obj.genre.all())  # Возвращаем строку с жанрами

    display_genre.short_description = 'Genres'  # Заголовок для отображаемого поля


admin.site.register(Book, BookAdmin)  # Регистрация BookAdmin для модели Book


@admin.register(BookInstance)  # Декоратор для регистрации модели BookInstance с классом BookInstanceAdmin
class BookInstanceAdmin(admin.ModelAdmin):  # Определяем класс для настройки админки модели BookInstance
    list_display = ('book', 'status', 'due_back', 'id')  # Поля, отображаемые в списке экземпл
    list_display = ('book', 'status', 'borrower', 'due_back', 'id')
    list_filter = ('status', 'due_back')

    class BookInstanceAdmin(admin.ModelAdmin):
        list_display = ('book', 'status', 'borrower', 'due_back', 'id')
        list_filter = ('status', 'due_back')

        fieldsets = (
            (None, {
                'fields': ('book', 'imprint', 'id')
            }),
            ('Availability', {
                'fields': ('status', 'due_back', 'borrower')
            }),
        )









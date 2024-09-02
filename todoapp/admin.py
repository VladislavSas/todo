from django.contrib import admin
from .models import ToDo, Category

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)  # Отображает только поле 'name' в списке категорий
    search_fields = ('name',)  # Добавляет поиск по полю 'name'

@admin.register(ToDo)
class ToDoAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_complete', 'created_at')  # Отображает эти поля в списке задач
    list_filter = ('is_complete', 'categories')  # Добавляет фильтрацию по полю 'is_complete' и 'categories'
    search_fields = ('title',)  # Добавляет поиск по полю 'title'
    filter_horizontal = ('categories',)  # Отображает поле 'categories' в виде горизонтального фильтра


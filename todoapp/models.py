from django.db import models

class Category(models.Model):
    name = models.CharField('Название категории', max_length=100, unique=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name

# Модель для задач
class ToDo(models.Model):
    title = models.CharField('Названия задания', max_length=500)
    is_complete = models.BooleanField('Выполнено', default=False)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)  # Новое поле для даты и времени создания
    categories = models.ManyToManyField(Category, blank=True, verbose_name='Категории')  # Связь многие ко многим с категориями

    class Meta:
        verbose_name = 'Задание'
        verbose_name_plural = 'Задания'

    def __str__(self):
        return self.title

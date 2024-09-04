from django.db import models
from django.contrib.auth.models import User
from datetime import date

# Модель для категорий
class Category(models.Model):
    name = models.CharField('Название категории', max_length=100, unique=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name

# Модель для задач
class ToDo(models.Model):
    PRIORITY_CHOICES = [
        ('L', 'Низкий'),
        ('M', 'Средний'),
        ('H', 'Высокий'),
    ]

    title = models.CharField('Название задания', max_length=500)
    is_complete = models.BooleanField('Выполнено', default=False)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    deadline = models.DateField('Срок выполнения', null=True, blank=True)
    priority = models.CharField('Приоритет', max_length=1, choices=PRIORITY_CHOICES, default='L')
    categories = models.ManyToManyField(Category, blank=True, verbose_name='Категории')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Задание'
        verbose_name_plural = 'Задания'
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def is_overdue(self):
        if self.deadline:
            return self.deadline < date.today() and not self.is_complete
        return False





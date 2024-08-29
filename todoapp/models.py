from django.db import models

# Create your models here.

class ToDo(models.Model):
    title = models.CharField('Названия задания', max_length=500)
    is_complete = models.BooleanField('Выполнено', default=False)
    created_at = models.DateTimeField(auto_now_add=True)  # Новое поле для даты и времени создания

    class Meta:
        verbose_name = 'Задание'
        verbose_name_plural = 'Задания'

    def __str__(self):
        return self.title


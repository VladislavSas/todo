from django import forms
from .models import ToDo

class ToDoForm(forms.ModelForm):
    class Meta:
        model = ToDo
        fields = ['title', 'categories']  # Добавляем поля формы: название задачи и категории
        widgets = {
            'categories': forms.CheckboxSelectMultiple(),  # Используем виджет для множественного выбора категорий
        }

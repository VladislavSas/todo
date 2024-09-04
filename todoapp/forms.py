from django import forms
from .models import ToDo

class ToDoForm(forms.ModelForm):
    class Meta:
        model = ToDo
        fields = ['title', 'deadline', 'priority', 'categories']  # Включите все необходимые поля
        widgets = {
            'categories': forms.CheckboxSelectMultiple,  # Отображение категорий в виде чекбоксов
            'deadline': forms.DateInput(attrs={'type': 'date'}),  # Поле для ввода даты
            'priority': forms.Select(choices=ToDo.PRIORITY_CHOICES),  # Выпадающий список для выбора приоритета
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['categories'].required = False  # Категории не являются обязательным полем
        self.fields['deadline'].required = False  # Срок выполнения не является обязательным полем
        self.fields['priority'].required = False  # Приоритет не является обязательным полем

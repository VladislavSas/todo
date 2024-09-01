from django import forms
from .models import ToDo, Category

class ToDoForm(forms.ModelForm):
    class Meta:
        model = ToDo
        fields = ['title', 'categories']

    categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

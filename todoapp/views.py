from django.shortcuts import render, redirect, get_object_or_404
from .models import ToDo, Category
from .forms import ToDoForm
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

def index(request):
    query = request.GET.get('q')
    if query:
        todos = ToDo.objects.filter(title__icontains=query)
    else:
        todos = ToDo.objects.all()
    categories = Category.objects.all()  # Получение всех категорий для отображения в форме
    return render(request, 'todoapp/index.html', {'todo_list': todos, 'title': 'Главная страница', 'categories': categories})

@require_http_methods(['POST'])
@csrf_exempt
def add(request):
    form = ToDoForm(request.POST)
    if form.is_valid():
        form.save()
    return redirect('index')

def update(request, todo_id):
    todo = get_object_or_404(ToDo, id=todo_id)
    todo.is_complete = not todo.is_complete
    todo.save()
    return redirect('index')

def delete(request, todo_id):
    todo = get_object_or_404(ToDo, id=todo_id)
    todo.delete()
    return redirect('index')

def edit(request, todo_id):
    todo = get_object_or_404(ToDo, id=todo_id)
    if request.method == 'POST':
        form = ToDoForm(request.POST, instance=todo)
        if form.is_valid():
            form.save()
            return redirect('index')
        else:
            return render(request, 'todoapp/index.html', {'form': form, 'todo': todo, 'error': 'Исправьте ошибки в форме.'})
    else:
        form = ToDoForm(instance=todo)
    categories = Category.objects.all()  # Получение всех категорий для отображения в форме
    return render(request, 'todoapp/index.html', {'form': form, 'todo': todo, 'categories': categories})

from django.shortcuts import render, redirect, get_object_or_404
from .models import ToDo, Category
from .forms import ToDoForm
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

def index(request):
    query = request.GET.get('q')
    selected_categories = request.GET.getlist('categories')

    # Сортировка по дате создания в убывающем порядке
    todos = ToDo.objects.all().order_by('-created_at')

    if query:
        todos = todos.filter(title__icontains=query)

    if selected_categories:
        todos = todos.filter(categories__id__in=selected_categories).distinct()

    categories = Category.objects.all()  # Получение всех категорий для отображения в форме
    return render(request, 'todoapp/index.html', {
        'todo_list': todos,
        'title': 'Главная страница',
        'categories': categories,
        'selected_categories': selected_categories,
    })

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
            return render(request, 'todoapp/index.html', {
                'form': form,
                'todo': todo,
                'error': 'Исправьте ошибки в форме.',
                'categories': Category.objects.all(),
            })
    else:
        form = ToDoForm(instance=todo)
        categories = Category.objects.all()
    return render(request, 'todoapp/index.html', {
        'form': form,
        'todo': todo,
        'categories': categories,
    })

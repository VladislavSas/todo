from django.shortcuts import render, redirect, get_object_or_404
from .models import ToDo, Category
from .forms import ToDoForm
from django.views.decorators.http import require_http_methods
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login as auth_login

@login_required
def index(request):
    query = request.GET.get('q')
    selected_categories = request.GET.getlist('categories')
    selected_deadline = request.GET.get('deadline')

    # Фильтрация пустых значений из selected_categories
    selected_categories = [cat for cat in selected_categories if cat.isdigit()]

    todos = ToDo.objects.filter(user=request.user).order_by('-created_at')

    if query:
        todos = todos.filter(title__icontains=query)

    if selected_categories:
        todos = todos.filter(categories__id__in=selected_categories).distinct()

    if selected_deadline:
        try:
            deadline_date = datetime.strptime(selected_deadline, '%Y-%m-%d').date()
            todos = todos.filter(deadline__lte=deadline_date)
        except ValueError:
            # Если формат даты неверный, просто не применяем фильтр
            pass

    categories = Category.objects.all()
    return render(request, 'todoapp/index.html', {
        'todo_list': todos,
        'title': 'Главная страница',
        'categories': categories,
        'selected_categories': selected_categories,
        'selected_deadline': selected_deadline,
    })

@login_required
@require_http_methods(['POST'])
def add(request):
    form = ToDoForm(request.POST)
    if form.is_valid():
        todo = form.save(commit=False)
        todo.user = request.user  # Присваиваем текущего пользователя
        todo.save()  # Сначала сохраняем задачу
        form.save_m2m()  # Затем сохраняем многие ко многим поля (категории)
        return redirect('index')
    else:
        todos = ToDo.objects.filter(user=request.user).order_by('-created_at')
        categories = Category.objects.all()
        return render(request, 'todoapp/index.html', {
            'todo_list': todos,
            'form': form,
            'title': 'Главная страница',
            'categories': categories,
            'selected_categories': request.GET.getlist('categories'),
        })

@login_required
def update(request, todo_id):
    todo = get_object_or_404(ToDo, id=todo_id, user=request.user)
    todo.is_complete = not todo.is_complete
    todo.save()
    return redirect('index')

@login_required
def delete(request, todo_id):
    todo = get_object_or_404(ToDo, id=todo_id, user=request.user)
    todo.delete()
    return redirect('index')

@login_required
def edit(request, todo_id):
    todo = get_object_or_404(ToDo, id=todo_id, user=request.user)
    if request.method == 'POST':
        form = ToDoForm(request.POST, instance=todo)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = ToDoForm(instance=todo)
    return render(request, 'todoapp/edit.html', {
        'form': form,
        'todo': todo,
        'categories': Category.objects.all(),
    })

@login_required
def calendar_view(request):
    todo_list = ToDo.objects.filter(user=request.user)
    return render(request, 'todoapp/calendar.html', {'todo_list': todo_list})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)  # Автоматически входить в систему после регистрации
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

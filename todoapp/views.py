from django.shortcuts import render, redirect, get_object_or_404
from .models import ToDo, Category
from .forms import ToDoForm
from django.views.decorators.http import require_http_methods
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login as auth_login
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


@login_required
def index(request):
    query = request.GET.get('q')
    selected_categories = request.GET.getlist('categories')
    selected_deadline = request.GET.get('deadline')
    status = request.GET.get('status')
    priority = request.GET.get('priority')

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

    if status:
        if status == 'complete':
            todos = todos.filter(is_complete=True)
        elif status == 'incomplete':
            todos = todos.filter(is_complete=False)

    if priority:
        todos = todos.filter(priority=priority)

    categories = Category.objects.all()
    return render(request, 'todoapp/index.html', {
        'todo_list': todos,
        'title': 'Главная страница',
        'categories': categories,
        'selected_categories': selected_categories,
        'selected_deadline': selected_deadline,
        'status': status,
        'priority': priority,
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
@csrf_exempt  # Отключение проверки CSRF для AJAX
def edit_ajax(request):
    if request.method == 'POST':
        todo_id = request.POST.get('id')
        todo = get_object_or_404(ToDo, id=todo_id, user=request.user)
        form = ToDoForm(request.POST, instance=todo)

        if form.is_valid():
            form.save()
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'status': 'error', 'errors': form.errors})

    return JsonResponse({'status': 'invalid request'}, status=400)

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

@login_required
def statistics(request):
    user = request.user

    # Получаем все задачи пользователя
    todos = ToDo.objects.filter(user=user)

    # Общая статистика
    total_tasks = todos.count()
    completed_tasks = todos.filter(is_complete=True).count()
    incomplete_tasks = total_tasks - completed_tasks

    # Статистика по приоритетам
    priority_stats = {
        'L': todos.filter(priority='L').count(),
        'M': todos.filter(priority='M').count(),
        'H': todos.filter(priority='H').count(),
        'None': todos.filter(priority__isnull=True).count()
    }

    # Статистика по статусам
    status_stats = {
        'Completed': completed_tasks,
        'Incomplete': incomplete_tasks
    }

    # Статистика по категориям
    categories = Category.objects.all()
    category_stats = {}
    for category in categories:
        category_stats[category.name] = todos.filter(categories=category).count()

    return render(request, 'todoapp/statistics.html', {
        'total_tasks': total_tasks,
        'completed_tasks': completed_tasks,
        'incomplete_tasks': incomplete_tasks,
        'priority_stats': priority_stats,
        'status_stats': status_stats,
        'category_stats': category_stats
    })


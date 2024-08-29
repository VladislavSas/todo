from django.shortcuts import render, redirect
from .models import ToDo
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

def index(request):
    query = request.GET.get('q')
    if query:
        todos = ToDo.objects.filter(title__icontains=query)
    else:
        todos = ToDo.objects.all()
    return render(request, 'todoapp/index.html', {'todo_list': todos, 'title': 'Главная страница'})

@require_http_methods(['POST'])
@csrf_exempt
def add(request):
    title = request.POST['title']
    todo = ToDo(title=title)
    todo.save()
    return redirect('index')

def update(request, todo_id):
    todo = ToDo.objects.get(id=todo_id)
    todo.is_complete = not todo.is_complete
    todo.save()
    return redirect('index')

def delete(request, todo_id):
    todo = ToDo.objects.get(id=todo_id)
    todo.delete()
    return redirect('index')

def edit(request, todo_id):
    todo = ToDo.objects.get(id=todo_id)
    if request.method == 'POST':
        new_title = request.POST.get('title')
        if new_title:
            todo.title = new_title
            todo.save()
            return redirect('index')
        else:
            return render(request, 'todoapp/index.html', {'todo': todo, 'error': 'Заголовок не может быть пустым.'})
    return render(request, 'todoapp/index.html', {'todo': todo})

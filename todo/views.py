from django.shortcuts import render, redirect
from django.http import Http404
from django.utils.timezone import make_aware, now
from django.utils.dateparse import parse_datetime
from todo.models import Task

# Create your views here.
def index(request):
    if request.method == 'POST':
        task = Task(title=request.POST['title'],
                    due_at=make_aware(parse_datetime(request.POST['due_at'])))
        task.save()

    status = request.GET.get('status', 'all')
    if status == 'completed':
        tasks = Task.objects.filter(completed=True)
    elif status == 'not_completed':
        tasks = Task.objects.filter(completed=False)
    else:
        tasks = Task.objects.all()

    if request.GET.get('order') == 'due':
        tasks = tasks.order_by('due_at')
    else:
        tasks = tasks.order_by('-posted_at')

    context = {
        'tasks': tasks,
        'now': now(),
    }
    return render(request, 'todo/index.html', context)


def detail(request, task_id):
    try:
        task = Task.objects.get(pk=task_id)
    except Task.DoesNotExist:
        raise Http404("Task does not exist")

    context = {
        'task': task,
        'now': now(),
    }
    return render(request, 'todo/detail.html', context)


def update(request, task_id):
    try:
        task = Task.objects.get(pk=task_id)
    except Task.DoesNotExist:
        raise Http404("Task does not exist")
    if request.method == 'POST':
        task.title = request.POST ['title']
        task.due_at = make_aware(parse_datetime(request.POST['due_at']))
        task.save()
        return redirect(detail, task_id)
    
    context = {
        'task': task
    }
    return render(request, "todo/edit.html", context)


def close(request, task_id):
    try:
        task = Task.objects.get(pk=task_id)
    except Task.DoesNotExist:
        raise Http404("Task does not exist")
    task.completed = True
    task.save()
    return redirect(index)


def delete(request, task_id):
    try:
        task = Task.objects.get(pk=task_id)
    except Task.DoesNotExist:
        raise Http404("Task does not exist")
    task.delete()
    return redirect('index')

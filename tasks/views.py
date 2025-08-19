from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Task
from .forms import TaskForm

def home(request):
    query = request.GET.get('q')
    filter_status = request.GET.get('filter')

    tasks = Task.objects.order_by('is_completed', '-created_at')  # order first by pending, then latest

    if query:
        tasks = tasks.filter(title__icontains=query)

    if filter_status == "completed":
        tasks = tasks.filter(is_completed=True)
    elif filter_status == "pending":
        tasks = tasks.filter(is_completed=False)

    form = TaskForm()
    return render(request, 'tasks/home.html', {'tasks': tasks, 'form': form})

def add_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Task added!")
        else:
            messages.error(request, "Please correct the error.")
    return redirect('home')

def toggle_task(request, pk):
    task = get_object_or_404(Task, pk=pk)
    task.is_completed = not task.is_completed
    task.save()
    return redirect('home')

def delete_task(request, pk):
    task = get_object_or_404(Task, pk=pk)
    task.delete()
    messages.success(request, "Task deleted!")
    return redirect('home')

def edit_task(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, "Task updated!")
            return redirect('home')
    else:
        form = TaskForm(instance=task)
    return render(request, 'tasks/edit_task.html', {'form': form, 'task': task})
from django.http import JsonResponse

def search_tasks(request):
    query = request.GET.get('q', '')
    filter_status = request.GET.get('filter', '')

    tasks = Task.objects.order_by('is_completed', '-created_at')

    if query:
        tasks = tasks.filter(title__icontains=query)

    if filter_status == "completed":
        tasks = tasks.filter(is_completed=True)
    elif filter_status == "pending":
        tasks = tasks.filter(is_completed=False)

    # return as JSON
    data = []
    for t in tasks:
        data.append({
            "id": t.id,
            "title": t.title,
            "is_completed": t.is_completed
        })
    return JsonResponse({"tasks": data})


def edit_task_inline(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == "POST":
        title = request.POST.get("title")
        if title:
            task.title = title
            task.save()
            return JsonResponse({"success": True, "title": task.title})
    return JsonResponse({"success": False})

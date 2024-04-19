# project/views.py

from django.shortcuts import render, get_object_or_404, redirect
from .models import Project, TodoTask
from .forms import ProjectForm, TodoTaskForm
import requests
from .models import Gist
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponse

def export_gist(request):
    if request.method == 'POST':
        gist_url = request.POST.get('gist_url')
        response = requests.get(gist_url)
        if response.status_code == 200:
            data = response.json()
            filename = data['files'].keys()[0]
            content = data['files'][filename]['content']
            # Save the content to a markdown file
            gist = Gist.objects.create(filename=filename, content=content)
            return HttpResponse("Gist exported successfully!")
        else:
            return HttpResponse("Failed to export gist.")
    return render(request, 'export_gist.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('project_list')  # Redirect to the desired page after login
        else:
            return render(request, 'login.html', {'error_message': 'Invalid credentials'})
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def project_list(request):
    projects = Project.objects.all()
    return render(request, 'project_list.html', {'projects': projects})

@login_required
def project_detail(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    tasks = TodoTask.objects.filter(project=project)

    # Calculate the number of completed todos
    completed_todos_count = tasks.filter(status=True).count()

    # Calculate the total number of todos
    total_todos_count = tasks.count()

    return render(request, 'detail.html', {
        'project': project,
        'tasks': tasks,
        'completed_todos_count': completed_todos_count,
        'total_todos_count': total_todos_count,
    })

@login_required
def project_add(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('project_list')
    else:
        form = ProjectForm()
    return render(request, 'project_form.html', {'form': form})

@login_required
def project_edit(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            return redirect('project_detail', project_id=project_id)
    else:
        form = ProjectForm(instance=project)
    return render(request, 'project_form.html', {'form': form})

@login_required
def project_delete(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    if request.method == 'POST':
        project.delete()
        return redirect('project_list')
    return render(request, 'project_confirm_delete.html', {'project': project})

@login_required
def task_add(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    if request.method == 'POST':
        form = TodoTaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.project = project
            task.save()
            return redirect('project_detail', project_id=project_id)
    else:
        form = TodoTaskForm()
    return render(request, 'task_form.html', {'form': form, 'project': project})

@login_required
def task_edit(request, project_id, task_id):
    project = get_object_or_404(Project, pk=project_id)
    task = get_object_or_404(TodoTask, pk=task_id)
    if request.method == 'POST':
        form = TodoTaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('project_detail', project_id=project_id)
    else:
        form = TodoTaskForm(instance=task)
    return render(request, 'task_form.html', {'form': form, 'project': project})

@login_required
def task_delete(request, project_id, task_id):
    task = get_object_or_404(TodoTask, pk=task_id)
    if request.method == 'POST':
        task.delete()
        return redirect('project_detail', project_id=project_id)
    return render(request, 'task_confirm_delete.html', {'task': task})


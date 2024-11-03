from django.shortcuts import render, redirect, get_object_or_404
from .models import Task, Category
from .forms import TaskForm, CategoryForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

# Create your views here.
def home(request):
     return render(request, 'todo/home.html')

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'todo/login.html', {'form': form})
    
def user_signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'todo/signup.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('home')

def task_list(request):
    tasks = Task.objects.all()
    return render(request, 'todo/task-list.html', {'tasks': tasks})

def category_list(request):
    category = Category.objects.all()
    return render(request, 'todo/category-list.html', {'categories': category})

@login_required
def add_task(request):
     if request.method == 'POST':
          form = TaskForm(request.POST)
          if form.is_valid():
               task = form.save(commit=False)
               task.user = request.user
               task.save()
               return redirect('task_list')
     else:
          form = TaskForm()
     return render(request, 'todo/add-task.html', {'form': form})

@login_required
def edit_task(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('task_list')  # Redirect to the task list after saving changes
    else:
        form = TaskForm(instance=task)
    return render(request, 'todo/edit_task.html', {'form': form})

@login_required
def delete_task(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('task_list')  # Redirect to the task list after deletion
    return render(request, 'todo/delete_task.html', {'task': task})

@login_required
def add_category(request):
     if request.method == 'POST':
          form = CategoryForm(request.POST)
          if form.is_valid():
               category = form.save(commit=False)
               category.user = request.user
               category.save()
               return redirect('category_list')
     else:
          form = CategoryForm()
     return render(request, 'todo/add-category.html', {'form': form})
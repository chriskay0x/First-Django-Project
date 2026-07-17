from django.shortcuts import render, redirect
from datetime import datetime
from .models import Task
from .forms import TaskForm, RegisterForm
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Create your views here.
def register_view(request):
    if request.user.is_authenticated:
        messages.warning(request, 'Already Signed In!')
        return redirect('home')
    
    form = RegisterForm()
    errors = None
    
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user)
                messages.success(request, 'Account created and login successful!')
                return redirect('home')
            else:
                messages.error(request, 'Account creation failed. Please try again.')
                return redirect('login')
        else:
            errors = form.errors.as_data()
            messages.error(request, errors)
            return redirect('register')
        
    context = {
        'form': form,
        'errors': errors
    }
    return render(request, 'register.html', context)


@login_required(login_url='login')
def home(request):
    date = datetime.now()
    h = int(date.strftime('%H'))
    
    msg = "Good "
    if h < 12:
        msg += "Morning"
    elif h < 16:
        msg += "Afternoon"
    elif h < 18:
        msg += "Evening"
    else:
        msg += "Night"
     
    greeting = f"{msg}! Christian"
    
    tasks = Task.objects.all()
    
    context = {
        'greeting': greeting,
        'tasks': tasks
    }
    return render(request, 'home.html', context)

def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
    
        if user is not None:
            login(request, user)
            messages.success(request, "Login Successful!")
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password!")
            return redirect('login')
    
    return render(request, 'login.html')


def logout_view(request):
    user = request.user
    logout(request)
    messages.success(request, "You've been logged out!")
    return redirect('login')


def add_task(request):
    forms = TaskForm()
    if request.method == "POST":
        # title = request.POST.get('title')
        # due_time = request.POST.get('due_time')
        
        # task = Task.objects.create(
        #     title=title,
        #     due_time=due_time
        # )
        # task.save()
        
        forms = TaskForm(request.POST)
        # ============================= #
        #  Check for form validation
        # ============================ #
        if form.is_valid():
            instance = forms.save(commit=False)
            instance.user = request.user
            instance.save()
            messages.success(request, "Task added successfully!")
            return redirect('home')
        else:
            messages.error(request, "Error adding task. Please check the form.")
            return redirect('add_task')
    context = {
        'forms':forms
    }
        
    return render(request, 'add_task.html', context)

def filter_tasks(request, foo):
    # Fixed lowercase 'task' to capitalized 'Task'
    if foo == "true":
        tasks = Task.objects.filter(done=True)
    elif foo == "false":
        tasks = Task.objects.filter(done=False)
    else:
        tasks = Task.objects.all() # Fallback instead of 'pass' to prevent UnboundLocalError
    
    context = {
        'tasks': tasks
    }
    return render(request, 'home.html', context)


@login_required(login_url='login')
def update_task(request, pk):
    # task = Task.objects.get(id=pk)
    task = get_object_or_404(Task, id=pk, user=request.user)
    form = TaskForm(instance=task)
    
    if request.method == "POST":
        # title = request.POST.get('title')
        # done = request.POST.get('done')
        # due_time = request.POST.get('due_time')
        
        # Assign values to task
        # task.title = title
        # if done:
        #     task.done = True
        # else:
        #     task.done = False
            
        # if due_time:
        #     task.due_time = due_time
        
        # # save task
        # task.save()
        
        form = TaskForm(request.POST, instance=task)
        
        if form.is_valid():
            form.save
            messages.success('Successfully updated task')
            return redirect('home')
        else:
            errors = form.errors.as_data()
            return redirect('task', pk=pk)
        
    context = {
        'task':task,
        'form':form
    }
        
    return render(request, 'update_task.html', context)

@login_required(login_url='login')
def delete_task(request, pk):
    task = get_object_or_404(Task, id=pk)
    task.delete()
    return redirect('home')



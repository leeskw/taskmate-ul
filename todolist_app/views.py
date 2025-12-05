from django import forms
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db import models
from django.http import HttpResponse
from django.shortcuts import redirect, render

from todolist_app.forms import TaskForm
from todolist_app.models import TaskList


@login_required
def todolist(request):
    if request.method == "POST":
        form = TaskForm(request.POST or None)
        if form.is_valid():
            # Save the form with commit=False to get the instance without saving to DB
            task = form.save(commit=False)

            # Make additional modifications to the task instance
            task.manage = request.user  # Assign the current user as the manage

            # Now, save the article instance to the database
            task.save()

        messages.success(request, 'New Task Added!')
        return redirect('todolist')
    else:
        # order_by() --> ADDED BY ME, '.' good practice.
        # all_tasks = TaskList.objects.filter(manage=request.user).order_by('id')
        all_tasks = TaskList.objects.filter(manage=request.user)
        paginator = Paginator(all_tasks, 10)
        page = request.GET.get('pg')
        all_tasks = paginator.get_page(page)  # Return a valid page

        context = {
            'all_tasks': all_tasks
        }
        return render(request, 'todolist.html', context)


@login_required
def delete_task(request, task_id):
    task = TaskList.objects.get(pk=task_id)
    # --- RESTRICTION CHECK ---
    if task.manage == request.user:
        task.delete()
    # User is NOT the owner, deny access and show error message
    else:
        messages.error(request, ("Access Restricted. You Are Not Allowed!"))

    return redirect('todolist')


@login_required
def edit_task(request, task_id):
    if request.method == "POST":
        task = TaskList.objects.get(pk=task_id)
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()

        messages.success(request, 'Task Edited!')
        return redirect('todolist')
    else:
        task_obj = TaskList.objects.get(pk=task_id)
        context = {
            'task_obj': task_obj
        }
        return render(request, 'edit.html', context)


@login_required
def complete_task(request, task_id):
    task = TaskList.objects.get(pk=task_id)
    # --- RESTRICTION CHECK ---
    if task.manage == request.user:
        task.done = True
        task.save()
    # User is NOT the owner, deny access and show error message
    else:
        messages.error(request, "Access Restricted. You Are Not Allowed!")

    return redirect('todolist')


@login_required
def pending_task(request, task_id):
    task = TaskList.objects.get(pk=task_id)
    # --- RESTRICTION CHECK ---
    if task.manage == request.user:
        task.done = False
        task.save()
    # User is NOT the owner, deny access and show error message
    else:
        messages.error(request, "Access Restricted. You Are Not Allowed!")

    return redirect('todolist')


def index(request):
    context = {
        'index_text': 'Welcome Index Page'
    }
    return render(request, 'index.html', context)


def contact(request):
    context = {
        'contact_text': 'Welcome Contact Page'
    }
    return render(request, 'contact.html', context)


def about(request):
    context = {
        'about_text': 'Welcome About Page'
    }
    return render(request, 'about.html', context)


"""
======
AI 개요
======
The commit=False argument in Django's ModelForm.save() method allows for 
retrieving the model instance from the form without saving it to the database immediately. 
This is useful when additional modifications or assignments need to be made to the instance 
before it is persisted.
Here is an example:
# models.py


class Article(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


# forms.py


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        # 'author' is excluded as it will be set manually
        fields = ['title', 'content']


# views.py


def create_article(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            # Save the form with commit=False to get the instance without saving to DB
            article = form.save(commit=False)

            # Make additional modifications to the article instance
            article.author = request.user  # Assign the current user as the author

            # Now, save the article instance to the database
            article.save()

            return redirect('article_detail', pk=article.pk)
    else:
        form = ArticleForm()
    return render(request, 'create_article.html', {'form': form})
"""

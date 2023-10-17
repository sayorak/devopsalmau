from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import Problem, UserAction
from django.contrib.auth.models import User, Group
from .forms import ProblemForm, UserActionForm
import random


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('problem_list')
    else:
        form = AuthenticationForm()
    return render(request, 'helper/login.html', {'form': form})


def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('problem_list')
    else:
        form = UserCreationForm()
    return render(request, 'helper/register.html', {'form': form})


@login_required
def problem_list(request):
    problems = Problem.objects.filter(user=request.user)

    return render(request, 'helper/problem_list.html', {'problems': problems})


def create_problem(request):
    if request.method == 'POST':
        form = ProblemForm(request.POST)
        if form.is_valid():
            problem = form.save(commit=False)
            reception_group = Group.objects.get(name='Reception')
            reception_users = reception_group.user_set.all()
            random_user = random.choice(reception_users)
            problem.user = random_user
            problem.save()
            return redirect('problem_list')
    else:
        form = ProblemForm()
    return render(request, 'helper/create_problem.html', {'form': form})


@login_required
def view_problem(request, problem_id):
    problem = get_object_or_404(Problem, id=problem_id, user=request.user)
    user_action_form = UserActionForm()

    reception_group = Group.objects.get(name='Reception')

    users = reception_group.user_set.all()
    tester_group = Group.objects.get(name='Tester')

    if request.method == 'POST':
        action = request.POST.get('action')
        if action:
            problem.action = action
            problem.save()
            return redirect('view_problem', problem_id=problem.id)

        assigned_to = request.POST.get('assigned_to')
        if assigned_to:
            user = User.objects.get(id=assigned_to)
            problem.user = user
            problem.save()
            return redirect('problem_list')

        status = request.POST.get('status')
        if status == 'resolved':
            tester_users = tester_group.user_set.all()
            if tester_users:
                random_tester = random.choice(tester_users)
                problem.user = random_tester
                problem.resolved_user = request.user
            else:
                problem.user = None
            problem.status = 'resolved'
            problem.save()
        if status != 'resolved' and status:
            problem.status = status
            problem.save()
            return redirect('problem_list')

    return render(request, 'helper/view_problem.html',
                  {'problem': problem, 'user_action_form': user_action_form, 'users': users})


@login_required
def logout_view(request):
    logout(request)
    return redirect('login_view')

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import CustomPasswordChangeForm, LoginForm, ProfileEditForm, RegistrationForm
from .models import User
from .service import paginate_queryset


def user_register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('users:login')
    else:
        form = RegistrationForm()
    return render(request, 'users/register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('projects:project_list')
        messages.error(request, 'Неверный email или пароль')
    form = LoginForm()
    return render(request, 'users/login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('users:login')


def user_list(request):
    filter_type = request.GET.get('filter', '')
    users = User.objects.all().order_by('-date_joined')
    if request.user.is_authenticated and filter_type:
        if filter_type == 'favorite_authors':
            fav_projects = request.user.favorites.all()
            users = User.objects.filter(
                owned_projects__in=fav_projects
            ).distinct().order_by('-date_joined')
        elif filter_type == 'participated_authors':
            users = User.objects.filter(
                owned_projects__participants=request.user
            ).distinct().order_by('-date_joined')
        elif filter_type == 'liked_my_projects':
            my_projects = request.user.owned_projects.all()
            users = User.objects.filter(
                favorites__in=my_projects
            ).distinct().order_by('-date_joined')
        elif filter_type == 'my_participants':
            my_projects = request.user.owned_projects.all()
            users = User.objects.filter(
                participated_projects__in=my_projects
            ).distinct().order_by('-date_joined')
    page_obj = paginate_queryset(users, request.GET.get('page'))
    return render(request, 'users/participants.html', {
        'participants': page_obj,
        'page_obj': page_obj,
        'active_filter': filter_type,
    })


def user_detail(request, pk):
    profile_user = get_object_or_404(User, pk=pk)
    return render(request, 'users/user-details.html', {'user': profile_user})


@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = ProfileEditForm(
            request.POST, request.FILES, instance=request.user
        )
        if form.is_valid():
            form.save()
            return redirect('users:detail', pk=request.user.pk)
    else:
        form = ProfileEditForm(instance=request.user)
    return render(request, 'users/edit-profile.html', {'form': form})


@login_required
def change_password(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            return redirect('users:login')
    else:
        form = CustomPasswordChangeForm(request.user)
    return render(request, 'users/change-password.html', {'form': form})

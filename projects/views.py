from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator
from django.http import JsonResponse
from .models import Project
from .forms import ProjectForm

PAGINATE_BY = 12


def project_list(request):
    projects_qs = Project.objects.select_related('owner').all()
    paginator = Paginator(projects_qs, PAGINATE_BY)
    page_obj = paginator.get_page(request.GET.get('page'))
    return render(request, 'projects/project_list.html', {
        'projects': page_obj,
        'page_obj': page_obj,
    })


def project_detail(request, pk):
    project = get_object_or_404(Project.objects.select_related('owner'), pk=pk)
    return render(request, 'projects/project-details.html', {'project': project})


@login_required
def project_create(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = request.user
            project.save()
            return redirect('projects:project_detail', pk=project.pk)
    else:
        form = ProjectForm()
    return render(request, 'projects/create-project.html', {'form': form, 'is_edit': False})


@login_required
def project_edit(request, pk):
    project = get_object_or_404(Project, pk=pk, owner=request.user)
    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            return redirect('projects:project_detail', pk=project.pk)
    else:
        form = ProjectForm(instance=project)
    return render(request, 'projects/create-project.html', {
        'form': form, 'project': project, 'is_edit': True,
    })


@login_required
@require_POST
def project_complete(request, pk):
    project = get_object_or_404(Project, pk=pk, owner=request.user)
    project.status = Project.STATUS_CLOSED
    project.save()
    return JsonResponse({'status': 'ok'})


@login_required
@require_POST
def toggle_participate(request, pk):
    project = get_object_or_404(Project, pk=pk)
    user = request.user
    if user == project.owner:
        return JsonResponse({'status': 'error'}, status=400)
    if project.participants.filter(pk=user.pk).exists():
        project.participants.remove(user)
        participating = False
    else:
        project.participants.add(user)
        participating = True
    return JsonResponse({'status': 'ok', 'participant': participating})


@login_required
@require_POST
def toggle_favorite(request, pk):
    project = get_object_or_404(Project, pk=pk)
    user = request.user
    if user.favorites.filter(pk=pk).exists():
        user.favorites.remove(project)
        added = False
    else:
        user.favorites.add(project)
        added = True
    return JsonResponse({'status': 'ok', 'added': added})


@login_required
def favorite_projects(request):
    favorites_qs = request.user.favorites.select_related('owner').all()
    paginator = Paginator(favorites_qs, PAGINATE_BY)
    page_obj = paginator.get_page(request.GET.get('page'))
    return render(request, 'projects/favorite_projects.html', {
        'projects': page_obj,
        'page_obj': page_obj,
    })

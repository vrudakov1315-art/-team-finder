from http import HTTPStatus

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .constants import PAGINATE_BY
from .forms import ProjectForm
from .models import Project
from .service import paginate_queryset


def project_list(request):
    projects_qs = Project.objects.select_related('owner').prefetch_related('participants').all()
    page_obj = paginate_queryset(projects_qs, request.GET.get('page'), PAGINATE_BY)
    return render(request, 'projects/project_list.html', {
        'projects': page_obj,
        'page_obj': page_obj,
    })


def project_detail(request, pk):
    project = get_object_or_404(
        Project.objects.select_related('owner').prefetch_related('participants'),
        pk=pk
    )
    return render(request, 'projects/project-details.html', {'project': project})


@login_required
def project_create(request):
    form = ProjectForm(request.POST or None)
    if form.is_valid():
        project = form.save(commit=False)
        project.owner = request.user
        project.save()
        return redirect('projects:project_detail', pk=project.pk)
    return render(request, 'projects/create-project.html', {'form': form, 'is_edit': False})


@login_required
def project_edit(request, pk):
    project = get_object_or_404(Project, pk=pk, owner=request.user)
    form = ProjectForm(request.POST or None, instance=project)
    if form.is_valid():
        form.save()
        return redirect('projects:project_detail', pk=project.pk)
    return render(request, 'projects/create-project.html', {
        'form': form,
        'project': project,
        'is_edit': True,
    })


@login_required
@require_POST
def project_complete(request, pk):
    project = get_object_or_404(Project, pk=pk, owner=request.user)
    if project.status != Project.STATUS_OPEN:
        return JsonResponse(
            {'status': 'error', 'message': 'Project is already closed'},
            status=HTTPStatus.BAD_REQUEST
        )
    project.status = Project.STATUS_CLOSED
    project.save()
    return JsonResponse({'status': 'ok', 'project_status': 'closed'})


@login_required
@require_POST
def toggle_participate(request, pk):
    project = get_object_or_404(Project, pk=pk)
    user = request.user
    is_participant = project.participants.filter(pk=user.pk).exists()
    if is_participant:
        project.participants.remove(user)
        participant = False
    else:
        project.participants.add(user)
        participant = True
    return JsonResponse(
        {'status': 'ok', 'participant': participant},
        status=HTTPStatus.OK
    )


@login_required
@require_POST
def toggle_favorite(request):
    project_id = request.POST.get('project_id')
    project = get_object_or_404(Project, pk=project_id)
    user = request.user
    is_favorited = user.favorites.filter(pk=project.pk).exists()
    if is_favorited:
        user.favorites.remove(project)
        favorited = False
    else:
        user.favorites.add(project)
        favorited = True
    return JsonResponse(
        {'status': 'ok', 'favorited': favorited},
        status=HTTPStatus.OK
    )


@login_required
def favorite_projects(request):
    favorites_qs = request.user.favorites.select_related('owner').prefetch_related('participants').all()
    page_obj = paginate_queryset(favorites_qs, request.GET.get('page'), PAGINATE_BY)
    return render(request, 'projects/favorite_projects.html', {
        'projects': page_obj,
        'page_obj': page_obj,
    })

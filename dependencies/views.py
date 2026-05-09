from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
import json
from .models import TeamDependency
from .forms import TeamDependencyForm
from teams.models import Team

@login_required
def dependency_list(request):
    user = request.user
    dependencies = TeamDependency.objects.all()
    teams = Team.objects.all()
    
    # Prepare data for visualization
    nodes = []
    edges = []
    
    for team in teams:
        nodes.append({
            'id': str(team.id),
            'label': team.teamName,
            'department': team.department.departmentName if team.department else 'Unknown',
        })
    
    for dep in dependencies:
        edges.append({
            'from': str(dep.from_team.id),
            'to': str(dep.to_team.id),
            'type': dep.dependency_type,
            'label': dep.get_dependency_type_display(),
        })
    
    create_access = user.is_staff or user.is_superuser or user.role == 'Admin'

    return render(request, 'dependencies/dependency_list.html', {
        'dependencies': dependencies,
        'teams': teams,
        'nodes': json.dumps(nodes),
        'edges': json.dumps(edges),
        'active_page': 'dependencies',
        'create_access': create_access,
    })

@login_required
def dependency_create(request):
    if not request.user.is_staff and not request.user.is_superuser and request.user.role != 'Admin':
        messages.error(request, 'You do not have permission to create dependencies.')
        return redirect('dependencies:dependency_list')
    if request.method == 'POST':
        form = TeamDependencyForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Dependency created successfully.')
            return redirect('dependencies:dependency_list')
    else:
        form = TeamDependencyForm()
    return render(request, 'dependencies/dependency_form.html', {'form': form})

@login_required
def dependency_update(request, pk):
    dependency = get_object_or_404(TeamDependency, pk=pk)
    if not request.user.is_staff and not request.user.is_superuser and request.user.role != 'Admin':
        messages.error(request, 'You do not have permission to update dependencies.')
        return redirect('dependencies:dependency_list')
    if request.method == 'POST':
        form = TeamDependencyForm(request.POST, instance=dependency)
        if form.is_valid():
            form.save()
            messages.success(request, 'Dependency updated successfully.')
            return redirect('dependencies:dependency_list')
    else:
        form = TeamDependencyForm(instance=dependency)
    return render(request, 'dependencies/dependency_form.html', {'form': form})

@login_required
def dependency_delete(request, pk):
    dependency = get_object_or_404(TeamDependency, pk=pk)
    if not request.user.is_staff and not request.user.is_superuser and request.user.role != 'Admin':
        messages.error(request, 'You do not have permission to delete dependencies.')
        return redirect('dependencies:dependency_list')
    if request.method == 'POST':
        dependency.delete()
        messages.success(request, 'Dependency deleted successfully.')
        return redirect('dependencies:dependency_list')
    return render(request, 'dependencies/dependency_confirm_delete.html', {'dependency': dependency})

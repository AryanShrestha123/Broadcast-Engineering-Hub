from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import PermissionDenied

from django.db.models import Count, Q
from teams.models import Team
from account.models import CustomUser
from .forms import TeamForm, TeamCreateForm


def user_can_edit_team(user, team):
    return user.is_authenticated and (
        user.is_staff or user.is_superuser or getattr(user, 'role', '') == 'Admin' or user == team.teamLeader
    )


def user_is_admin(user):
    return user.is_authenticated and (user.is_staff or user.is_superuser or getattr(user, 'role', '') == 'Admin')


@login_required
def team_view(request):
    q = request.GET.get('q', '')

    teams = Team.objects.all().annotate(member_count=Count('members'))

    if q:
        teams = teams.filter(teamName__icontains=q).annotate(member_count=Count('members'))

    context = {
        'teams': teams,
        'q': q,
        'active_page': 'teams',
    }

    return render(request, 'teams/teams.html', context)

def team_detail_view(request, team_id):
    team = Team.objects.get(id=team_id)
    members = team.members.all()

    context = {
        'team': team,
        'members': members,
        'upstream_teams': team.upstream_teams,
        'downstream_teams': team.downstream_teams,
        'all_dependencies': team.all_dependencies,
        'active_page': 'teams',
    }
    return render(request, 'teams/team_detail.html', context)

def team_create_view(request):
    if not user_is_admin(request.user):
        messages.error(request, 'Only admins can create teams.')
        return redirect('teams:team_view')

    if request.method == 'POST':
        form = TeamCreateForm(request.POST)
        if form.is_valid():
            team = form.save()
            messages.success(request, 'Team created successfully.')
            return redirect('teams:team_detail_view', team_id=team.id)
    else:
        form = TeamCreateForm()

    context = {
        'form': form,
        'title': 'Create Team',
        'active_page': 'teams',
    }
    return render(request, 'teams/team_form.html', context)

@login_required
def team_edit_view(request, team_id):
    team = get_object_or_404(Team, id=team_id)
    if not user_can_edit_team(request.user, team):
        messages.error(request, 'You do not have permission to edit this team.')
        return redirect('teams:team_detail_view', team_id=team.id)

    if request.method == 'POST':
        form = TeamForm(request.POST, instance=team)
        if form.is_valid():
            form.save()
            messages.success(request, 'Team details updated successfully.')
            return redirect('teams:team_detail_view', team_id=team.id)
    else:
        form = TeamForm(instance=team)

    context = {
        'team': team,
        'form': form,
        'title': 'Edit Team',
        'active_page': 'teams',
    }
    return render(request, 'teams/team_form.html', context)
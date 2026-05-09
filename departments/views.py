from django.shortcuts import render, get_object_or_404
from django.db.models import Count
from django.contrib.auth.decorators import login_required

from .models import Department

# Create your views here.
@login_required
def department_view(request):
    departments = Department.objects.annotate(
        team_count=Count('teams', distinct=True),
        member_count=Count('teams__members', distinct=True)
    ).order_by('departmentName')

    context = {
        'departments': departments,
        'active_page': 'departments',
    }
    return render(request, 'departments/departments.html', context)


@login_required
def department_detail_view(request, department_id):
    department = get_object_or_404(Department, id=department_id)

    teams = department.teams.all().annotate(member_count=Count('members', distinct=True)).order_by('teamName')

    teams_count = teams.count()

    members_count = (
        teams.aggregate(total=Count('members', distinct=True))['total'] or 0
    )

    context = {
        'department': department,
        'teams': teams,
        'teams_count': teams_count,
        'members_count': members_count,
        'active_page': 'departments',
    }

    return render(request, 'departments/department_detail.html', context)
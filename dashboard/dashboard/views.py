from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from teams.models import Team
from departments.models import Department
from django.db.models import Count

# Create your views here.
@login_required
def dashboard_view(request):
    user = request.user
    team = getattr(user, 'team', None)  
    members = team.members.all() if team else []  # prevent crash
    active_page = 'dashboard'

    context = {
        'user': user,
        'active_page': active_page,
        'stats': {
            'active_teams': Team.objects.filter(status='active').count(),
            'total_teams': Team.objects.count(),
            'departments': Department.objects.count(),
            'dependencies': 7     #dummy
        },
        'team': team,
        'members': members,
        'teams': Team.objects.all().annotate(member_count=Count('members')) 
    }
    return render(request, 'dashboard/dashboard.html',context)
from django.db import models

class TeamDependency(models.Model):
    DEPENDENCY_TYPES = [
        ('upstream', 'Upstream'),
        ('downstream', 'Downstream'),
    ]

    from_team = models.ForeignKey('teams.Team', on_delete=models.CASCADE, related_name='dependencies_from')
    to_team = models.ForeignKey('teams.Team', on_delete=models.CASCADE, related_name='dependencies_to')
    dependency_type = models.CharField(max_length=20, choices=DEPENDENCY_TYPES)
    description = models.TextField(blank=True, null=True)

    class Meta:
        unique_together = ('from_team', 'to_team', 'dependency_type')

    def __str__(self):
        return f"{self.from_team.teamName} -> {self.to_team.teamName} ({self.dependency_type})"

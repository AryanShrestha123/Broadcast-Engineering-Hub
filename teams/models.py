from django.db import models

# Create your models here.
class Team(models.Model):
    teamName = models.CharField(max_length=100)
    description = models.TextField()
    contactChannel = models.CharField(max_length=100)
    createdDate = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='active')

    # Foreign key references
    teamLeader = models.ForeignKey('account.CustomUser', on_delete=models.CASCADE, related_name='led_teams')
    department = models.ForeignKey('departments.Department', on_delete=models.CASCADE, related_name='teams')

    def __str__(self):
        return self.teamName

    @property
    def upstream_teams(self):
        return [dep.from_team for dep in self.dependencies_to.filter(dependency_type='upstream')]

    @property
    def downstream_teams(self):
        return [dep.to_team for dep in self.dependencies_from.filter(dependency_type='downstream')]

    @property
    def all_dependencies(self):
        upstream = self.dependencies_to.filter(dependency_type='upstream')
        downstream = self.dependencies_from.filter(dependency_type='downstream')
        return list(upstream) + list(downstream)
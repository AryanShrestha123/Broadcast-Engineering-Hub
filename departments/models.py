from django.db import models

# Create your models here.
class Department(models.Model):
    departmentName = models.CharField(max_length=100)
    description = models.TextField()
    specialization = models.CharField(max_length=100)
    createdDate = models.DateTimeField(auto_now_add=True)
    
    # Foreign key reference to CustomUser for department head
    departmentLeader = models.ForeignKey('account.CustomUser', on_delete=models.CASCADE, related_name='headed_departments')

    def __str__(self):
        return self.departmentName
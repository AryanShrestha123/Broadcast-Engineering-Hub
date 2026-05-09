from django import forms
from .models import TeamDependency

class TeamDependencyForm(forms.ModelForm):
    class Meta:
        model = TeamDependency
        fields = ['from_team', 'to_team', 'dependency_type', 'description']

    def clean(self):
        cleaned_data = super().clean()
        from_team = cleaned_data.get('from_team')
        to_team = cleaned_data.get('to_team')
        
        if from_team and to_team and from_team == to_team:
            raise forms.ValidationError("A team cannot depend on itself.")
        
        return cleaned_data
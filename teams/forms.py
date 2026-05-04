from django import forms
from django.core.exceptions import ValidationError
from .models import Team
from account.models import CustomUser


class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ['teamName', 'description', 'contactChannel', 'status', 'teamLeader', 'department']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # If editing an existing team, filter teamLeader to only show team members
        if self.instance and self.instance.pk:
            self.fields['teamLeader'].queryset = self.instance.members.all()


class TeamCreateForm(forms.ModelForm):
    members = forms.ModelMultipleChoiceField(
        queryset=CustomUser.objects.none(),
        widget=forms.SelectMultiple(attrs={'style': 'display:none;'}),
        required=True,
        label='Team Members',
        help_text='Select at least one member. Only users without a team can be added.'
    )

    class Meta:
        model = Team
        fields = ['teamName', 'description', 'contactChannel', 'status', 'department']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filter members to only show users without a team
        self.fields['members'].queryset = CustomUser.objects.filter(team__isnull=True)

    def clean_members(self):
        members = self.cleaned_data.get('members')
        if not members:
            raise ValidationError('You must select at least one team member.')
        if len(members) < 1:
            raise ValidationError('Team must have at least one member.')
        return members

    def save(self, commit=True):
        team = super().save(commit=False)
        members = self.cleaned_data.get('members')

        if members:
            # Set the first member as the team leader
            team.teamLeader = members[0]

        if commit:
            team.save()
            # Assign all members to the team
            for member in members:
                member.team = team
                member.save()

        return team

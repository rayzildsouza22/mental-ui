from django import forms
from .models import Activity, Mood

class ActivityForm(forms.ModelForm):
    class Meta:
        model = Activity
        fields = ['title', 'duration', 'time']
        widgets = {
            'time': forms.TimeInput(attrs={'type': 'time'})
        }


class MoodForm(forms.ModelForm):
    class Meta:
        model = Mood
        fields = ['mood']
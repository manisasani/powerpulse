from django import forms
from .models import UserDietInfo , DietGoal , ActivityLevel


class UserInfoForm(forms.ModelForm):
    class Meta:
        model = UserDietInfo
        fields = ['first_name' , 'gender' , 'age' , 'weight' , 'height' , 'goal' , 'activity_level']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'age': forms.NumberInput(attrs={'class': 'form-control'}),
            'weight': forms.NumberInput(attrs={'class': 'form-control'}),
            'height': forms.NumberInput(attrs={'class': 'form-control'}),

        }

class DiteGoalForm(forms.Form):
    goal = forms.modelChoiceField(
        queryset=DietGoal.objects.all(),
        widget=forms.RadioSelect
    )

class ActivityLevelForm(forms.Form):
    activity_level = forms.modelChoiceField(
        queryset=ActivityLevel.objects.all(),
        widget=forms.RadioSelect
    )
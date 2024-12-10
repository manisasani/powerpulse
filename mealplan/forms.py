from django import forms
from .models import UserDietInfo, DietGoal, ActivityLevel


class UserInfoForm(forms.ModelForm):
    class Meta:
        model = UserDietInfo
        fields = ["first_name", "gender", "age", "weight", "height"]
        widgets = {
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "gender": forms.Select(attrs={"class": "form-control"}),
            "age": forms.NumberInput(attrs={"class": "form-control"}),
            "weight": forms.NumberInput(attrs={"class": "form-control"}),
            "height": forms.NumberInput(attrs={"class": "form-control"}),
        }


class DietGoalForm(forms.Form):  # تغییر به Form ساده
    goal = forms.ModelChoiceField(
        queryset=DietGoal.objects.all(), widget=forms.RadioSelect, empty_label=None
    )


class ActivityLevelForm(forms.Form):  # تغییر به Form ساده
    activity_level = forms.ModelChoiceField(
        queryset=ActivityLevel.objects.all(), widget=forms.RadioSelect, empty_label=None
    )

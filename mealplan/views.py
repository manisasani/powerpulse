from django.shortcuts import render, redirect
from django.views.generic import FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import UserInfoForm, DietGoalForm, ActivityLevelForm
from . models import UserDietInfo, DietPlan


class UserInfoView(LoginRequiredMixin, FormView):
    template_name = 'diet/user_info.html'
    form_class = UserInfoForm
    success_url = '/diet/goal/'

    def from_valid(self, form):
        user_info = form.save(commit=False)
        user_info.user = self.request.user
        user_info.save()
        self.request.session['user_diet_info_id'] = user_info.id
        return super().form_valid(form)

class DietGoalView(LoginRequiredMixin, FormView):
    template_name = 'diet/diet_goal.html'
    form_class = DietGoalForm
    success_url = "/diet/activity/"

    def form_valid(self, form):
        user_info_id = self.request.session.get('user_diet_info_id')
        user_info = UserDietInfo.objects.get(id=user_info_id)
        user_info.goal = form.cleaned_data["goal"]
        user_info.save()
        return super().form_valid(form)

class ActivityLevelView(LoginRequiredMixin, FormView):
    template_name = 'diet/activity.html'
    form_class = ActivityLevelForm
    success_url = '/diet/plan/'

    def form_valid(self, form):
        user_info_id = self.request.session.get('user_diet_info_id')
        user_info = UserDietInfo.objects.get(id=user_info_id)
        user_info.activity_level = form.cleaned_data["activity_level"]
        user_info.save()
        return super().form_valid(form)


class DietPlanView(LoginRequiredMixin, FormView):
    template_name = 'diet/diet_plan.html'

    def get(self, request, *args, **kwargs):
        user_info_id = self.request.session.get('user_diet_info_id')
        user_info = UserDietInfo.objects.get(id=user_info_id)

        bmr = user_info.calculate_bmr()
        daily_calories = bmr * user_info.activity_level.level

        diet_plan = DietPlan.objects.filter(
            goal=user_info.goal, 
            activity_level=user_info.activity_level
            ).first()
        
        return render(request, self.template_name, {
            'diet_plan': diet_plan,
            'daily_calories': daily_calories
            })

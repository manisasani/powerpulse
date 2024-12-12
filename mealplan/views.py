from django.shortcuts import render, redirect
from django.views.generic import FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import UserInfoForm, DietGoalForm, ActivityLevelForm
from . models import UserDietInfo, DietPlan


class UserInfoView(LoginRequiredMixin, FormView):
    template_name = 'diet/user_info.html'
    form_class = UserInfoForm
    success_url = '/diet/goal/'

    def form_valid(self, form):
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
    template_name = "diet/diet_plan.html"

    def get(self, request, *args, **kwargs):
        user_info_id = self.request.session.get("user_diet_info_id")
        user_info = UserDietInfo.objects.get(id=user_info_id)

        # محاسبه کالری روزانه
        bmr = user_info.calculate_bmr()
        daily_calories = bmr * float(user_info.activity_level.multiplier)

        # لاگ اطلاعات پایه
        print(f"User Info:")
        print(f"- Weight: {user_info.weight}kg")
        print(f"- Height: {user_info.height}cm")
        print(f"- Age: {user_info.age}")
        print(f"- Gender: {user_info.gender}")
        print(f"- Activity Level: {user_info.activity_level}")
        print(f"- BMR: {bmr:.2f}")
        print(f"- Daily Calories: {daily_calories:.2f}")

        diet_plan = DietPlan.objects.filter(
            goal=user_info.goal,
            calorie_range_min__lte=daily_calories,
            calorie_range_max__gte=daily_calories,
        ).first()

        if not diet_plan:
            context = {
                "user_info": user_info,
                "daily_calories": int(daily_calories),
                "diet_plan": None,
                "error": "هیچ برنامه غذایی مناسب پیدا نشد.",
            }
            return render(request, self.template_name, context)

        # محاسبه ماکروها
        protein_grams = (daily_calories * diet_plan.protein_percentage / 100) / 4
        carbs_grams = (daily_calories * diet_plan.carbs_percentage / 100) / 4
        fats_grams = (daily_calories * diet_plan.fat_percentage / 100) / 9

        # لاگ اطلاعات ماکروها
        print(f"\nMacronutrient Calculations:")
        print(f"Diet Plan: {diet_plan}")
        print(
            f"- Protein: {diet_plan.protein_percentage}% = {protein_grams:.1f}g ({protein_grams * 4:.0f} kcal)"
        )
        print(
            f"- Carbs: {diet_plan.carbs_percentage}% = {carbs_grams:.1f}g ({carbs_grams * 4:.0f} kcal)"
        )
        print(
            f"- Fats: {diet_plan.fat_percentage}% = {fats_grams:.1f}g ({fats_grams * 9:.0f} kcal)"
        )

        # بررسی نسبت پروتئین به وزن بدن
        protein_per_kg = protein_grams / user_info.weight
        print(f"\nProtein per kg of body weight: {protein_per_kg:.2f}g/kg")
        if protein_per_kg < 1.6 or protein_per_kg > 2.2:
            print("Warning: Protein intake is outside recommended range (1.6-2.2g/kg)")

        # بررسی مجموع کالری‌ها
        total_calories = (protein_grams * 4) + (carbs_grams * 4) + (fats_grams * 9)
        print(f"\nTotal calories from macros: {total_calories:.0f}")
        print(f"Difference from target: {daily_calories - total_calories:.0f} kcal")

        context = {
            "user_info": user_info,
            "daily_calories": int(daily_calories),
            "diet_plan": diet_plan,
            "macros": {
                "protein": int(protein_grams),
                "carbs": int(carbs_grams),
                "fats": int(fats_grams),
            },
        }
        return render(request, self.template_name, context)

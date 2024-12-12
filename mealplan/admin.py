# admin.py
from django.contrib import admin
from .models import UserDietInfo, DietGoal, ActivityLevel, DietPlan


@admin.register(DietGoal)
class DietGoalAdmin(admin.ModelAdmin):
    list_display = ["goal"]
    search_fields = ["goal"]


@admin.register(ActivityLevel)
class ActivityLevelAdmin(admin.ModelAdmin):
    list_display = ["level", "multiplier"]
    search_fields = ["level"]


@admin.register(UserDietInfo)
class UserDietInfoAdmin(admin.ModelAdmin):
    list_display = [
        "user",
        "first_name",
        "age",
        "weight",
        "height",
        "goal",
        "activity_level",
    ]
    list_filter = ["goal", "activity_level"]
    search_fields = ["user__username", "first_name"]


@admin.register(DietPlan)
class DietPlanAdmin(admin.ModelAdmin):
    list_display = [
        "goal",
        "calorie_range_min",
        "calorie_range_max",
        "protein_percentage",
        "carbs_percentage",
        "fat_percentage",
    ]

    fieldsets = (
        (
            "Basic Information",
            {"fields": ("goal", "calorie_range_min", "calorie_range_max")},
        ),
        (
            "Macronutrients",
            {
                "fields": ("protein_percentage", "carbs_percentage", "fat_percentage"),
                "description": "مجموع درصدها باید 100 باشد و درصد چربی نباید کمتر از 20 درصد باشد",
            },
        ),
        (
            "Meal Plan",
            {
                "fields": (
                    "breakfast",
                    "snacks",
                    "lunch",
                    "snacks2",
                    "dinner",
                    "snacks3",
                )
            },
        ),
        ("Additional Information", {"fields": ("notes",)}),
    )

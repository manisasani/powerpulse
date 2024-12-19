from django.urls import path
from . views import UserInfoView , DietGoalView , ActivityLevelView , DietPlanView

app_name = "mealplan"

urlpatterns = [
    path("info/", UserInfoView.as_view(), name="user_info"),
    path("goal/", DietGoalView.as_view(), name="diet_goal"),
    path('activity/', ActivityLevelView.as_view(), name="activity_level"),
    path('plan/', DietPlanView.as_view(), name='diet_plan'),
]

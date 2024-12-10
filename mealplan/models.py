from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings
class DietGoal(models.Model):
    goal = models.CharField(
        max_length=20,
        choices=[
            ("lose_weight", "کاهش وزن"),
            ("gain_weight", "افزایش وزن"),
            ("maintain_weight", "حفظ وزن"),
            ("muscle_building", "عضله‌سازی"),
        ],
        unique=True,
    )

    def __str__(self):
        return self.get_goal_display()


class ActivityLevel(models.Model):
    level = models.CharField(
        max_length=20,
        choices=[
            ("low", "کم"),
            ("medium", "متوسط"),
            ("high", "زیاد"),
            ("athlete", "ورزشکار"),
        ],
        unique=True,
    )

    def __str__(self):
        return self.get_level_display()

class UserDietInfo(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL , on_delete=models.CASCADE)
    first_name = models.CharField(max_length=20)
    gender = models.CharField(max_length=10, choices=[('M', 'مرد'), ('F', 'زن'),])  
    age = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(120)])
    weight = models.FloatField(validators=[MinValueValidator(1)])  # in kg
    height = models.FloatField(validators=[MinValueValidator(30)])  # in cm
    goal = models.ForeignKey(DietGoal, on_delete=models.SET_NULL, null=True)
    activity_level = models.ForeignKey(ActivityLevel, on_delete=models.SET_NULL , null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def calculate_bmr(self):

        if self.gender == "M":
            return (
                88.362
                + (13.397 * self.weight)
                + (4.799 * self.height)
                - (5.677 * self.age)
            )
        else:
            return (
                447.593
                + (9.247 * self.weight)
                + (3.098 * self.height)
                - (4.330 * self.age)
            )

class DietPlan(models.Model):
    class Meta:
            ordering = ['goal', 'activity_level'] 
            verbose_name = 'Diet Plan'  
            verbose_name_plural = 'Diet Plans'  

    user_info = models.ForeignKey(UserDietInfo, on_delete=models.CASCADE)
    goal = models.ForeignKey(DietGoal, on_delete=models.SET_NULL, null=True)
    activity_level = models.ForeignKey(ActivityLevel, on_delete=models.SET_NULL , null=True)
    calories = models.IntegerField()
    protein = models.IntegerField() #in grams
    carbs = models.IntegerField() #in grams
    fats = models.IntegerField() #in grams
    meal_plan = models.TextField() 

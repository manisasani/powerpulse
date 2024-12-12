from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models

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
    ACTIVITY_CHOICES = [
        ("low", "کم"),
        ("medium", "متوسط"),
        ("high", "زیاد"),
        ("athlete", "ورزشکار"),
    ]

    level = models.CharField(
        max_length=20,
        choices=ACTIVITY_CHOICES,
        unique=True,
    )
    multiplier = models.FloatField()

    def __str__(self):
        return dict(self.ACTIVITY_CHOICES)[self.level]

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
            bmr = (10 * self.weight) + (6.25 * self.height) - (5 * self.age) + 5
        else:
            bmr = (10 * self.weight) + (6.25 * self.height) - (5 * self.age) - 161
        return bmr
    def __str__(self):
        return f"{self.first_name}"


class DietPlan(models.Model):
    goal = models.ForeignKey(DietGoal, on_delete=models.CASCADE)
    calorie_range_min = models.IntegerField(default=0)
    calorie_range_max = models.IntegerField(default=0)
    breakfast = models.TextField(default="")
    lunch = models.TextField(default="")
    dinner = models.TextField(default="")
    snacks = models.TextField(default="")
    snacks2 = models.TextField(default="")
    snacks3 = models.TextField(blank=True, default="")
    protein_percentage = models.IntegerField(default=0)
    carbs_percentage = models.IntegerField(default=0)
    fat_percentage = models.IntegerField(default=0)
    notes = models.TextField(blank=True, default="")

    def validate_macros(self):
        """اعتبارسنجی مقادیر ماکروها"""
        total = self.protein_percentage + self.carbs_percentage + self.fat_percentage
        if total != 100:
            return False, f"مجموع درصدهای ماکروها باید 100 باشد. مقدار فعلی: {total}"

        if self.fat_percentage < 20:
            return False, "درصد چربی نباید کمتر از 20 درصد باشد"

        return True, "OK"

    def save(self, *args, **kwargs):
        is_valid, message = self.validate_macros()
        if not is_valid:
            raise ValidationError(message)
        super().save(*args, **kwargs)

    class Meta:
        ordering = ["goal", "calorie_range_min"]
        verbose_name = "Diet Plan"
        verbose_name_plural = "Diet Plans"

    def __str__(self):
        return f"Diet Plan for {self.goal} ({self.calorie_range_min}-{self.calorie_range_max} cal)"

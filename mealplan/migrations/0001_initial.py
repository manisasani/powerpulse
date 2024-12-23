# Generated by Django 4.2.16 on 2024-12-10 09:58

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ActivityLevel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('level', models.CharField(choices=[('low', 'کم'), ('medium', 'متوسط'), ('high', 'زیاد'), ('athlete', 'ورزشکار')], max_length=20, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='DietGoal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('goal', models.CharField(choices=[('lose_weight', 'کاهش وزن'), ('gain_weight', 'افزایش وزن'), ('maintain_weight', 'حفظ وزن'), ('muscle_building', 'عضله\u200cسازی')], max_length=20, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserDietInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=20)),
                ('gender', models.CharField(choices=[('M', 'مرد'), ('F', 'زن')], max_length=10)),
                ('age', models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(120)])),
                ('weight', models.FloatField(validators=[django.core.validators.MinValueValidator(1)])),
                ('height', models.FloatField(validators=[django.core.validators.MinValueValidator(30)])),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('activity_level', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='mealplan.activitylevel')),
                ('goal', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='mealplan.dietgoal')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='DietPlan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('calories', models.IntegerField()),
                ('protein', models.IntegerField()),
                ('carbs', models.IntegerField()),
                ('fats', models.IntegerField()),
                ('meal_plan', models.TextField()),
                ('activity_level', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='mealplan.activitylevel')),
                ('goal', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='mealplan.dietgoal')),
                ('user_info', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mealplan.userdietinfo')),
            ],
            options={
                'verbose_name': 'Diet Plan',
                'verbose_name_plural': 'Diet Plans',
                'ordering': ['goal', 'activity_level'],
            },
        ),
    ]

from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.home_page_view, name='home'),
    path('about/', views.about_page_view, name='about')
    
]

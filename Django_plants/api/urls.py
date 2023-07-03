# -*- coding: utf-8 -*-
from django.urls import path, re_path

from . import views

urlpatterns = [
    path('plants/', views.plants_view),
    re_path('plant/<str:plant_id>', views.plant_view),
]

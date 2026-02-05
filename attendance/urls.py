from django.urls import path
from . import views

urlpatterns = [
    path('employee/<int:id>/', views.view_attendance, name='view_attendance'),
    path('weekly/', views.weekly_attendance, name='weekly_attendance'),
    path('mark-bulk/', views.mark_bulk_attendance, name='mark_bulk_attendance'),
]

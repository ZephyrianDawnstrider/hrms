from django.urls import path
from . import views

urlpatterns = [
    path('', views.employee_list, name='employee_list'),
    path('add/', views.employee_add, name='employee_add'),
    path('edit/<int:id>/', views.employee_edit, name='employee_edit'),
    path('delete/<int:id>/', views.employee_delete, name='employee_delete'),
    path('check-id/', views.check_employee_id, name='check_employee_id'),
    path('available-ids/', views.get_available_ids, name='available_ids'),
]

from django.urls import path
from .views import (
    dashboard_view,
    admin_dashboard,
    edit_lead,
    delete_lead,
    admin_login,
    admin_logout,
)

urlpatterns = [
    path('', dashboard_view, name='dashboard'),
    path('admin-dashboard/', admin_dashboard, name='admin_dashboard'),
    path('edit/<int:pk>/', edit_lead, name='edit_lead'),
    path('delete/<int:pk>/', delete_lead, name='delete_lead'),

    # 🔐 Login and Logout for Admin
    path('admin-login/', admin_login, name='admin_login'),
    path('admin-logout/', admin_logout, name='admin_logout'),
]

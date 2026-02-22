from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

app_name = 'leads'

urlpatterns = [
    path('', views.lead_list, name='lead_list'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('add/', views.lead_create, name='lead_create'),
    path('<int:pk>/', views.lead_detail, name='lead_detail'),
    path('<int:pk>/edit/', views.lead_edit, name='lead_edit'),
    path('<int:pk>/delete/', views.lead_delete, name='lead_delete'),
    path('upload/', views.lead_upload, name='lead_upload'),
    path('download/', views.lead_download, name='lead_download'),
    path('download/template/', views.lead_download_template, name='lead_download_template'),
]

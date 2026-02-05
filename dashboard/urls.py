from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.dashboard_home, name='home'),
    path('admin/', views.admin_dashboard, name='admin'),
    path('user/', views.user_dashboard, name='user'),
    path('application/<int:app_id>/<str:status>/',views.update_application_status,name='update_status'),
    path("admin/candidates/", views.admin_candidates, name="admin_candidates"),
    path("admin/candidate/<int:user_id>/", views.admin_candidate_detail, name="admin_candidate_detail"),
    path("admin/analytics/", views.admin_analytics, name="admin_analytics"),

]

from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login_view'),
    path('register/', views.register_view, name='register_view'),
    path('logout/', views.logout_view, name='logout_view'),
    path('', views.problem_list, name='problem_list'),
    path('helper/', views.problem_list, name='problem_list'),
    path('helper/create/', views.create_problem, name='create_problem'),
    path('helper/<int:problem_id>/', views.view_problem, name='view_problem'),
]

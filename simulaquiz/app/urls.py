from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login, name='login'),
    path('sign-up/', views.sign_up, name='sign-up'),
    path('logout/', views.logout_user, name='logout'),
    path('exams/', views.exams, name='exams'),
    path('exam/<int:id>/', views.exam, name='exam'),
    path('feedback/<int:id>/', views.feedback, name='feedback'),
    path('my-exams/', views.my_exams, name='my-exams'),
    path('my-exam/<int:id>', views.my_exam, name='my-exam'),
    path('create-exam/', views.create_exam, name='create-exam'),
    path('create-question/<int:id>/', views.create_question, name='create-question'),
    path('create-choice/<int:id>/', views.create_choice, name='create-choice'),
    path('edit-exam/<int:id>/', views.edit_exam, name='edit-exam'),
    path('edit-question/<int:id>', views.edit_question, name='edit-question'),
    path('edit-choice/<int:id>', views.edit_choice, name='edit-choice'),
    path('delete-exam/<int:id>/', views.delete_exam, name='delete-exam'),
    path('delete-question/<int:id>/', views.delete_question, name='delete-question'),
    path('delete-choice/<int:id>/', views.delete_choice, name='delete-choice'),
    
]
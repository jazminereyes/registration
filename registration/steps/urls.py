from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

urlpatterns = [
    path('', auth_views.LoginView.as_view(redirect_authenticated_user=True), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('home/', views.HomeView.as_view(), name='home'),
    path('step/', views.StepView.as_view(), name='step'),
    path('step/<int:step>/', views.StepView.as_view(), name='step'),
    path('step/ajax/', views.StepAjaxView.as_view(), name='step_ajax'),
]
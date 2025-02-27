from django.urls import path
from django.contrib.auth import views as auth_views
from . import views  # Import views from the core app



urlpatterns = [
    path('', auth_views.LoginView.as_view(template_name="core/login.html",redirect_authenticated_user=True), name='login'),  # Route for the home page
    path("register/", views.register, name="register"),   # Route for the register page
    path("home/", views.home, name="home"),
    path("logout/", auth_views.LogoutView.as_view(next_page="login"), name="logout"),
    path('post_list', views.post_list, name='post_list'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/new/', views.create_post, name='create_post'),
    path('post/<int:pk>/edit/', views.update_post, name='update_post'),
    path('post/<int:pk>/delete/', views.delete_post, name='delete_post'),
]
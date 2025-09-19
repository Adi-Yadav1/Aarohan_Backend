from django.urls import path
from .views import (
    # Authentication
    register_athlete, login_view, get_profile,
    forgot_password, reset_password,
    # Test Management  
    get_all_tests, submit_performance, get_leaderboard
)

urlpatterns = [
    # Authentication URLs - SAI Fitness API
    path("auth/register/", register_athlete, name="register_athlete"),
    path("auth/login/", login_view, name="login"), 
    path("auth/profile/", get_profile, name="get_profile"), 
    path("auth/forgot-password/", forgot_password, name="forgot_password"),
    path("auth/reset-password/", reset_password, name="reset_password"),
    
    # Test Management URLs
    path("tests/", get_all_tests, name="get_all_tests"),
    path("tests/submit/", submit_performance, name="submit_performance"),
    path("leaderboard/<str:test_id>/", get_leaderboard, name="get_leaderboard"),
]

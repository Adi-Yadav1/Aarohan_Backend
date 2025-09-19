from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import get_object_or_404
from django.db.models import Count, Q, Max, Avg, F, Case, When
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.hashers import make_password
from datetime import timedelta, datetime
import secrets
import string
import csv
import io
from .serializers import (
    RegisterSerializer, LoginSerializer, UserSerializer, AthleteSerializer,
    ForgotPasswordSerializer, ResetPasswordSerializer, TestSerializer,
    TestCreateSerializer, PerformanceSerializer, PerformanceCreateSerializer,
    PerformanceUpdateSerializer, LeaderboardSerializer, BadgeSerializer,
    AthleteBadgeSerializer, AthleteStatsSerializer, DashboardStatsSerializer,
    AthleteListSerializer, NotificationSerializer
)
from .models import (
    User, Athlete, Test, Performance, Badge, AthleteBadge,
    AthleteStats, Notification, SystemSettings
)

# Utility Functions

def generate_token():
    return ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(32))

def is_admin_user(user):
    return user.role == 'ADMIN'

def send_email_notification(to_email, subject, message):
    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[to_email],
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f"Email sending failed: {str(e)}")
        return False

# Health Check

@api_view(["GET"])
@permission_classes([AllowAny])
def health_check(request):
    """Health check endpoint"""
    return Response({
        "status": "OK",
        "message": "SAI Fitness Backend is running",
        "timestamp": timezone.now().isoformat()
    }, status=200)

# Authentication Views

@api_view(["POST"])
@permission_classes([AllowAny])
def register_athlete(request):
    """Register new athlete account"""
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        
        # Send verification email
        verification_url = f"http://localhost:3000/verify-email?token={user.email_verification_token}"
        send_email_notification(
            to_email=user.email,
            subject="Welcome to SAI Fitness - Verify Your Email",
            message=f"Welcome to SAI Fitness! Please verify your email by clicking: {verification_url}"
        )
        
        # Generate JWT token
        refresh = RefreshToken.for_user(user)
        
        return Response({
            "success": True,
            "message": "Registration successful. Please verify your email.",
            "data": {
                "user": UserSerializer(user).data,
                "token": str(refresh.access_token)
            }
        }, status=201)
    
    return Response({
        "success": False,
        "message": "Registration failed",
        "errors": serializer.errors
    }, status=400)

@api_view(["POST"])
@permission_classes([AllowAny])
def login_view(request):
    """Authenticate user and get token"""
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data["user"]
        refresh = RefreshToken.for_user(user)
        
        # Get profile data
        profile_data = {}
        if hasattr(user, 'athlete'):
            profile_data = {
                "firstName": user.athlete.first_name,
                "lastName": user.athlete.last_name,
                "sport": user.athlete.sport
            }
        
        return Response({
            "success": True,
            "message": "Login successful",
            "data": {
                "user": {
                    **UserSerializer(user).data,
                    "profile": profile_data
                },
                "token": str(refresh.access_token)
            }
        }, status=200)
    
    return Response({
        "success": False,
        "message": "Invalid credentials",
        "errors": serializer.errors
    }, status=400)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_profile(request):
    """Get current user profile"""
    user = request.user
    serializer = UserSerializer(user)
    
    return Response({
        "success": True,
        "data": {
            "user": serializer.data
        }
    }, status=200)

# Test Management Views

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_all_tests(request):
    """Retrieve all available fitness tests"""
    tests = Test.objects.filter(is_active=True)
    serializer = TestSerializer(tests, many=True)
    
    return Response({
        "success": True,
        "message": "Tests retrieved successfully",
        "data": {
            "tests": serializer.data
        }
    }, status=200)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_test_by_id(request, test_id):
    """Get specific test details"""
    try:
        test = Test.objects.get(id=test_id, is_active=True)
        serializer = TestSerializer(test)
        
        return Response({
            "success": True,
            "data": {
                "test": serializer.data
            }
        }, status=200)
    except Test.DoesNotExist:
        return Response({
            "success": False,
            "message": "Test not found"
        }, status=404)

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_test(request):
    """Create new fitness test (Admin only)"""
    if not is_admin_user(request.user):
        return Response({
            "success": False,
            "message": "Admin access required"
        }, status=403)
    
    serializer = TestCreateSerializer(data=request.data)
    if serializer.is_valid():
        test = serializer.save()
        return Response({
            "success": True,
            "message": "Test created successfully",
            "data": {
                "test": TestSerializer(test).data
            }
        }, status=201)
    
    return Response({
        "success": False,
        "errors": serializer.errors
    }, status=400)

# Performance Management Views

@api_view(["POST"])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser, JSONParser])
def submit_performance(request):
    """Submit performance with media files"""
    if not hasattr(request.user, 'athlete'):
        return Response({
            "success": False,
            "message": "Athlete profile required"
        }, status=400)
    
    serializer = PerformanceCreateSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        performance = serializer.save()
        
        return Response({
            "success": True,
            "message": "Performance submitted successfully",
            "data": {
                "performance": PerformanceSerializer(performance).data
            }
        }, status=201)
    
    return Response({
        "success": False,
        "errors": serializer.errors
    }, status=400)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_my_performances(request):
    """Get athlete's own performances"""
    if not hasattr(request.user, 'athlete'):
        return Response({
            "success": False,
            "message": "Athlete profile required"
        }, status=400)
    
    # Filter parameters
    test_id = request.GET.get('testId')
    status_filter = request.GET.get('status')
    page = int(request.GET.get('page', 1))
    limit = int(request.GET.get('limit', 10))
    
    performances = Performance.objects.filter(athlete=request.user.athlete)
    
    if test_id:
        performances = performances.filter(test_id=test_id)
    if status_filter:
        performances = performances.filter(status=status_filter)
    
    # Pagination
    start_idx = (page - 1) * limit
    end_idx = start_idx + limit
    
    performances = performances.order_by('-created_at')[start_idx:end_idx]
    serializer = PerformanceSerializer(performances, many=True)
    
    return Response({
        "success": True,
        "data": {
            "performances": serializer.data,
            "pagination": {
                "page": page,
                "limit": limit,
                "total": Performance.objects.filter(athlete=request.user.athlete).count()
            }
        }
    }, status=200)

# Simple leaderboard view
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_leaderboard(request, test_id):
    """Get performance rankings"""
    try:
        test = Test.objects.get(id=test_id)
        
        # Get verified performances
        performances = Performance.objects.filter(
            test=test, status='VERIFIED'
        ).select_related('athlete').order_by('value')[:20]
        
        leaderboard_data = []
        for rank, perf in enumerate(performances, 1):
            leaderboard_data.append({
                "rank": rank,
                "athlete": {
                    "firstName": perf.athlete.first_name,
                    "lastName": perf.athlete.last_name,
                    "state": perf.athlete.state,
                    "district": perf.athlete.district
                },
                "value": perf.value,
                "createdAt": perf.created_at
            })
        
        return Response({
            "success": True,
            "data": {
                "leaderboard": leaderboard_data,
                "total": len(leaderboard_data),
                "testInfo": {
                    "name": test.name,
                    "unit": test.unit
                }
            }
        }, status=200)
        
    except Test.DoesNotExist:
        return Response({
            "success": False,
            "message": "Test not found"
        }, status=404)

# Password Reset Views

@api_view(["POST"])
@permission_classes([AllowAny])
def forgot_password(request):
    """Request password reset"""
    serializer = ForgotPasswordSerializer(data=request.data)
    if serializer.is_valid():
        email = serializer.validated_data['email']
        user = User.objects.get(email=email)
        
        # Generate reset token
        reset_token = generate_token()
        user.password_reset_token = reset_token
        user.password_reset_expires = timezone.now() + timedelta(hours=1)
        user.save()
        
        # Send reset email
        reset_url = f"http://localhost:3000/reset-password?token={reset_token}"
        send_email_notification(
            to_email=email,
            subject="SAI Fitness - Password Reset",
            message=f"Click here to reset your password: {reset_url} (Valid for 1 hour)"
        )
        
        return Response({
            "success": True,
            "message": "Password reset email sent successfully"
        }, status=200)
    
    return Response({
        "success": False,
        "errors": serializer.errors
    }, status=400)

@api_view(["POST"])
@permission_classes([AllowAny])
def reset_password(request):
    """Reset password with token"""
    serializer = ResetPasswordSerializer(data=request.data)
    if serializer.is_valid():
        token = serializer.validated_data['token']
        new_password = serializer.validated_data['new_password']
        
        user = User.objects.get(password_reset_token=token)
        user.set_password(new_password)
        user.password_reset_token = None
        user.password_reset_expires = None
        user.save()
        
        return Response({
            "success": True,
            "message": "Password reset successful"
        }, status=200)
    
    return Response({
        "success": False,
        "errors": serializer.errors
    }, status=400)

@api_view(["POST"])
@permission_classes([AllowAny])
def reset_password(request):
    """Reset password with token"""
    serializer = ResetPasswordSerializer(data=request.data)
    if serializer.is_valid():
        token = serializer.validated_data['token']
        new_password = serializer.validated_data['new_password']
        
        user = User.objects.get(password_reset_token=token)
        user.set_password(new_password)
        user.password_reset_token = None
        user.password_reset_expires = None
        user.save()
        
        return Response({
            "success": True,
            "message": "Password reset successful"
        }, status=200)
    
    return Response({
        "success": False,
        "errors": serializer.errors
    }, status=400)

from rest_framework import serializers
from django.contrib.auth import authenticate
from django.utils import timezone
from django.core.validators import validate_email
from django.contrib.auth.password_validation import validate_password
import secrets
import string
from .models import (
    User, Athlete, Test, Performance, Badge, AthleteBadge, 
    AthleteStats, Notification, SystemSettings
)

# Authentication Serializers

class AthleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Athlete
        fields = [
            'id', 'first_name', 'last_name', 'date_of_birth', 'gender', 
            'phone', 'state', 'district', 'address', 'sport', 'category'
        ]

class UserSerializer(serializers.ModelSerializer):
    athlete = AthleteSerializer(read_only=True)
    
    class Meta:
        model = User
        fields = ['id', 'email', 'role', 'is_email_verified', 'athlete']

class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(min_length=8, validators=[validate_password])
    first_name = serializers.CharField(max_length=50)
    last_name = serializers.CharField(max_length=50)
    date_of_birth = serializers.DateField()
    gender = serializers.ChoiceField(choices=Athlete.GENDER_CHOICES)
    phone = serializers.CharField(max_length=15)
    state = serializers.CharField(max_length=50)
    district = serializers.CharField(max_length=50)
    address = serializers.CharField()
    sport = serializers.ChoiceField(choices=Athlete.SPORT_CHOICES)
    category = serializers.ChoiceField(choices=Athlete.CATEGORY_CHOICES)
    
    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already registered")
        return value
    
    def create(self, validated_data):
        # Extract athlete data
        athlete_data = {
            'first_name': validated_data.pop('first_name'),
            'last_name': validated_data.pop('last_name'),
            'date_of_birth': validated_data.pop('date_of_birth'),
            'gender': validated_data.pop('gender'),
            'phone': validated_data.pop('phone'),
            'state': validated_data.pop('state'),
            'district': validated_data.pop('district'),
            'address': validated_data.pop('address'),
            'sport': validated_data.pop('sport'),
            'category': validated_data.pop('category'),
        }
        
        # Create user
        user = User.objects.create_user(
            username=validated_data['email'],
            email=validated_data['email'],
            password=validated_data['password'],
            role='ATHLETE'
        )
        
        # Generate email verification token
        user.email_verification_token = self.generate_token()
        user.save()
        
        # Create athlete profile
        athlete = Athlete.objects.create(user=user, **athlete_data)
        
        # Create athlete stats
        AthleteStats.objects.create(athlete=athlete)
        
        return user
    
    def generate_token(self):
        return ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(32))

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        email = data.get("email")
        password = data.get("password")

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError("Invalid email or password")

        user = authenticate(username=user.username, password=password)
        if not user:
            raise serializers.ValidationError("Invalid email or password")

        data["user"] = user
        return data

class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
    
    def validate_email(self, value):
        try:
            user = User.objects.get(email=value)
            return value
        except User.DoesNotExist:
            raise serializers.ValidationError("No user found with this email address")

class ResetPasswordSerializer(serializers.Serializer):
    token = serializers.CharField()
    new_password = serializers.CharField(min_length=8, validators=[validate_password])
    
    def validate_token(self, value):
        try:
            user = User.objects.get(password_reset_token=value)
            if user.password_reset_expires and user.password_reset_expires < timezone.now():
                raise serializers.ValidationError("Reset token has expired")
            return value
        except User.DoesNotExist:
            raise serializers.ValidationError("Invalid or expired reset token")

# Test Serializers

class TestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Test
        fields = ['id', 'name', 'description', 'unit', 'category', 'is_active', 'created_at']

class TestCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Test
        fields = ['name', 'description', 'unit', 'category']

# Performance Serializers

class PerformanceSerializer(serializers.ModelSerializer):
    test_name = serializers.CharField(source='test.name', read_only=True)
    test_unit = serializers.CharField(source='test.unit', read_only=True)
    athlete_name = serializers.CharField(source='athlete.full_name', read_only=True)
    
    class Meta:
        model = Performance
        fields = [
            'id', 'test', 'test_name', 'test_unit', 'athlete', 'athlete_name',
            'value', 'status', 'video', 'image', 'verified_by', 'verified_at',
            'verification_notes', 'created_at'
        ]
        read_only_fields = ['id', 'athlete', 'verified_by', 'verified_at', 'created_at']

class PerformanceCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Performance
        fields = ['test', 'value', 'video', 'image']
    
    def create(self, validated_data):
        validated_data['athlete'] = self.context['request'].user.athlete
        return super().create(validated_data)

class PerformanceUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Performance
        fields = ['status', 'verification_notes', 'flag_reason', 'flag_notes']

# Leaderboard Serializers

class LeaderboardEntrySerializer(serializers.Serializer):
    rank = serializers.IntegerField()
    athlete = AthleteSerializer()
    value = serializers.FloatField()
    created_at = serializers.DateTimeField()

class LeaderboardSerializer(serializers.Serializer):
    leaderboard = LeaderboardEntrySerializer(many=True)
    total = serializers.IntegerField()
    test_info = TestSerializer()

# Badge Serializers

class BadgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Badge
        fields = ['id', 'name', 'description', 'badge_type', 'icon', 'points']

class AthleteBadgeSerializer(serializers.ModelSerializer):
    badge = BadgeSerializer(read_only=True)
    
    class Meta:
        model = AthleteBadge
        fields = ['badge', 'earned_at']

# Stats Serializers

class AthleteStatsSerializer(serializers.ModelSerializer):
    personal_bests = serializers.SerializerMethodField()
    recent_performances = serializers.SerializerMethodField()
    
    class Meta:
        model = AthleteStats
        fields = [
            'total_performances', 'verified_performances', 'pending_performances',
            'flagged_performances', 'total_badges', 'total_points', 'current_rank',
            'personal_bests', 'recent_performances'
        ]
    
    def get_personal_bests(self, obj):
        # Get best performance for each test
        performances = Performance.objects.filter(
            athlete=obj.athlete, 
            status='VERIFIED'
        ).select_related('test').order_by('test', 'value')
        
        bests = {}
        for perf in performances:
            if perf.test.name not in bests:
                bests[perf.test.name] = {
                    'test_name': perf.test.name,
                    'best_value': perf.value,
                    'unit': perf.test.unit,
                    'achieved_at': perf.created_at
                }
        
        return list(bests.values())
    
    def get_recent_performances(self, obj):
        recent = Performance.objects.filter(
            athlete=obj.athlete
        ).select_related('test').order_by('-created_at')[:5]
        
        return [{
            'test_name': perf.test.name,
            'value': perf.value,
            'status': perf.status,
            'created_at': perf.created_at
        } for perf in recent]

# Admin Serializers

class DashboardStatsSerializer(serializers.Serializer):
    total_athletes = serializers.IntegerField()
    total_performances = serializers.IntegerField()
    pending_verifications = serializers.IntegerField()
    flagged_performances = serializers.IntegerField()
    recent_registrations = serializers.IntegerField()
    top_performing_states = serializers.ListField()

class AthleteListSerializer(serializers.ModelSerializer):
    user_email = serializers.CharField(source='user.email', read_only=True)
    performance_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Athlete
        fields = [
            'id', 'first_name', 'last_name', 'user_email', 'sport', 
            'category', 'state', 'district', 'created_at', 'performance_count'
        ]
    
    def get_performance_count(self, obj):
        return obj.performances.filter(status='VERIFIED').count()

# Notification Serializers

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'notification_type', 'title', 'message', 'is_read', 'created_at']

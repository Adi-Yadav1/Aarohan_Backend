from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from cloudinary.models import CloudinaryField
import uuid

# UUID Generation Functions
def generate_user_id():
    return f"cm4user{uuid.uuid4().hex[:6]}"

def generate_athlete_id():
    return f"cm4{uuid.uuid4().hex[:9]}"

def generate_test_id():
    return f"cm4test{uuid.uuid4().hex[:6]}"

def generate_performance_id():
    return f"cm4perf{uuid.uuid4().hex[:6]}"

def generate_badge_id():
    return f"cm4badge{uuid.uuid4().hex[:5]}"

def generate_notification_id():
    return f"cm4notif{uuid.uuid4().hex[:5]}"

class User(AbstractUser):
    ROLE_CHOICES = [
        ('ADMIN', 'Admin'),
        ('ATHLETE', 'Athlete'),
    ]
    
    id = models.CharField(max_length=20, primary_key=True, default=generate_user_id)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='ATHLETE')
    is_email_verified = models.BooleanField(default=False)
    email_verification_token = models.CharField(max_length=100, blank=True, null=True)
    password_reset_token = models.CharField(max_length=100, blank=True, null=True)
    password_reset_expires = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.username} ({self.role})"

class Athlete(models.Model):
    GENDER_CHOICES = [
        ('MALE', 'Male'),
        ('FEMALE', 'Female'),
    ]
    
    SPORT_CHOICES = [
        ('ATHLETICS', 'Athletics'),
        ('SWIMMING', 'Swimming'),
        ('CYCLING', 'Cycling'),
        ('WEIGHTLIFTING', 'Weightlifting'),
        ('BOXING', 'Boxing'),
        ('WRESTLING', 'Wrestling'),
        ('BADMINTON', 'Badminton'),
        ('TENNIS', 'Tennis'),
        ('FOOTBALL', 'Football'),
        ('BASKETBALL', 'Basketball'),
    ]
    
    CATEGORY_CHOICES = [
        ('SPRINTS', 'Sprints'),
        ('MIDDLE_DISTANCE', 'Middle Distance'),
        ('LONG_DISTANCE', 'Long Distance'),
        ('JUMPS', 'Jumps'),
        ('THROWS', 'Throws'),
        ('COMBINED_EVENTS', 'Combined Events'),
        ('FREESTYLE', 'Freestyle'),
        ('BACKSTROKE', 'Backstroke'),
        ('BREASTSTROKE', 'Breaststroke'),
        ('BUTTERFLY', 'Butterfly'),
        ('INDIVIDUAL_MEDLEY', 'Individual Medley'),
    ]
    
    id = models.CharField(max_length=20, primary_key=True, default=generate_athlete_id)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='athlete')
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    phone = models.CharField(max_length=15)
    state = models.CharField(max_length=50)
    district = models.CharField(max_length=50)
    address = models.TextField()
    sport = models.CharField(max_length=20, choices=SPORT_CHOICES)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    profile_image = CloudinaryField('image', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.sport}"
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

class Test(models.Model):
    CATEGORY_CHOICES = [
        ('SPRINTS', 'Sprints'),
        ('MIDDLE_DISTANCE', 'Middle Distance'),
        ('LONG_DISTANCE', 'Long Distance'),
        ('JUMPS', 'Jumps'),
        ('THROWS', 'Throws'),
        ('COMBINED_EVENTS', 'Combined Events'),
        ('FREESTYLE', 'Freestyle Swimming'),
        ('BACKSTROKE', 'Backstroke Swimming'),
        ('BREASTSTROKE', 'Breaststroke Swimming'),
        ('BUTTERFLY', 'Butterfly Swimming'),
        ('INDIVIDUAL_MEDLEY', 'Individual Medley'),
    ]
    
    id = models.CharField(max_length=20, primary_key=True, default=generate_test_id)
    name = models.CharField(max_length=100, help_text="e.g., 100m Sprint, Long Jump", default="Test Name")
    description = models.TextField(default="Test Description")
    unit = models.CharField(max_length=20, help_text="e.g., seconds, meters, kilograms", default="seconds")
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='SPRINTS')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['category', 'name']
    
    def __str__(self):
        return f"{self.name} ({self.category})"

class Performance(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending Verification'),
        ('VERIFIED', 'Verified'),
        ('FLAGGED', 'Flagged'),
    ]
    
    FLAG_REASONS = [
        ('SUSPICIOUS_TIMING', 'Suspicious Timing'),
        ('TECHNICAL_VIOLATION', 'Technical Violation'),
        ('INVALID_VIDEO', 'Invalid Video Evidence'),
        ('OTHER', 'Other Reason'),
    ]
    
    id = models.CharField(max_length=20, primary_key=True, default=generate_performance_id)
    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name='performances')
    athlete = models.ForeignKey(Athlete, on_delete=models.CASCADE, related_name='performances')
    value = models.FloatField(help_text="Performance value in the unit specified by test")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    
    # Media fields
    video = CloudinaryField('video', blank=True, null=True, resource_type='video')
    image = CloudinaryField('image', blank=True, null=True)
    
    # Verification fields
    verified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='verified_performances')
    verified_at = models.DateTimeField(null=True, blank=True)
    verification_notes = models.TextField(blank=True)
    
    # Flagging fields
    flagged_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='flagged_performances')
    flagged_at = models.DateTimeField(null=True, blank=True)
    flag_reason = models.CharField(max_length=20, choices=FLAG_REASONS, blank=True)
    flag_notes = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['test', 'status']),
            models.Index(fields=['athlete', 'created_at']),
        ]
    
    def __str__(self):
        return f"{self.athlete.full_name} - {self.test.name}: {self.value} {self.test.unit}"

class Badge(models.Model):
    BADGE_TYPE_CHOICES = [
        ('PERFORMANCE', 'Performance Badge'),
        ('MILESTONE', 'Milestone Badge'),
        ('PARTICIPATION', 'Participation Badge'),
        ('ACHIEVEMENT', 'Achievement Badge'),
    ]
    
    id = models.CharField(max_length=20, primary_key=True, default=generate_badge_id)
    name = models.CharField(max_length=100)
    description = models.TextField()
    badge_type = models.CharField(max_length=15, choices=BADGE_TYPE_CHOICES)
    icon = models.CharField(max_length=10, default='🏆', help_text="Emoji icon for the badge")
    requirements = models.TextField(help_text="Requirements to earn this badge")
    points = models.IntegerField(default=0, help_text="Points awarded for earning this badge")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['badge_type', 'name']
    
    def __str__(self):
        return self.name

class AthleteBadge(models.Model):
    athlete = models.ForeignKey(Athlete, on_delete=models.CASCADE, related_name='badges')
    badge = models.ForeignKey(Badge, on_delete=models.CASCADE)
    earned_at = models.DateTimeField(auto_now_add=True)
    performance = models.ForeignKey(Performance, on_delete=models.SET_NULL, null=True, blank=True, 
                                  help_text="Performance that earned this badge")
    
    class Meta:
        unique_together = ['athlete', 'badge']
        ordering = ['-earned_at']
    
    def __str__(self):
        return f"{self.athlete.full_name} - {self.badge.name}"

class AthleteStats(models.Model):
    athlete = models.OneToOneField(Athlete, on_delete=models.CASCADE, related_name='stats')
    total_performances = models.IntegerField(default=0)
    verified_performances = models.IntegerField(default=0)
    pending_performances = models.IntegerField(default=0)
    flagged_performances = models.IntegerField(default=0)
    total_badges = models.IntegerField(default=0)
    total_points = models.IntegerField(default=0)
    current_rank = models.IntegerField(default=0)
    best_performances = models.JSONField(default=dict, blank=True, 
                                      help_text="Store best performance for each test")
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Athlete Statistics"
        verbose_name_plural = "Athlete Statistics"
    
    def __str__(self):
        return f"{self.athlete.full_name} Stats"

class Notification(models.Model):
    NOTIFICATION_TYPES = [
        ('PERFORMANCE_VERIFIED', 'Performance Verified'),
        ('PERFORMANCE_FLAGGED', 'Performance Flagged'),
        ('BADGE_EARNED', 'Badge Earned'),
        ('RANK_CHANGED', 'Rank Changed'),
        ('SYSTEM_UPDATE', 'System Update'),
    ]
    
    id = models.CharField(max_length=20, primary_key=True, default=generate_notification_id)
    athlete = models.ForeignKey(Athlete, on_delete=models.CASCADE, related_name='notifications')
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    title = models.CharField(max_length=200)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.athlete.full_name} - {self.title}"

class SystemSettings(models.Model):
    key = models.CharField(max_length=100, unique=True)
    value = models.TextField()
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "System Setting"
        verbose_name_plural = "System Settings"
    
    def __str__(self):
        return f"{self.key}: {self.value}"

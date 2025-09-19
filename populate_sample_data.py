#!/usr/bin/env python
"""
Sample data population script for SAI Fitness Backend
Creates initial test data including admin user, sample tests, and badges
"""
import os
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Aaarohan_Backend.settings')
django.setup()

from django.contrib.auth import get_user_model
from authapp.models import User, Athlete, Test, Badge, SystemSettings

def create_sample_data():
    """Create sample data for the SAI Fitness system"""
    
    # Create admin user
    admin_user, created = User.objects.get_or_create(
        username='admin',
        defaults={
            'email': 'admin@saifitness.com',
            'role': 'ADMIN',
            'is_staff': True,
            'is_superuser': True,
            'is_email_verified': True,
            'first_name': 'SAI',
            'last_name': 'Admin'
        }
    )
    if created:
        admin_user.set_password('admin123')
        admin_user.save()
        print(f"✅ Created admin user: {admin_user.username}")
    else:
        print(f"ℹ️  Admin user already exists: {admin_user.username}")

    # Create sample tests
    sample_tests = [
        {
            'name': '100m Sprint',
            'description': 'Standard 100-meter sprint race',
            'unit': 'seconds',
            'category': 'SPRINTS',
        },
        {
            'name': '200m Sprint', 
            'description': '200-meter sprint race',
            'unit': 'seconds',
            'category': 'SPRINTS',
        },
        {
            'name': '1500m Run',
            'description': '1500-meter middle distance run',
            'unit': 'minutes:seconds',
            'category': 'MIDDLE_DISTANCE',
        },
        {
            'name': 'Long Jump',
            'description': 'Standing or running long jump',
            'unit': 'meters',
            'category': 'JUMPS',
        },
        {
            'name': 'Shot Put',
            'description': 'Shot put throwing event',
            'unit': 'meters',
            'category': 'THROWS',
        },
        {
            'name': '50m Freestyle',
            'description': 'Freestyle swimming 50 meters',
            'unit': 'seconds',
            'category': 'FREESTYLE',
        },
    ]
    
    created_tests = []
    for test_data in sample_tests:
        test, created = Test.objects.get_or_create(
            name=test_data['name'],
            defaults=test_data
        )
        if created:
            print(f"✅ Created test: {test.name}")
        else:
            print(f"ℹ️  Test already exists: {test.name}")
        created_tests.append(test)

    # Create sample badges
    sample_badges = [
        {
            'name': 'Speed Demon',
            'description': 'Complete a 100m sprint under 12 seconds',
            'badge_type': 'PERFORMANCE',
            'icon': '⚡',
            'requirements': 'Sprint 100m in under 12.00 seconds',
            'points': 100,
        },
        {
            'name': 'Distance Runner',
            'description': 'Complete a 1500m run under 5 minutes',
            'badge_type': 'PERFORMANCE',
            'icon': '🏃',
            'requirements': 'Complete 1500m in under 5:00',
            'points': 150,
        },
        {
            'name': 'First Performance',
            'description': 'Submit your first performance',
            'badge_type': 'MILESTONE',
            'icon': '🎯',
            'requirements': 'Submit any performance for verification',
            'points': 50,
        },
        {
            'name': 'Consistent Athlete',
            'description': 'Submit 10 verified performances',
            'badge_type': 'MILESTONE',
            'icon': '🔥',
            'requirements': 'Have 10 verified performances',
            'points': 300,
        },
        {
            'name': 'Top Performer',
            'description': 'Achieve top 3 ranking in any test',
            'badge_type': 'ACHIEVEMENT',
            'icon': '🏆',
            'requirements': 'Rank in top 3 of any leaderboard',
            'points': 500,
        },
    ]
    
    for badge_data in sample_badges:
        badge, created = Badge.objects.get_or_create(
            name=badge_data['name'],
            defaults=badge_data
        )
        if created:
            print(f"✅ Created badge: {badge.name}")
        else:
            print(f"ℹ️  Badge already exists: {badge.name}")

    # Create system settings
    sample_settings = [
        {'key': 'max_file_size_mb', 'value': '50', 'description': 'Maximum file size for uploads in MB'},
        {'key': 'allowed_video_formats', 'value': 'mp4,mov,avi', 'description': 'Allowed video file formats'},
        {'key': 'allowed_image_formats', 'value': 'jpg,jpeg,png,webp', 'description': 'Allowed image file formats'},
        {'key': 'performance_auto_verify', 'value': 'False', 'description': 'Auto-verify performance submissions'},
        {'key': 'leaderboard_update_frequency', 'value': '60', 'description': 'Leaderboard update frequency in seconds'},
        {'key': 'email_notifications_enabled', 'value': 'True', 'description': 'Enable email notifications'},
    ]
    
    for setting in sample_settings:
        obj, created = SystemSettings.objects.get_or_create(
            key=setting['key'],
            defaults={
                'value': setting['value'],
                'description': setting['description']
            }
        )
        if created:
            print(f"✅ Created setting: {setting['key']}")
        else:
            print(f"ℹ️  Setting already exists: {setting['key']}")

    # Create a sample athlete account
    athlete_user, created = User.objects.get_or_create(
        username='athlete_demo',
        defaults={
            'email': 'athlete@example.com',
            'role': 'ATHLETE',
            'is_email_verified': True,
            'first_name': 'Demo',
            'last_name': 'Athlete'
        }
    )
    if created:
        athlete_user.set_password('athlete123')
        athlete_user.save()
        
        # Create athlete profile
        athlete_profile = Athlete.objects.create(
            user=athlete_user,
            first_name='Demo',
            last_name='Athlete',
            date_of_birth='1995-01-01',
            gender='MALE',
            sport='ATHLETICS',
            category='SPRINTS',
            phone='+91-9876543210',
            state='Maharashtra',
            district='Mumbai',
            address='Mumbai, Maharashtra, India',
        )
        print(f"✅ Created sample athlete: {athlete_user.username}")
    else:
        print(f"ℹ️  Sample athlete already exists: {athlete_user.username}")

    print("\n🎉 Sample data creation completed!")
    print("\n📋 Summary:")
    print(f"   • Tests: {Test.objects.count()}")
    print(f"   • Badges: {Badge.objects.count()}")
    print(f"   • Athletes: {Athlete.objects.count()}")
    print(f"   • Users: {User.objects.count()}")
    
    print("\n🔐 Login Credentials:")
    print("   Admin: username=admin, password=admin123")
    print("   Sample Athlete: username=athlete_demo, password=athlete123")
    
    print("\n🌐 API Endpoints Available:")
    print("   • POST /api/auth/register/ - Register new athlete")
    print("   • POST /api/auth/login/ - Login") 
    print("   • GET /api/auth/profile/ - Get user profile")
    print("   • GET /api/tests/ - Get all tests")
    print("   • POST /api/tests/submit/ - Submit performance")
    print("   • GET /api/leaderboard/<test_id>/ - Get leaderboard")

if __name__ == '__main__':
    create_sample_data()
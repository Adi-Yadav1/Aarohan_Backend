from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
import random
from authapp.models import User, Badge, UserBadge, Test, RecentActivity, UserStats

class Command(BaseCommand):
    help = 'Populate the database with demo data for testing'
    
    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting demo data population...'))
        
        # Create badges
        self.create_badges()
        
        # Create or get demo user
        demo_user = self.get_or_create_demo_user()
        
        # Create demo data for the user
        self.create_demo_tests(demo_user)
        self.assign_demo_badges(demo_user)
        self.create_demo_activities(demo_user)
        
        # Update user stats
        from authapp.views import update_user_stats
        update_user_stats(demo_user)
        
        self.stdout.write(self.style.SUCCESS('Demo data population completed!'))
        self.stdout.write(f'Demo user credentials:')
        self.stdout.write(f'Email: demo@aarohan.com')
        self.stdout.write(f'Password: demo123')
    
    def create_badges(self):
        """Create sample badges"""
        badges_data = [
            {
                'name': 'First Test',
                'description': 'Complete your first fitness test',
                'badge_type': 'MILESTONE',
                'icon': '🎯',
                'points': 10,
                'requirements': 'Complete 1 test'
            },
            {
                'name': 'Speed Demon',
                'description': 'Complete 5 agility tests',
                'badge_type': 'ACHIEVEMENT',
                'icon': '⚡',
                'points': 50,
                'requirements': 'Complete 5 agility tests'
            },
            {
                'name': 'Endurance Master',
                'description': 'Complete 3 endurance tests with score > 80',
                'badge_type': 'ACHIEVEMENT',
                'icon': '🏃',
                'points': 75,
                'requirements': 'Complete 3 endurance tests with score > 80'
            },
            {
                'name': 'Strength Warrior',
                'description': 'Complete 5 strength tests',
                'badge_type': 'ACHIEVEMENT',
                'icon': '💪',
                'points': 60,
                'requirements': 'Complete 5 strength tests'
            },
            {
                'name': 'Consistency Champion',
                'description': 'Take tests for 7 consecutive days',
                'badge_type': 'SPECIAL',
                'icon': '🏆',
                'points': 100,
                'requirements': 'Take tests for 7 consecutive days'
            }
        ]
        
        for badge_data in badges_data:
            badge, created = Badge.objects.get_or_create(
                name=badge_data['name'],
                defaults=badge_data
            )
            if created:
                self.stdout.write(f'Created badge: {badge.name}')
    
    def get_or_create_demo_user(self):
        """Get or create demo user"""
        email = 'demo@aarohan.com'
        try:
            user = User.objects.get(email=email)
            self.stdout.write(f'Demo user already exists: {email}')
        except User.DoesNotExist:
            user = User.objects.create_user(
                username='demo_user',
                email=email,
                password='demo123',
                first_name='Aditya',
                last_name='Yadav',
                role='ATHLETE'
            )
            self.stdout.write(f'Created demo user: {email}')
        
        # Create user stats if not exists
        UserStats.objects.get_or_create(user=user)
        
        return user
    
    def create_demo_tests(self, user):
        """Create demo tests for user"""
        test_types = ['ENDURANCE', 'STRENGTH', 'AGILITY', 'FLEXIBILITY']
        
        # Create tests from the past week
        for i in range(5):
            test_date = timezone.now() - timedelta(days=random.randint(1, 7))
            test_type = random.choice(test_types)
            score = random.uniform(60, 95)
            duration = timedelta(minutes=random.randint(15, 60))
            
            test = Test.objects.create(
                user=user,
                test_type=test_type,
                status='COMPLETED',
                score=round(score, 1),
                duration=duration,
                notes=f'Great {test_type.lower()} test session!',
                completed_at=test_date
            )
            test.created_at = test_date
            test.save()
            
            self.stdout.write(f'Created test: {test_type} - Score: {score:.1f}')
    
    def assign_demo_badges(self, user):
        """Assign demo badges to user"""
        badge_names = ['First Test', 'Speed Demon', 'Endurance Master']
        
        for badge_name in badge_names:
            try:
                badge = Badge.objects.get(name=badge_name)
                user_badge, created = UserBadge.objects.get_or_create(
                    user=user,
                    badge=badge
                )
                if created:
                    # Create badge earned activity
                    RecentActivity.objects.create(
                        user=user,
                        activity_type='BADGE_EARNED',
                        title=f'Badge earned: {badge.name}',
                        subtitle=badge.description,
                        emoji=badge.icon,
                        created_at=timezone.now() - timedelta(days=random.randint(1, 5))
                    )
                    self.stdout.write(f'Assigned badge: {badge.name}')
            except Badge.DoesNotExist:
                self.stdout.write(f'Badge not found: {badge_name}')
    
    def create_demo_activities(self, user):
        """Create demo recent activities"""
        activities_data = [
            {
                'activity_type': 'TEST_COMPLETED',
                'title': 'Endurance Test completed!',
                'subtitle': 'Score: 87.5 - Excellent performance!',
                'emoji': '🎯',
                'days_ago': 1
            },
            {
                'activity_type': 'RANK_IMPROVED',
                'title': 'Rank improved to #8!',
                'subtitle': 'Moved up from #12 - Keep it up!',
                'emoji': '🏆',
                'days_ago': 2
            },
            {
                'activity_type': 'TEST_COMPLETED',
                'title': 'Strength Test completed!',
                'subtitle': 'Score: 92.0 - Outstanding result!',
                'emoji': '💪',
                'days_ago': 3
            },
            {
                'activity_type': 'MILESTONE_REACHED',
                'title': 'Milestone: 5 tests completed!',
                'subtitle': 'You\'re on fire! Keep going!',
                'emoji': '🔥',
                'days_ago': 4
            }
        ]
        
        for activity_data in activities_data:
            activity_date = timezone.now() - timedelta(days=activity_data['days_ago'])
            RecentActivity.objects.create(
                user=user,
                activity_type=activity_data['activity_type'],
                title=activity_data['title'],
                subtitle=activity_data['subtitle'],
                emoji=activity_data['emoji'],
                created_at=activity_date
            )
            self.stdout.write(f'Created activity: {activity_data["title"]}')
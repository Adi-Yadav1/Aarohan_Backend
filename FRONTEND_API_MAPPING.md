# SAI Fitness Backend - Complete API Reference for Frontend Integration

## 🌐 Base Configuration
```
Base URL: http://127.0.0.1:8000/api/
Content-Type: application/json (for most endpoints)
Content-Type: multipart/form-data (for file uploads)
Authentication: Bearer Token (JWT)
```

## 🔐 Authentication Flow

### 1. **POST** `/auth/register/` - Register New Athlete
**Purpose:** Register a new athlete account with complete profile information

**Request Headers:**
```
Content-Type: application/json
```

**Request Body:**
```json
{
  "username": "john_athlete",
  "email": "john@example.com",
  "password": "SecurePass123!",
  "first_name": "John",
  "last_name": "Doe", 
  "date_of_birth": "1995-05-15",
  "gender": "MALE",
  "sport": "ATHLETICS",
  "category": "SPRINTS",
  "phone": "+91-9876543210",
  "state": "Maharashtra",
  "district": "Mumbai",
  "address": "123 Main Street, Andheri, Mumbai, Maharashtra"
}
```

**Success Response (201):**
```json
{
  "success": true,
  "message": "Athlete registered successfully. Please check your email for verification.",
  "data": {
    "user_id": "cm4user123abc",
    "athlete_id": "cm4ath456def789",
    "username": "john_athlete",
    "email": "john@example.com",
    "email_verification_required": true
  }
}
```

**Error Response (400):**
```json
{
  "success": false,
  "errors": {
    "username": ["This username is already taken"],
    "email": ["User with this email already exists"],
    "password": ["Password too weak"]
  }
}
```

**Frontend Usage:**
- Registration form with all athlete fields
- Password strength validation
- Email verification flow
- Duplicate username/email handling

---

### 2. **POST** `/auth/login/` - User Login
**Purpose:** Authenticate user and receive JWT tokens

**Request Headers:**
```
Content-Type: application/json
```

**Request Body:**
```json
{
  "username": "john_athlete",
  "password": "SecurePass123!"
}
```

**Success Response (200):**
```json
{
  "success": true,
  "message": "Login successful",
  "data": {
    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjk1MjA4ODAwLCJpYXQiOjE2OTUyMDUyMDAsImp0aSI6IjEyMzQ1Njc4OTAiLCJ1c2VyX2lkIjoiY200dXNlcjEyM2FiYyJ9...",
    "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY5NTgxMDAwMCwiaWF0IjoxNjk1MjA1MjAwLCJqdGkiOiI5ODc2NTQzMjEwIiwidXNlcl9pZCI6ImNtNHVzZXIxMjNhYmMifQ...",
    "user": {
      "id": "cm4user123abc",
      "username": "john_athlete", 
      "email": "john@example.com",
      "role": "ATHLETE",
      "is_email_verified": true
    },
    "athlete_profile": {
      "id": "cm4ath456def789",
      "first_name": "John",
      "last_name": "Doe",
      "sport": "ATHLETICS",
      "category": "SPRINTS"
    }
  }
}
```

**Error Response (401):**
```json
{
  "success": false,
  "message": "Invalid credentials"
}
```

**Frontend Usage:**
- Store access_token in secure storage
- Store refresh_token for token renewal
- Navigate to dashboard on success
- Show error message on failure
- Handle email verification requirement

---

### 3. **GET** `/auth/profile/` - Get User Profile
**Purpose:** Get complete user and athlete profile information

**Request Headers:**
```
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
Content-Type: application/json
```

**Success Response (200):**
```json
{
  "success": true,
  "data": {
    "user": {
      "id": "cm4user123abc",
      "username": "john_athlete",
      "email": "john@example.com",
      "first_name": "John",
      "last_name": "Doe",
      "role": "ATHLETE",
      "is_email_verified": true,
      "date_joined": "2025-09-20T10:30:00Z"
    },
    "athlete": {
      "id": "cm4ath456def789", 
      "first_name": "John",
      "last_name": "Doe",
      "date_of_birth": "1995-05-15",
      "gender": "MALE",
      "phone": "+91-9876543210",
      "state": "Maharashtra", 
      "district": "Mumbai",
      "address": "123 Main Street, Andheri, Mumbai, Maharashtra",
      "sport": "ATHLETICS",
      "category": "SPRINTS",
      "profile_image": "https://res.cloudinary.com/your-cloud/image/upload/v1695205200/profile_images/john_profile.jpg",
      "is_active": true,
      "created_at": "2025-09-20T10:30:00Z"
    }
  }
}
```

**Error Response (401):**
```json
{
  "success": false,
  "message": "Authentication credentials were not provided"
}
```

**Frontend Usage:**
- Display user profile information
- Show profile image
- Edit profile functionality
- Account settings page

---

### 4. **POST** `/auth/forgot-password/` - Request Password Reset
**Purpose:** Send password reset email to user

**Request Headers:**
```
Content-Type: application/json
```

**Request Body:**
```json
{
  "email": "john@example.com"
}
```

**Success Response (200):**
```json
{
  "success": true,
  "message": "Password reset email sent successfully. Please check your email."
}
```

**Error Response (404):**
```json
{
  "success": false,
  "message": "No user found with this email address"
}
```

**Frontend Usage:**
- Forgot password form
- Email input validation
- Success message display
- Redirect to login with message

---

### 5. **POST** `/auth/reset-password/` - Reset Password
**Purpose:** Reset password using token from email

**Request Headers:**
```
Content-Type: application/json
```

**Request Body:**
```json
{
  "token": "cm4reset789xyz123",
  "new_password": "NewSecurePass456!"
}
```

**Success Response (200):**
```json
{
  "success": true,
  "message": "Password reset successful. You can now login with your new password."
}
```

**Error Response (400):**
```json
{
  "success": false,
  "message": "Invalid or expired reset token"
}
```

**Frontend Usage:**
- Password reset form
- Token extraction from email link
- Password strength validation
- Redirect to login after success

---

## 🏃‍♂️ Test Management APIs

### 6. **GET** `/tests/` - Get All Available Tests
**Purpose:** Retrieve list of all active fitness tests

**Request Headers:**
```
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
Content-Type: application/json
```

**Success Response (200):**
```json
{
  "success": true,
  "data": [
    {
      "id": "cm4test123abc",
      "name": "100m Sprint",
      "description": "Standard 100-meter sprint race. Run as fast as possible from start to finish line.",
      "unit": "seconds",
      "category": "SPRINTS",
      "is_active": true,
      "created_at": "2025-09-20T10:00:00Z"
    },
    {
      "id": "cm4test456def", 
      "name": "Long Jump",
      "description": "Jump as far as possible from the takeoff line. Distance measured from takeoff to nearest landing point.",
      "unit": "meters",
      "category": "JUMPS",
      "is_active": true,
      "created_at": "2025-09-20T10:00:00Z"
    },
    {
      "id": "cm4test789ghi",
      "name": "1500m Run", 
      "description": "Middle distance running event. Complete 1500 meters as quickly as possible.",
      "unit": "minutes:seconds",
      "category": "MIDDLE_DISTANCE",
      "is_active": true,
      "created_at": "2025-09-20T10:00:00Z"
    },
    {
      "id": "cm4test101jkl",
      "name": "Shot Put",
      "description": "Throw the shot put as far as possible using proper technique.",
      "unit": "meters", 
      "category": "THROWS",
      "is_active": true,
      "created_at": "2025-09-20T10:00:00Z"
    },
    {
      "id": "cm4test202mno",
      "name": "50m Freestyle",
      "description": "Swim 50 meters using freestyle stroke as fast as possible.",
      "unit": "seconds",
      "category": "FREESTYLE",
      "is_active": true,
      "created_at": "2025-09-20T10:00:00Z"
    }
  ]
}
```

**Frontend Usage:**
- Test selection screen
- Test details display
- Category-wise test filtering
- Performance submission test picker

---

### 7. **POST** `/tests/submit/` - Submit Performance
**Purpose:** Submit athlete performance with optional video/image evidence

**Request Headers:**
```
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
Content-Type: multipart/form-data
```

**Request Body (Form Data):**
```javascript
const formData = new FormData();
formData.append('test_id', 'cm4test123abc');
formData.append('value', '11.75'); 
formData.append('video', videoFile); // Optional: Video file (max 50MB)
formData.append('image', imageFile); // Optional: Image file (max 50MB)  
formData.append('notes', 'Personal best attempt! Great weather conditions.');
```

**Success Response (201):**
```json
{
  "success": true,
  "message": "Performance submitted successfully. It will be reviewed by administrators.",
  "data": {
    "id": "cm4perf789xyz",
    "test": {
      "id": "cm4test123abc",
      "name": "100m Sprint",
      "unit": "seconds"
    },
    "athlete_name": "John Doe",
    "value": 11.75,
    "status": "PENDING",
    "video_url": "https://res.cloudinary.com/your-cloud/video/upload/v1695205500/performances/john_sprint_video.mp4",
    "image_url": "https://res.cloudinary.com/your-cloud/image/upload/v1695205500/performances/john_sprint_photo.jpg",
    "notes": "Personal best attempt! Great weather conditions.",
    "submitted_at": "2025-09-20T14:30:00Z"
  }
}
```

**Error Response (400):**
```json
{
  "success": false,
  "errors": {
    "test_id": ["Invalid test ID"],
    "value": ["Performance value is required"],
    "video": ["Video file too large. Maximum size is 50MB"],
    "image": ["Invalid image format. Allowed: jpg, jpeg, png, webp"]
  }
}
```

**Frontend Usage:**
- Performance submission form
- Test selection dropdown
- Value input with unit display
- Video/image file picker
- File size validation
- Upload progress indicator
- Success/error message handling

---

## 🏆 Leaderboard APIs

### 8. **GET** `/leaderboard/{test_id}/` - Get Test Leaderboard
**Purpose:** Get ranked leaderboard for a specific test with filtering options

**Request Headers:**
```
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
Content-Type: application/json
```

**URL Parameters:**
- `test_id` (required): Test identifier (e.g., `cm4test123abc`)

**Query Parameters:**
- `gender` (optional): Filter by gender (`MALE`, `FEMALE`)
- `category` (optional): Filter by athlete category (`SPRINTS`, `JUMPS`, etc.)
- `state` (optional): Filter by athlete state
- `limit` (optional): Number of results (default: 50, max: 100)

**Example Request:**
```
GET /leaderboard/cm4test123abc/?gender=MALE&category=SPRINTS&limit=20
```

**Success Response (200):**
```json
{
  "success": true,
  "data": {
    "test": {
      "id": "cm4test123abc",
      "name": "100m Sprint",
      "description": "Standard 100-meter sprint race",
      "unit": "seconds",
      "category": "SPRINTS"
    },
    "filters_applied": {
      "gender": "MALE",
      "category": "SPRINTS", 
      "limit": 20
    },
    "total_performances": 156,
    "filtered_performances": 87,
    "leaderboard": [
      {
        "rank": 1,
        "athlete_id": "cm4ath111aaa",
        "athlete_name": "Rajesh Kumar",
        "state": "Punjab",
        "district": "Ludhiana",
        "value": 10.45,
        "performance_id": "cm4perf555fff",
        "verified_at": "2025-09-20T12:00:00Z",
        "verified_by": "Admin User"
      },
      {
        "rank": 2,
        "athlete_id": "cm4ath222bbb", 
        "athlete_name": "Arjun Singh",
        "state": "Haryana",
        "district": "Gurugram", 
        "value": 10.67,
        "performance_id": "cm4perf666ggg",
        "verified_at": "2025-09-20T11:45:00Z",
        "verified_by": "Admin User"
      },
      {
        "rank": 3,
        "athlete_id": "cm4ath333ccc",
        "athlete_name": "John Doe",
        "state": "Maharashtra", 
        "district": "Mumbai",
        "value": 10.89,
        "performance_id": "cm4perf777hhh", 
        "verified_at": "2025-09-20T11:30:00Z",
        "verified_by": "Admin User"
      }
    ],
    "user_ranking": {
      "current_user_rank": 15,
      "current_user_performance": {
        "value": 11.75,
        "status": "VERIFIED",
        "verified_at": "2025-09-20T10:00:00Z"
      }
    }
  }
}
```

**Error Response (404):**
```json
{
  "success": false,
  "message": "Test not found"
}
```

**Frontend Usage:**
- Leaderboard display screen
- Ranking table with athlete info
- Filter controls (gender, category, state)
- User's own rank highlighting
- Performance value formatting
- Load more/pagination
- State and district display

---

## 📊 Performance History APIs

### 9. **GET** `/performances/my/` - Get My Performance History
**Purpose:** Get current user's performance history across all tests

**Request Headers:**
```
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
Content-Type: application/json
```

**Query Parameters:**
- `test_id` (optional): Filter by specific test
- `status` (optional): Filter by status (`PENDING`, `VERIFIED`, `FLAGGED`)
- `limit` (optional): Number of results (default: 20)
- `offset` (optional): Pagination offset

**Success Response (200):**
```json
{
  "success": true,
  "data": {
    "total_performances": 15,
    "performances": [
      {
        "id": "cm4perf789xyz",
        "test": {
          "id": "cm4test123abc",
          "name": "100m Sprint",
          "unit": "seconds",
          "category": "SPRINTS"
        },
        "value": 11.75,
        "status": "VERIFIED",
        "video_url": "https://res.cloudinary.com/your-cloud/video/upload/v1695205500/performances/sprint_video.mp4",
        "image_url": "https://res.cloudinary.com/your-cloud/image/upload/v1695205500/performances/sprint_photo.jpg",
        "notes": "Personal best attempt!",
        "submitted_at": "2025-09-20T14:30:00Z",
        "verified_at": "2025-09-20T15:00:00Z",
        "verified_by": "Admin User",
        "rank_achieved": 15,
        "personal_best": true
      },
      {
        "id": "cm4perf456def",
        "test": {
          "id": "cm4test456def",
          "name": "Long Jump", 
          "unit": "meters",
          "category": "JUMPS"
        },
        "value": 6.75,
        "status": "PENDING",
        "video_url": null,
        "image_url": "https://res.cloudinary.com/your-cloud/image/upload/v1695205400/performances/jump_photo.jpg",
        "notes": "Good jump, slight headwind",
        "submitted_at": "2025-09-20T13:15:00Z",
        "verified_at": null,
        "verified_by": null,
        "rank_achieved": null,
        "personal_best": false
      }
    ]
  }
}
```

**Frontend Usage:**
- Performance history screen
- Performance status indicators
- Personal best highlighting
- Media file viewing
- Performance details modal
- Filter controls

---

## 🏅 Badge & Achievement APIs

### 10. **GET** `/badges/available/` - Get Available Badges
**Purpose:** Get list of all badges and achievement criteria

**Request Headers:**
```
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
Content-Type: application/json
```

**Success Response (200):**
```json
{
  "success": true,
  "data": [
    {
      "id": "cm4badge111aaa",
      "name": "Speed Demon",
      "description": "Complete a 100m sprint under 12 seconds",
      "badge_type": "PERFORMANCE",
      "icon": "⚡",
      "requirements": "Sprint 100m in under 12.00 seconds",
      "points": 100,
      "is_active": true,
      "earned_by_user": false,
      "total_earned": 45
    },
    {
      "id": "cm4badge222bbb", 
      "name": "Distance Runner",
      "description": "Complete a 1500m run under 5 minutes",
      "badge_type": "PERFORMANCE",
      "icon": "🏃",
      "requirements": "Complete 1500m in under 5:00",
      "points": 150,
      "is_active": true,
      "earned_by_user": true,
      "earned_at": "2025-09-20T10:30:00Z",
      "total_earned": 23
    },
    {
      "id": "cm4badge333ccc",
      "name": "First Performance", 
      "description": "Submit your first performance",
      "badge_type": "MILESTONE",
      "icon": "🎯",
      "requirements": "Submit any performance for verification",
      "points": 50,
      "is_active": true,
      "earned_by_user": true,
      "earned_at": "2025-09-20T09:00:00Z",
      "total_earned": 234
    }
  ]
}
```

**Frontend Usage:**
- Badges showcase screen
- Achievement progress indicators
- Earned badges highlighting
- Badge details modal
- Progress tracking

---

### 11. **GET** `/badges/my/` - Get My Badges
**Purpose:** Get current user's earned badges

**Request Headers:**
```
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
Content-Type: application/json
```

**Success Response (200):**
```json
{
  "success": true,
  "data": {
    "total_badges": 3,
    "total_points": 350,
    "badges": [
      {
        "id": "cm4badge333ccc",
        "name": "First Performance",
        "description": "Submit your first performance", 
        "badge_type": "MILESTONE",
        "icon": "🎯",
        "points": 50,
        "earned_at": "2025-09-20T09:00:00Z",
        "performance_that_earned": {
          "id": "cm4perf789xyz",
          "test_name": "100m Sprint",
          "value": 11.75
        }
      },
      {
        "id": "cm4badge222bbb",
        "name": "Distance Runner", 
        "description": "Complete a 1500m run under 5 minutes",
        "badge_type": "PERFORMANCE",
        "icon": "🏃",
        "points": 150,
        "earned_at": "2025-09-20T10:30:00Z",
        "performance_that_earned": {
          "id": "cm4perf456def",
          "test_name": "1500m Run",
          "value": "4:45"
        }
      },
      {
        "id": "cm4badge444ddd",
        "name": "Consistent Athlete",
        "description": "Submit 10 verified performances",
        "badge_type": "MILESTONE", 
        "icon": "🔥",
        "points": 150,
        "earned_at": "2025-09-20T16:00:00Z",
        "performance_that_earned": null
      }
    ]
  }
}
```

**Frontend Usage:**
- My badges screen
- Badge collection display
- Achievement notifications
- Points leaderboard
- Badge sharing functionality

---

## 📊 Statistics & Analytics APIs

### 12. **GET** `/stats/my/` - Get My Statistics
**Purpose:** Get comprehensive statistics for current user

**Request Headers:**
```
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
Content-Type: application/json
```

**Success Response (200):**
```json
{
  "success": true,
  "data": {
    "overall_stats": {
      "total_performances": 15,
      "verified_performances": 12,
      "pending_performances": 2,
      "flagged_performances": 1,
      "total_badge_points": 350,
      "badges_earned": 3,
      "personal_bests": 8,
      "average_rank": 12.5,
      "best_rank": 3,
      "registration_date": "2025-09-20T09:00:00Z",
      "last_performance": "2025-09-20T16:30:00Z"
    },
    "performance_by_category": [
      {
        "category": "SPRINTS",
        "total_performances": 6,
        "verified_performances": 5,
        "best_performance": {
          "test_name": "100m Sprint",
          "value": 11.75,
          "rank": 15
        },
        "average_rank": 18.2
      },
      {
        "category": "JUMPS",
        "total_performances": 4,
        "verified_performances": 3, 
        "best_performance": {
          "test_name": "Long Jump",
          "value": 6.75,
          "rank": 8
        },
        "average_rank": 12.7
      }
    ],
    "recent_achievements": [
      {
        "type": "BADGE_EARNED",
        "badge_name": "Consistent Athlete",
        "earned_at": "2025-09-20T16:00:00Z"
      },
      {
        "type": "PERSONAL_BEST",
        "test_name": "100m Sprint", 
        "old_value": 12.15,
        "new_value": 11.75,
        "improvement": 0.40,
        "achieved_at": "2025-09-20T14:30:00Z"
      },
      {
        "type": "RANK_IMPROVEMENT",
        "test_name": "Long Jump",
        "old_rank": 12,
        "new_rank": 8,
        "improvement": 4,
        "achieved_at": "2025-09-20T13:15:00Z"
      }
    ]
  }
}
```

**Frontend Usage:**
- Dashboard statistics
- Performance analytics charts
- Achievement timeline
- Progress tracking
- Personal records display

---

## 📱 Notification APIs

### 13. **GET** `/notifications/` - Get Notifications
**Purpose:** Get user's notifications

**Request Headers:**
```
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
Content-Type: application/json
```

**Query Parameters:**
- `unread_only` (optional): Get only unread notifications (`true`/`false`)
- `limit` (optional): Number of results (default: 20)

**Success Response (200):**
```json
{
  "success": true,
  "data": {
    "total_notifications": 25,
    "unread_count": 3,
    "notifications": [
      {
        "id": "cm4notif111aaa",
        "notification_type": "PERFORMANCE_VERIFIED",
        "title": "Performance Verified! 🎉",
        "message": "Your 100m Sprint performance (11.75s) has been verified and you ranked #15!",
        "is_read": false,
        "created_at": "2025-09-20T15:00:00Z",
        "related_performance": {
          "id": "cm4perf789xyz",
          "test_name": "100m Sprint",
          "value": 11.75,
          "rank": 15
        }
      },
      {
        "id": "cm4notif222bbb",
        "notification_type": "BADGE_EARNED",
        "title": "New Badge Earned! 🏅",
        "message": "Congratulations! You earned the 'Consistent Athlete' badge for submitting 10 verified performances.",
        "is_read": false,
        "created_at": "2025-09-20T16:00:00Z",
        "related_badge": {
          "id": "cm4badge444ddd",
          "name": "Consistent Athlete",
          "icon": "🔥",
          "points": 150
        }
      },
      {
        "id": "cm4notif333ccc",
        "notification_type": "RANK_CHANGED",
        "title": "Ranking Update 📈", 
        "message": "Your ranking in Long Jump improved from #12 to #8! Keep up the great work!",
        "is_read": true,
        "created_at": "2025-09-20T13:30:00Z",
        "related_performance": {
          "id": "cm4perf456def",
          "test_name": "Long Jump",
          "old_rank": 12,
          "new_rank": 8
        }
      }
    ]
  }
}
```

**Frontend Usage:**
- Notification center
- Push notification handling
- Badge notifications
- Performance update alerts
- Unread count display

---

### 14. **PATCH** `/notifications/{id}/mark-read/` - Mark Notification as Read
**Purpose:** Mark specific notification as read

**Request Headers:**
```
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
Content-Type: application/json
```

**Success Response (200):**
```json
{
  "success": true,
  "message": "Notification marked as read"
}
```

**Frontend Usage:**
- Mark notifications as read when viewed
- Update unread count
- Notification interaction tracking

---

## 🔍 Search & Filter APIs

### 15. **GET** `/search/athletes/` - Search Athletes
**Purpose:** Search for athletes by name, location, or sport

**Request Headers:**
```
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
Content-Type: application/json
```

**Query Parameters:**
- `q` (required): Search query
- `sport` (optional): Filter by sport
- `state` (optional): Filter by state
- `limit` (optional): Number of results (default: 20)

**Example Request:**
```
GET /search/athletes/?q=john&sport=ATHLETICS&state=Maharashtra&limit=10
```

**Success Response (200):**
```json
{
  "success": true,
  "data": {
    "total_results": 45,
    "athletes": [
      {
        "id": "cm4ath123abc",
        "first_name": "John",
        "last_name": "Doe",
        "profile_image": "https://res.cloudinary.com/your-cloud/image/upload/v1695205200/profiles/john.jpg",
        "sport": "ATHLETICS",
        "category": "SPRINTS", 
        "state": "Maharashtra",
        "district": "Mumbai",
        "total_badges": 3,
        "badge_points": 350,
        "best_performances": [
          {
            "test_name": "100m Sprint",
            "value": 11.75,
            "rank": 15
          }
        ]
      }
    ]
  }
}
```

**Frontend Usage:**
- Athlete search functionality
- Social features
- Competitor analysis
- Performance comparison

---

## 🏋️‍♂️ Admin APIs (For Admin Role)

### 16. **GET** `/admin/dashboard/` - Admin Dashboard Stats
**Purpose:** Get comprehensive admin dashboard statistics

**Request Headers:**
```
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
Content-Type: application/json
```

**Success Response (200):**
```json
{
  "success": true,
  "data": {
    "overview": {
      "total_athletes": 1250,
      "total_performances": 5670,
      "pending_verifications": 45,
      "total_tests": 12,
      "total_badges": 15,
      "active_athletes_today": 89,
      "performances_today": 23
    },
    "performance_stats": {
      "by_status": {
        "verified": 5234,
        "pending": 45,
        "flagged": 391
      },
      "by_category": [
        {"category": "SPRINTS", "count": 1567},
        {"category": "JUMPS", "count": 1234},
        {"category": "THROWS", "count": 987}
      ]
    },
    "recent_activity": [
      {
        "type": "PERFORMANCE_SUBMITTED",
        "athlete_name": "John Doe",
        "test_name": "100m Sprint",
        "value": 11.75,
        "submitted_at": "2025-09-20T16:45:00Z"
      }
    ]
  }
}
```

**Frontend Usage:**
- Admin dashboard
- Statistics charts
- Activity monitoring
- Performance analytics

---

### 17. **GET** `/admin/performances/pending/` - Get Pending Verifications
**Purpose:** Get performances awaiting admin verification

**Request Headers:**
```
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
Content-Type: application/json
```

**Success Response (200):**
```json
{
  "success": true,
  "data": {
    "total_pending": 45,
    "performances": [
      {
        "id": "cm4perf789xyz",
        "athlete": {
          "id": "cm4ath123abc",
          "name": "John Doe",
          "sport": "ATHLETICS",
          "state": "Maharashtra"
        },
        "test": {
          "id": "cm4test123abc", 
          "name": "100m Sprint",
          "unit": "seconds",
          "category": "SPRINTS"
        },
        "value": 11.75,
        "video_url": "https://res.cloudinary.com/your-cloud/video/upload/v1695205500/performances/sprint_video.mp4",
        "image_url": "https://res.cloudinary.com/your-cloud/image/upload/v1695205500/performances/sprint_photo.jpg", 
        "notes": "Personal best attempt!",
        "submitted_at": "2025-09-20T14:30:00Z"
      }
    ]
  }
}
```

**Frontend Usage:**
- Admin verification queue
- Performance review interface
- Media file viewing
- Batch verification actions

---

### 18. **PATCH** `/admin/performances/{id}/verify/` - Verify Performance
**Purpose:** Verify or flag a performance submission

**Request Headers:**
```
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
Content-Type: application/json
```

**Request Body:**
```json
{
  "status": "VERIFIED",
  "admin_notes": "Performance looks legitimate. Good video quality and proper technique shown."
}
```

**Success Response (200):**
```json
{
  "success": true,
  "message": "Performance verified successfully",
  "data": {
    "performance_id": "cm4perf789xyz",
    "status": "VERIFIED",
    "verified_at": "2025-09-20T17:00:00Z",
    "verified_by": "Admin User",
    "new_rank": 15
  }
}
```

**Frontend Usage:**
- Performance verification interface
- Status update handling
- Admin action logging
- Notification triggers

---

## 🔧 System Configuration APIs

### 19. **GET** `/system/settings/` - Get System Settings
**Purpose:** Get current system configuration

**Request Headers:**
```
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
Content-Type: application/json
```

**Success Response (200):**
```json
{
  "success": true,
  "data": {
    "file_upload": {
      "max_file_size_mb": 50,
      "allowed_video_formats": ["mp4", "mov", "avi"],
      "allowed_image_formats": ["jpg", "jpeg", "png", "webp"]
    },
    "performance": {
      "auto_verify": false,
      "verification_required": true
    },
    "leaderboard": {
      "update_frequency_minutes": 60,
      "default_limit": 50,
      "max_limit": 100
    },
    "notifications": {
      "email_enabled": true,
      "push_enabled": true
    }
  }
}
```

**Frontend Usage:**
- File upload validation
- Configuration-based UI behavior
- Feature flags
- Upload limits display

---

## 🎯 Error Handling & Status Codes

### HTTP Status Codes
- **200 OK** - Successful GET/PATCH requests
- **201 Created** - Successful POST requests (resource created)  
- **400 Bad Request** - Invalid request data/validation errors
- **401 Unauthorized** - Missing or invalid authentication
- **403 Forbidden** - Insufficient permissions
- **404 Not Found** - Resource not found
- **413 Payload Too Large** - File size exceeds limit
- **429 Too Many Requests** - Rate limit exceeded
- **500 Internal Server Error** - Server error

### Error Response Format
```json
{
  "success": false,
  "message": "Error description",
  "errors": {
    "field_name": ["Specific field error message"],
    "another_field": ["Another error message"]
  },
  "error_code": "VALIDATION_ERROR"
}
```

### Common Error Scenarios
1. **Authentication Errors:**
   - Expired JWT tokens → Return 401, refresh token
   - Invalid credentials → Show error message

2. **Validation Errors:**
   - File size too large → Show size limit message
   - Invalid file format → Show allowed formats
   - Required fields missing → Highlight required fields

3. **Permission Errors:**
   - Admin-only endpoints → Show access denied message
   - User trying to access other user's data → Redirect to login

---

## 🔐 Authentication Implementation Guide

### Token Management
```javascript
// Store tokens securely
const storeTokens = (accessToken, refreshToken) => {
  // Use secure storage (Keychain on iOS, Keystore on Android)
  SecureStore.setItemAsync('access_token', accessToken);
  SecureStore.setItemAsync('refresh_token', refreshToken);
};

// Add token to API requests
const apiRequest = async (url, options = {}) => {
  const token = await SecureStore.getItemAsync('access_token');
  
  return fetch(`${BASE_URL}${url}`, {
    ...options,
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json',
      ...options.headers,
    },
  });
};

// Handle token refresh
const refreshToken = async () => {
  const refresh = await SecureStore.getItemAsync('refresh_token');
  
  const response = await fetch(`${BASE_URL}/auth/token/refresh/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ refresh }),
  });
  
  if (response.ok) {
    const data = await response.json();
    await storeTokens(data.access, refresh);
    return data.access;
  }
  
  // Refresh failed, redirect to login
  redirectToLogin();
};
```

---

## 📱 Frontend Integration Checklist

### Authentication Flow
- [ ] Login form with username/password
- [ ] Registration form with all athlete fields
- [ ] Token storage and management  
- [ ] Auto token refresh
- [ ] Logout functionality
- [ ] Password reset flow

### Main Features
- [ ] Dashboard with user stats
- [ ] Test list and selection
- [ ] Performance submission with file upload
- [ ] Leaderboard with filtering
- [ ] Performance history
- [ ] Badge collection
- [ ] Notification center
- [ ] Profile management

### File Upload
- [ ] Camera integration for video/photo
- [ ] File size validation
- [ ] Upload progress indicator
- [ ] File format validation
- [ ] Compression for large files

### Offline Support
- [ ] Cache user profile data
- [ ] Queue performance submissions
- [ ] Sync when online
- [ ] Offline indicator

### Performance
- [ ] Image lazy loading
- [ ] API response caching
- [ ] Pagination for large lists
- [ ] Optimistic updates

This comprehensive API reference provides everything your frontend AI needs to integrate with the SAI Fitness backend. Each endpoint includes detailed request/response examples, error handling, and specific frontend usage guidelines. 🚀
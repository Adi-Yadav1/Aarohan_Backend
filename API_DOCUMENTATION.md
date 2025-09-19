# Aarohan Backend API Documentation

This document describes the API endpoints available for the Aarohan fitness app dashboard functionality.

## Base URL
```
http://localhost:8000/api/
```

## Authentication
All dashboard endpoints require JWT authentication. Include the token in the Authorization header:
```
Authorization: Bearer <your_jwt_token>
```

## Endpoints Overview

### Authentication Endpoints

#### 1. Login
```
POST /api/auth/login/
```

**Request Body:**
```json
{
    "email": "demo@aarohan.com",
    "password": "demo123"
}
```

**Response:**
```json
{
    "success": true,
    "message": "Login successful",
    "data": {
        "user": {
            "id": 1,
            "username": "demo_user",
            "email": "demo@aarohan.com",
            "role": "ATHLETE"
        },
        "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
    }
}
```

#### 2. Signup
```
POST /api/auth/signup/
```

**Request Body:**
```json
{
    "email": "newuser@example.com",
    "password": "password123",
    "role": "ATHLETE"
}
```

### Dashboard Endpoints

#### 3. Get Complete Dashboard Data
```
GET /api/dashboard/
```

**Response:**
```json
{
    "success": true,
    "data": {
        "user": {
            "id": "1",
            "username": "demo_user",
            "first_name": "Aditya",
            "last_name": "Yadav",
            "email": "demo@aarohan.com",
            "profile_image": null,
            "name": "Aditya Yadav"
        },
        "stats": {
            "total_tests": 5,
            "current_rank": 10,
            "total_badges": 3,
            "total_points": 185,
            "improvement_percentage": 8.5,
            "last_test_date": "2025-09-18T10:30:00Z",
            "last_test_date_formatted": "1 day ago"
        },
        "recentActivities": [
            {
                "id": "activity-1",
                "type": "TEST_COMPLETED",
                "title": "Endurance Test completed!",
                "subtitle": "Score: 87.5 - Excellent performance!",
                "emoji": "🎯",
                "timestamp": "2025-09-18T10:30:00Z"
            }
        ],
        "badges": [
            {
                "badge": {
                    "id": 1,
                    "name": "First Test",
                    "description": "Complete your first fitness test",
                    "badge_type": "MILESTONE",
                    "icon": "🎯",
                    "points": 10
                },
                "earned_at": "2025-09-15T14:20:00Z"
            }
        ]
    }
}
```

#### 4. Get User Profile
```
GET /api/profile/
```

**Response:**
```json
{
    "success": true,
    "data": {
        "id": "1",
        "username": "demo_user",
        "first_name": "Aditya",
        "last_name": "Yadav",
        "email": "demo@aarohan.com",
        "profile_image": null,
        "name": "Aditya Yadav"
    }
}
```

#### 5. Get User Statistics
```
GET /api/stats/
```

**Response:**
```json
{
    "success": true,
    "data": {
        "total_tests": 5,
        "current_rank": 10,
        "total_badges": 3,
        "total_points": 185,
        "improvement_percentage": 8.5,
        "last_test_date": "2025-09-18T10:30:00Z",
        "last_test_date_formatted": "1 day ago"
    }
}
```

#### 6. Get Recent Activities
```
GET /api/activities/
```

**Response:**
```json
{
    "success": true,
    "data": [
        {
            "id": "activity-1",
            "type": "TEST_COMPLETED",
            "title": "Endurance Test completed!",
            "subtitle": "Score: 87.5 - Excellent performance!",
            "emoji": "🎯",
            "timestamp": "2025-09-18T10:30:00Z"
        }
    ]
}
```

### Test Management Endpoints

#### 7. Get User Tests
```
GET /api/tests/
```

**Response:**
```json
{
    "success": true,
    "data": [
        {
            "id": "test-uuid-1",
            "test_type": "ENDURANCE",
            "status": "COMPLETED",
            "score": 87.5,
            "duration": "00:45:00",
            "created_at": "2025-09-18T09:00:00Z",
            "completed_at": "2025-09-18T09:45:00Z",
            "notes": "Great endurance test session!"
        }
    ]
}
```

#### 8. Create New Test
```
POST /api/tests/create/
```

**Request Body:**
```json
{
    "test_type": "ENDURANCE",
    "notes": "Starting endurance test session"
}
```

**Response:**
```json
{
    "success": true,
    "message": "Test created successfully",
    "data": {
        "id": "new-test-uuid",
        "test_type": "ENDURANCE",
        "status": "PENDING",
        "score": null,
        "duration": null,
        "created_at": "2025-09-19T10:00:00Z",
        "completed_at": null,
        "notes": "Starting endurance test session"
    }
}
```

#### 9. Update Test Results
```
PUT /api/tests/<test_id>/update/
```

**Request Body:**
```json
{
    "status": "COMPLETED",
    "score": 89.5,
    "duration": "00:42:30",
    "notes": "Excellent performance today!"
}
```

**Response:**
```json
{
    "success": true,
    "message": "Test updated successfully",
    "data": {
        "id": "test-uuid",
        "test_type": "ENDURANCE",
        "status": "COMPLETED",
        "score": 89.5,
        "duration": "00:42:30",
        "created_at": "2025-09-19T10:00:00Z",
        "completed_at": "2025-09-19T10:42:30Z",
        "notes": "Excellent performance today!"
    }
}
```

### Badge and Leaderboard Endpoints

#### 10. Get User Badges
```
GET /api/badges/
```

**Response:**
```json
{
    "success": true,
    "data": [
        {
            "badge": {
                "id": 1,
                "name": "First Test",
                "description": "Complete your first fitness test",
                "badge_type": "MILESTONE",
                "icon": "🎯",
                "points": 10
            },
            "earned_at": "2025-09-15T14:20:00Z"
        }
    ]
}
```

#### 11. Get Leaderboard
```
GET /api/leaderboard/
```

**Response:**
```json
{
    "success": true,
    "data": [
        {
            "rank": 1,
            "user_id": "user-uuid-1",
            "username": "top_athlete",
            "name": "John Doe",
            "total_points": 500,
            "total_tests": 25,
            "total_badges": 12,
            "profile_image": null
        }
    ]
}
```

## Test Types Available
- `ENDURANCE` - Endurance Test
- `STRENGTH` - Strength Test  
- `AGILITY` - Agility Test
- `FLEXIBILITY` - Flexibility Test

## Activity Types
- `TEST_COMPLETED` - Test Completed
- `BADGE_EARNED` - Badge Earned
- `RANK_IMPROVED` - Rank Improved
- `MILESTONE_REACHED` - Milestone Reached

## Error Responses
All endpoints return error responses in this format:
```json
{
    "success": false,
    "message": "Error description here",
    "errors": {} // Optional validation errors
}
```

## Integration Notes for React Native

1. **Authentication Flow:**
   - First, call `/api/auth/login/` to get the JWT token
   - Store the token securely (AsyncStorage)
   - Include the token in all subsequent API calls

2. **Dashboard Data Loading:**
   - Use `/api/dashboard/` for the main dashboard screen
   - This endpoint provides all data needed for your HomeScreen component

3. **Real-time Updates:**
   - Call `/api/stats/` periodically to update user statistics
   - Refresh activities with `/api/activities/` when user performs actions

4. **Test Flow:**
   - Create test with `/api/tests/create/` when user starts a test
   - Update test with results using `/api/tests/<id>/update/` when completed
   - This will automatically update stats and create activities

## Demo Credentials
```
Email: demo@aarohan.com
Password: demo123
```

## Sample Frontend Integration Code

### Login Function
```javascript
const login = async (email, password) => {
  try {
    const response = await fetch('http://localhost:8000/api/auth/login/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ email, password }),
    });
    
    const data = await response.json();
    
    if (data.success) {
      await AsyncStorage.setItem('jwt_token', data.data.token);
      await AsyncStorage.setItem('user_data', JSON.stringify(data.data.user));
      return data.data;
    } else {
      throw new Error(data.message);
    }
  } catch (error) {
    console.error('Login error:', error);
    throw error;
  }
};
```

### Dashboard Data Fetch
```javascript
const fetchDashboardData = async () => {
  try {
    const token = await AsyncStorage.getItem('jwt_token');
    
    const response = await fetch('http://localhost:8000/api/dashboard/', {
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json',
      },
    });
    
    const data = await response.json();
    
    if (data.success) {
      return data.data;
    } else {
      throw new Error(data.message);
    }
  } catch (error) {
    console.error('Dashboard fetch error:', error);
    throw error;
  }
};
```

The API is fully compatible with your existing React Native HomeScreen component structure and provides all the data needed for the dashboard functionality.
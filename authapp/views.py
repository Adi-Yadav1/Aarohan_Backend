from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import LoginSerializer, UserSerializer
from .models import User

@api_view(["POST"])
@permission_classes([AllowAny])
def login_view(request):
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data["user"]
        refresh = RefreshToken.for_user(user)
        return Response({
            "success": True,
            "message": "Login successful",
            "data": {
                "user": UserSerializer(user).data,
                "token": str(refresh.access_token),
            }
        }, status=status.HTTP_200_OK)
    return Response({"success": False, "message": serializer.errors}, status=400)

@api_view(["POST"])
@permission_classes([AllowAny])
def signup_view(request):
    email = request.data.get("email")
    password = request.data.get("password")
    role = request.data.get("role", "ATHLETE")

    if User.objects.filter(email=email).exists():
        return Response({"success": False, "message": "Email already exists"}, status=400)

    user = User.objects.create_user(
        username=email,
        email=email,
        password=password,
        role=role.upper()
    )
    return Response({
        "success": True,
        "message": "User created successfully",
        "data": UserSerializer(user).data
    }, status=201)

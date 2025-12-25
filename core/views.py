from django.shortcuts import render
from rest_framework import viewsets, filters, status
from .models import Event, Alert
from .serializers import EventSerializer, AlertSerializer, RegisterSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenObtainPairSerializer
from .permissions import IsAnalystReadOnly, IsAdmin
from rest_framework import generics
from .models import User
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.views import APIView
from rest_framework.response import Response

from rest_framework.permissions import IsAdminUser

def dashboard(request):
    return render(request, 'dashboard.html')

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class RegisterView(APIView):
    permission_classes = []  # Allow anyone

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "User registered successfully"},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsAdmin]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        
        if not serializer.is_valid():
            # Return validation errors
            return Response({
                "success": False,
                "errors": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        event = serializer.save()

        return Response({
            "success": True,
            "message": "Event created successfully",
            "data": serializer.data
        }, status=status.HTTP_201_CREATED)


class AlertViewSet(viewsets.ModelViewSet):
    queryset = Alert.objects.select_related('event')
    serializer_class = AlertSerializer
    permission_classes = [IsAnalystReadOnly]

    filter_backends = [DjangoFilterBackend]
    filterset_fields = {
        'status': ['exact'],
        'event__severity': ['exact'],
    }
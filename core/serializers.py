from rest_framework import serializers
from .models import Event, Alert, User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.exceptions import AuthenticationFailed

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):
        username = attrs.get("username")
        password = attrs.get("password")

        # Check user exists
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise AuthenticationFailed("User does not exist")

        # Check password
        if not user.check_password(password):
            raise AuthenticationFailed("Password is not correct")

        # Call parent (this sets self.user)
        data = super().validate(attrs)

        # Keep your existing response
        data['user'] = {
            'id': self.user.id,
            'username': self.user.username,
            'role': self.user.role
        }

        return data


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'password','role')

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            role=validated_data['role'],
        )
        return user


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'

    def validate_source_name(self, value):
        if not value.strip():
            raise serializers.ValidationError("Source name cannot be empty")
        return value

    def validate_event_type(self, value):
        if not value.strip():
            raise serializers.ValidationError("Event type cannot be empty")
        return value

    def validate_severity(self, value):
        allowed = ['LOW', 'MEDIUM', 'HIGH', 'CRITICAL']
        if value not in allowed:
            raise serializers.ValidationError(
                f"Severity must be one of {allowed}"
            )
        return value

    def validate_description(self, value):
        if len(value.strip()) < 5:
            raise serializers.ValidationError(
                "Description must be at least 5 characters long"
            )
        return value

class AlertSerializer(serializers.ModelSerializer):
    event = EventSerializer(read_only=True)

    class Meta:
        model = Alert
        fields = '__all__'

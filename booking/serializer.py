from rest_framework import serializers
from .models import *
from rest_framework_simplejwt.tokens import RefreshToken

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    is_staff = serializers.BooleanField(required=False)

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password', 'department', 'position', 'employee_id', 'is_staff')

    def create(self, validated_data):
        password = validated_data.pop('password')
        is_staff = validated_data.pop('is_staff', False)

        user = CustomUser(**validated_data)
        user.set_password(password)
        user.is_staff = is_staff
        user.save()

        refresh = RefreshToken.for_user(user)

        return {
            'username': user.username,
            'email': user.email,
            'department': user.department,
            'position': user.position,
            'employee_id': user.employee_id,
            'is_staff': user.is_staff,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        exclude = ['user']

    def create(self, validated_data):
        request = self.context.get('request')
        if request and hasattr(request, "user"):
            validated_data['user'] = request.user
        return super().create(validated_data)
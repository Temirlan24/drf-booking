
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import *

urlpatterns = [
    path('auth/register/', UserRegistrationView.as_view(), name='register'),
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('rooms/', RoomListCreateAPIView.as_view(), name='room'),
    path('rooms/<int:pk>/', RoomDetailAPIView.as_view(), name='room-detail'),
    path('bookings/', BookingListCreateAPIView.as_view(), name='booking'),
    path('bookings/<int:pk>/', BookingDetailAPIView.as_view(), name='booking-detail'),
]

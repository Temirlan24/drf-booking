from django.shortcuts import render
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializer import *
from django.shortcuts import get_object_or_404

class UserRegistrationView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RoomListCreateAPIView(APIView):
    def get(self, request):
        rooms = Room.objects.all()
        serializer = RoomSerializer(rooms, many=True)
        return Response(serializer.data)

    def post(self, request):
        if not request.user.is_staff:
            return Response({"error": "Only admins can add rooms."}, status=status.HTTP_403_FORBIDDEN)

        serializer = RoomSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RoomDetailAPIView(APIView):
    def get(self, request, pk):
        room = get_object_or_404(Room, pk=pk)
        serializer = RoomSerializer(room)
        return Response(serializer.data)

    def put(self, request, pk):
        if not request.user.is_staff:
            return Response({"error": "Only admins can update rooms."}, status=status.HTTP_403_FORBIDDEN)

        room = get_object_or_404(Room, pk=pk)
        serializer = RoomSerializer(room, data=request.data, partial=True)  # Allow partial updates
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        if not request.user.is_staff:
            return Response({"error": "Only admins can delete rooms."}, status=status.HTTP_403_FORBIDDEN)

        room = get_object_or_404(Room, pk=pk)
        room.delete()
        return Response({"message": "Room deleted successfully."}, status=status.HTTP_204_NO_CONTENT)


class BookingListCreateAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        if request.user.is_staff:
            bookings = Booking.objects.all()
        else:
            bookings = Booking.objects.filter(user=request.user)

        serializer = BookingSerializer(bookings, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = BookingSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BookingDetailAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, pk, user):
        booking = get_object_or_404(Booking, pk=pk)
        if not user.is_staff and booking.user != user:
            return None
        return booking

    def get(self, request, pk):
        booking = self.get_object(pk, request.user)
        if not booking:
            return Response({"error": "Unauthorized access."}, status=status.HTTP_403_FORBIDDEN)

        serializer = BookingSerializer(booking)
        return Response(serializer.data)

    def put(self, request, pk):
        booking = self.get_object(pk, request.user)
        if not booking:
            return Response({"error": "Unauthorized access."}, status=status.HTTP_403_FORBIDDEN)

        if 'room' in request.data and booking.user != request.user:
            return Response({"error": "Only the user who booked this room can change it."}, status=status.HTTP_403_FORBIDDEN)

        serializer = BookingSerializer(booking, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, pk):
        booking = self.get_object(pk, request.user)
        if not booking:
            return Response({"error": "Unauthorized access."}, status=status.HTTP_403_FORBIDDEN)

        booking.delete()
        return Response({"message": "Booking deleted successfully."}, status=status.HTTP_204_NO_CONTENT)


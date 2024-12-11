from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404
from .models import Hotel, Room, Favorites
from users.models import Guest
from .forms import BookRoomForm
from django.contrib.auth.decorators import login_required
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializers import HotelSerializer, RoomSerializer, FavoritesSerializer
from rest_framework.views import APIView

def list_hotels(request):
    hotels = get_list_or_404(Hotel)
    return render(request, 'hotels.html', {'hotels':hotels})

def hotel_detail(request, hotel_id):
    hotel = get_object_or_404(Hotel, id=hotel_id)
    return render(request, 'hotel_detail.html', {'hotel':hotel})

@login_required(login_url='/login/')
def booking_room(request, hotel_id):
    hotel = get_object_or_404(Hotel, id=hotel_id)
    rooms = Room.objects.filter(hotel=hotel, reserved=False)

    if request.method == 'POST':
        form = BookRoomForm(request.POST, hotel=hotel)
        if form.is_valid():
            room = form.cleaned_data['room']  # Получаем выбранную комнату
            room.reserved = True  # Помечаем как забронированную
            room.save()  # Сохраняем изменения

            guest = Guest.objects.create(user=request.user, room=room)

            return redirect('booked', hotel_id=hotel.id, room_id=room.id)
    else:
        form = BookRoomForm(hotel=hotel)

    return render(request, 'booking_room.html', {'hotel': hotel, 'rooms': rooms, 'form': form})

@login_required
def booked(request, hotel_id, room_id):
    guest = get_object_or_404(Guest, user = request.user, room_id=room_id)
    room = get_object_or_404(Room, id = room_id)
    return render(request, 'booked.html', {'guest': guest, 'room': room})


class HotelViewSet(viewsets.ModelViewSet):
    queryset = Hotel.objects.all()
    serializer_class = HotelSerializer
    permission_classes = [IsAuthenticated]

class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = [IsAuthenticated]

class FavoritesViewSet(viewsets.ModelViewSet):
    queryset = Favorites.objects.all()
    serializer_class = FavoritesSerializer
    permission_classes = [IsAuthenticated]


class HotelRoomListCreateView(APIView):
    def get(self, request, hotel_id):
        try:
            hotel = Hotel.objects.get(id=hotel_id)
        except Hotel.DoesNotExist:
            return Response({"error ": "Hotel not found"}, status=status.HTTP_404_NOT_FOUND)

        rooms = Room.objects.filter(hotel=hotel)
        serializer = RoomSerializer(rooms, many=True)
        return Response(serializer.data)

    def post(self, request, hotel_id):
        try:
            hotel = Hotel.objects.get(id=hotel_id)
        except Hotel.DoesNotExist:
            return Response({"error": "Hotel not found"}, status=status.HTTP_404_NOT_FOUND)

        data = request.data.copy()
        data['hotel'] = hotel.id

        serializer = RoomSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class HotelRoomDetailView(APIView):
    def get(self, request, hotel_id, room_id):
        try:
            hotel = Hotel.objects.get(id=hotel_id)
            room = Room.objects.get(id=room_id, hotel=hotel)
        except (Hotel.DoesNotExist, Room.DoesNotExist):
            return Response({"error": "Hotel or Room not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = RoomSerializer(room)
        return Response(serializer.data)

    def put(self, request, hotel_id, room_id):
        try:
            hotel = Hotel.objects.get(id=hotel_id)
            room = Room.objects.get(id=room_id, hotel=hotel)
        except (Hotel.DoesNotExist, Room.DoesNotExist):
            return Response({"error": "Hotel or Room not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = RoomSerializer(room, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, hotel_id, room_id):
        try:
            hotel = Hotel.objects.get(id=hotel_id)
            room = Room.objects.get(id=room_id, hotel=hotel)
        except (Hotel.DoesNotExist, Room.DoesNotExist):
            return Response({"error": "Hotel or Room not found"}, status=status.HTTP_404_NOT_FOUND)

        room.delete()
        return Response({"message": "Room deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

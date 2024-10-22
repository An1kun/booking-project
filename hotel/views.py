from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404
from .models import Hotel, Room
from users.models import Guest
from .forms import BookRoomForm
from django.contrib.auth.decorators import login_required

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
from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404
from .models import Hotel, Room
from .forms import BookRoomForm

def list_hotels(request):
    hotels = get_list_or_404(Hotel)
    return render(request, 'hotels.html', {'hotels':hotels})

def hotel_detail(request, hotel_id):
    hotel = get_object_or_404(Hotel, id=hotel_id)
    return render(request, 'hotel_detail.html', {'hotel':hotel})

def booking_room(request, hotel_id):
    hotel = get_object_or_404(Hotel, id=hotel_id)
    rooms = Room.objects.filter(hotel=hotel, reserved=False)

    if request.method == 'POST':
        form = BookRoomForm(request.POST, hotel=hotel)
        if form.is_valid():
            room = form.cleaned_data['room']  # Получаем выбранную комнату
            room.reserved = True  # Помечаем как забронированную
            room.save()  # Сохраняем изменения
            return redirect('hotel_detail', hotel_id=hotel.id)
    else:
        form = BookRoomForm(hotel=hotel)

    return render(request, 'booking_room.html', {'hotel': hotel, 'rooms': rooms, 'form': form})


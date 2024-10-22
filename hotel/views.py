from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404
from .models import Hotel, Room

def list_hotels(request):
    hotels = get_list_or_404(Hotel)
    return render(request, 'hotels.html', {'hotels':hotels})

def hotel_detail(request, hotel_id):
    hotel = get_object_or_404(Hotel, id=hotel_id)
    return render(request, 'hotel_detail.html', {'hotel':hotel})

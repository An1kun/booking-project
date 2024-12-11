from django.test import Client, TestCase
from hotel.forms import BookRoomForm
from hotel.models import Favorites, Hotel, Room
from hotel.serializers import RoomSerializer
import users
from users.models import Guest
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class HotelTestCase(TestCase):
    def setUp(self):
        self.hotel = Hotel.objects.create(name='Test Hotel',city='Test City',description='Test Description',photo='hotel_images/test.jpg')
        self.room = Room.objects.create(hotel=self.hotel, reserved=False)
        self.user = users.models.User.objects.create_user(username='testuser', password='12345')
        self.favorites = Favorites.objects.create(user=self.user, hotel=self.hotel)

    def test_hotel_name(self):
        self.assertEqual(self.hotel.name, 'Test Hotel') # Check if the hotel name is correct  

    def test_hotel_list(self):
        hotels = Hotel.objects.all()
        self.assertEqual(hotels.count(), 1) # Check if the hotel list contains only one hotel

    def test_room_reserved(self):
        self.assertEqual(self.room.reserved, False) # Check if the room is not reserved

    def test_hotel_detail(self):
        hotel = Hotel.objects.get(name='Test Hotel')
        self.assertEqual(hotel.city, 'Test City') # Check if the hotel city is correct 



class BookingRoomViewTest(TestCase):
    def setUp(self):
        # Create a user and log them in
        self.user = users.models.User.objects.create_user(username='testuser', password='12345')
        self.client.login(username="testuser", password="12345")

        # Create a hotel and rooms
        self.hotel = Hotel.objects.create(name="Test Hotel")
        self.room1 = Room.objects.create(hotel=self.hotel, reserved=False)

        # URL for the view
        self.url = reverse('booking_room', args=[self.hotel.id])

    def test_get_request(self):
        # Send GET request
        response = self.client.get(self.url)

        # Check response status and template
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'booking_room.html')

        # Check context data
        self.assertEqual(response.context['hotel'], self.hotel)
        self.assertIn(self.room1, response.context['rooms'])  # Only non-reserved rooms
        self.assertIsInstance(response.context['form'], BookRoomForm)


    def test_post_valid_data(self):
        # Send POST request with valid data
        response = self.client.post(self.url, {'room': self.room1.id})

        # Reload room from the database
        self.room1.refresh_from_db()
        self.assertTrue(self.room1.reserved)  # Check if the room is reserved

        # Check Guest creation
        guest = Guest.objects.get(user=self.user, room=self.room1)
        self.assertIsNotNone(guest)

        # Check redirect
        self.assertRedirects(response, reverse('booked', args=[self.hotel.id, self.room1.id]))


    def test_post_invalid_data(self):
        # Send POST request with invalid data (e.g., no room selected)
        response = self.client.post(self.url, {'room': ''})

        # Check that the form re-renders with errors
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'booking_room.html')
        self.assertFalse(Room.objects.filter(id=self.room1.id, reserved=True).exists())


    def test_unauthenticated_user_redirect(self):
        # Log out the user
        self.client.logout()

        # Send GET request
        response = self.client.get(self.url)

        # Check redirect to login
        self.assertRedirects(response, f'/login/?next={self.url}')





class BookedViewTest(TestCase):
    def setUp(self):
        # Create a user and log them in
        self.user = users.models.User.objects.create_user(username='testuser', password='12345')
        self.client.login(username="testuser", password="12345")

        # Create a hotel and rooms
        self.hotel = Hotel.objects.create(name="Test Hotel")
        self.room1 = Room.objects.create(hotel=self.hotel, reserved=False)

        # Create a guest
        self.guest = Guest.objects.create(user=self.user, room=self.room1)

        # URL for the view
        self.url = reverse('booked', args=[self.hotel.id, self.room1.id])

    def test_get_request(self):
        # Send GET request
        response = self.client.get(self.url)

        # Check response status and template
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'booked.html')

        # Check context data
        self.assertEqual(response.context['guest'], self.guest)
        self.assertEqual(response.context['room'], self.room1)
    

class RoomViewSetTest(APITestCase):
    def setUp(self):
        self.hotel = Hotel.objects.create(name='Test Hotel',city='Test City',description='Test Description',photo='hotel_images/test.jpg')
        self.room = Room.objects.create(hotel=self.hotel, reserved=False)
        self.user = users.models.User.objects.create_user(username='testuser', password='12345')
        self.favorites = Favorites.objects.create(user=self.user, hotel=self.hotel)

        
    
    




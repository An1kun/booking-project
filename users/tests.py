from django.test import TestCase

# Create your tests here.
# tests.py
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.test import Client

from hotel.models import Hotel
from .models import Review

from .forms import ReviewForm, UserRegistationForm


class RegistrationViewTests(TestCase):

    def test_registration_view(self):
        response = self.client.get(reverse('registration'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration.html')

    def test_registration_form(self):
        form_data = {
            'username': 'testuser',
            'email': ' ',
            'password1': '12345',
            'password2': '12345'
        }
        form = UserRegistationForm(data=form_data)
        self.assertFalse(form.is_valid())


class HotelReviewsViewTests(TestCase):

    def test_hotel_reviews_view(self):
        hotel = Hotel.objects.create(name='Test Hotel', city='Test City', description='Test Description',
                                     photo='hotel_images/test.jpg')
        response = self.client.get(reverse('hotel_reviews', args=[hotel.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'hotel_reviews.html')
        self.assertEqual(response.context['hotel'], hotel)
        self.assertQuerysetEqual(response.context['reviews'], [])

    def test_review_form(self):
        hotel = Hotel.objects.create(name='Test Hotel', city='Test City', description='Test Description',
                                     photo='hotel_images/test.jpg')
        form_data = {
            'stars': 5,
            'content': 'Test Content'
        }
        form = ReviewForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_create_review_view(self):
        hotel = Hotel.objects.create(name='Test Hotel', city='Test City', description='Test Description',
                                     photo='hotel_images/test.jpg')
        response = self.client.get(reverse('create_review', args=[hotel.id]))
        self.assertEqual(response.status_code, 302)

    def test_delete_review_view(self):
        hotel = Hotel.objects.create(name='Test Hotel', city='Test City', description='Test Description',
                                     photo='hotel_images/test.jpg')
        review = Review.objects.create(hotel=hotel,
                                       user=User.objects.create_user(username='testuser', password='12345'), stars=5,
                                       content='Test Content')
        response = self.client.get(reverse('delete_review', args=[hotel.id, review.id]))
        self.assertEqual(response.status_code, 302)

    def test_edit_review_view(self):
        hotel = Hotel.objects.create(name='Test Hotel', city='Test City', description='Test Description',
                                     photo='hotel_images/test.jpg')
        review = Review.objects.create(hotel=hotel,
                                       user=User.objects.create_user(username='testuser', password='12345'), stars=5,
                                       content='Test Content')
        response = self.client.get(reverse('edit_review', args=[hotel.id, review.id]))
        self.assertEqual(response.status_code, 302)

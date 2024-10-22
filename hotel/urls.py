from django.urls import path
from . import views

urlpatterns = [
    path("hotels/", views.list_hotels, name="hotels"),
    path("hotels/<int:hotel_id>/", views.hotel_detail, name="hotel_detail"),
    path("hotels/<int:hotel_id>/booking", views.booking_room, name="booking_room")
]
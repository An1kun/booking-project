from . import views
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import HotelViewSet, RoomViewSet, FavoritesViewSet
from .views import HotelRoomListCreateView, HotelRoomDetailView

router = DefaultRouter()
router.register(r'hotels', HotelViewSet)
router.register(r'rooms', RoomViewSet)
router.register(r'favorites', FavoritesViewSet)

urlpatterns = [
    path("hotels/", views.list_hotels, name="hotels"),
    path("hotels/<int:hotel_id>/", views.hotel_detail, name="hotel_detail"),
    path("hotels/<int:hotel_id>/booking", views.booking_room, name="booking_room"),
    path("hotels/<int:hotel_id>/booking/booked/<int:room_id>", views.booked, name="booked"),
    path('api/', include(router.urls)),
]
urlpatterns += [
    path('api/hotel/<int:hotel_id>/room/', HotelRoomListCreateView.as_view(), name='hotel-room-list-create'),
    path('api/hotel/<int:hotel_id>/room/<int:room_id>/', HotelRoomDetailView.as_view(), name='hotel-room-detail'),
]
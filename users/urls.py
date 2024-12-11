from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("registration/", views.registration, name="registration"),
    path("login/", auth_views.LoginView.as_view(template_name = 'login.html'), name='login'),
    path("hotels/<int:hotel_id>/reviews", views.hotel_reviews, name="hotel_reviews"),
    path('hotels/<int:hotel_id>/reviews/create/', views.create_review, name='create_review'),
    path('hotels/<int:hotel_id>/reviews/<int:review_id>/edit', views.edit_review, name='edit_review'),
    path('hotels/<int:hotel_id>/reviews/<int:review_id>/delete', views.delete_review, name='delete_review'),
    path('chart/', views.generate_chart, name='generate_chart'),
]

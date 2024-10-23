from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404
from django.contrib import messages
from .forms import UserRegistationForm
from .models import User, Employee, Review
from hotel.models import Hotel
from .forms import ReviewForm
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required


def registration(request):
    if request.method == "POST":
        user_form = UserRegistationForm(request.POST)

        if user_form.is_valid():
            user = user_form.save()

        return redirect("login")

    else:
        user_form = UserRegistationForm()

    return render(request, 'registration.html', {'user_form': user_form})


def hotel_reviews(request, hotel_id):
    hotel = get_object_or_404(Hotel, id=hotel_id)
    reviews = Review.objects.filter(hotel=hotel)
    return render(request, 'hotel_reviews.html', {'hotel': hotel, 'reviews': reviews})


@login_required(login_url='/login/')
def create_review(request, hotel_id):
    hotel = get_object_or_404(Hotel, id=hotel_id)

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.hotel = hotel
            review.user = request.user
            review.save()
            return redirect('hotels')
    else:
        form = ReviewForm()

    return render(request, 'create_review.html', {'form': form, 'hotel': hotel})


@login_required(login_url='/login/')
def edit_review(request, hotel_id, review_id):
    review = get_object_or_404(Review, id=review_id)
    if review.user != request.user:
        return HttpResponse('Error')
    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            return redirect('hotel_reviews', hotel_id=review.hotel.id)
    else:
        form = ReviewForm(instance=review)

    return render(request, 'edit_review.html', {'form': form, 'review': review})

@login_required(login_url='/login/')
def delete_review(request, hotel_id, review_id):
    review = get_object_or_404(Review, id=review_id)
    if review.user != request.user:
        return HttpResponse('Error')
    if request.method == 'POST':
        review.delete()
        return redirect('hotel_reviews', hotel_id=review.hotel.id)

    return render(request, 'delete_review.html', {'review': review})


from django.shortcuts import render, redirect, get_list_or_404
from django.contrib import messages
from .forms import UserRegistationForm
from .models import User


def registration(request):
    if request.method == "POST":
        user_form = UserRegistationForm(request.POST)

        if user_form.is_valid():
            user = user_form.save()

        redirect("login")

    else:
        user_form = UserRegistationForm()

    return render(request, 'registration.html', {'user_form': user_form})



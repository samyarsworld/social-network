from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from authMain.decorators import unauthenticated_user
from .models import User, Profile
from mail.models import Email

import re



def dashboard(request):
    profile = None
    if request.user.is_authenticated:
        profile = Profile.objects.get(user=request.user)
    return render(request, 'authMain/dashboard.html', {'user_profile':profile})

@unauthenticated_user
def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"].lower()
        password = request.POST["password"]

        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("dashboard"))
        else:
            return render(request, "authMain/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "authMain/login.html")

@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("dashboard"))

@unauthenticated_user
def register(request):
    if request.method == "POST":
        username = request.POST["username"].lower()
        email = request.POST["email"].lower()
        name = request.POST["name"].lower()
        last = request.POST["last"].lower()

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "authMain/register.html", {
                "message": "Passwords must match."
            })    

        # Ensure password criteria is met    
        if len(password) < 8 or not re.search(r'\d', password) or not re.search(r'[a-zA-Z]', password):
            return render(request, 'authMain/register.html', {"message": 'Password must be at least 8 characters long and contain at least one digit and one letter'})

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
            profile = Profile(user=user, name=name, last=last)
            profile.save()

            # Create greeting email for all users
            host = User.objects.get(email="sam@sam.ca")
            subject = f"Welcome {user.username.capitalize()}!"
            body = "Greeting! Please use email addresses made on this website to communicate with your friends. Real email feature will be added soon!"
            email = Email(
            user=user,
            sender=host,
            subject=subject,
            body=body,
            read=False
            )
            email.save()
            email.recipients.add(user)
            email.save()


        except IntegrityError:
            return render(request, "authMain/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("dashboard"))
    else:
        return render(request, "authMain/register.html")
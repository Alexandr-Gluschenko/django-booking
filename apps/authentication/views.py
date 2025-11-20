from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .forms import LoginForm, SignUpForm


def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, "You have successfully logged in.")
                return redirect("home:index")
            else:
                messages.error(request, "Invalid credentials.")
        else:
            messages.error(request, "Please correct the errors in the form.")
    else:
        form = LoginForm()

    return render(request, "accounts/login.html", {"form": form})


def register_user(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)

        if form.is_valid():
            user = form.save()

            login(request, user)
            messages.success(request, "Account created successfully!")
            return redirect("home:index")

        else:
            messages.error(request, "Please correct the errors below.")

    else:
        form = SignUpForm()

    return render(request, "accounts/register.html", {"form": form})
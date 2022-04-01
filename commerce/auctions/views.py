from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

from .models import User, Listing, Bid, Comment, Category
from .forms import ListingForm


def index(request):
    listings = Listing.objects.all()

    return render(request, "auctions/index.html", {
        "listings": listings
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


def listing(request, listing_id):
    listing = Listing.objects.get(id=listing_id)
    return render(request, 'auctions/listing.html', {
        'listing': listing
    })


def categories(request):
    categories = Category.objects.all()
    return render(request, 'auctions/categories.html', {
        'categories': categories
    })


def category_listings(request, category_id):
    category = Category.objects.get(id=category_id)
    # We will reuse the same template for Active Listings, but specity the category
    return render(request, 'auctions/index.html', {
        'listings': category.category_listings.all(),
        'category': category.name
    })


# Create a new listing
@login_required(login_url="login")
def create_listing(request):
    # If a listing was created via POST
    if request.method == 'POST':
        # We are using ModelForms to manage our model data
        # See https://docs.djangoproject.com/en/4.0/topics/forms/modelforms/
        # Create a form and populate it with the POST request data
        form = ListingForm(request.POST)

        if form.is_valid():
            # Create a new listing, but don't commit it to the database (since it does not have the 'user' data yet)
            listing = form.save(commit=False)
            # Add the user to the Listing object
            listing.user = request.user
            # Now we save / commit the Listing to the database
            listing.save()
            # Redirect to home page
            return redirect(reverse('index'))

        # Since we are using ModelForms, we don't need to parse the cleaned_data one by one; we can just save the ModelForm into the corresponding Model object
        # if form.is_valid():
        #     # title = form.cleaned_data['title']
        #     # description = form.cleaned_data['description']
        #     # starting_bid = form.cleaned_data['starting_bid']
        #     # category = form.cleaned_data['category']
        #     # img_url = form.cleaned_data['img_url']

            
    else:
        # If GET request, we create a blank form
        form = ListingForm()

    return render(request, 'auctions/create_listing.html', {
        'form': form
    })


# Check watch list
@login_required(login_url="login")
def watchlist(request):
    return render(request, 'auctions/watchlist.html')
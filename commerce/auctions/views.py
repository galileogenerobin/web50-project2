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
    # Check if there are existing bids
    bids = listing.bids.all()
    highest_bid = None
    if bids is not None:
        # Get the highest bid for the given listing, by first querying for all bids (.bids.all()), then ordering by amount and getting the first value
        highest_bid = listing.bids.all().order_by('-amount').first()
    
    in_watchlist = False
    # Check if listing is in users' watchlist
    if listing in request.user.watchlist.all():
        in_watchlist = True

    return render(request, 'auctions/listing.html', {
        'listing': listing,
        'highest_bid': highest_bid,
        'in_watchlist': in_watchlist,
    })


def categories(request):
    categories = Category.objects.all()
    return render(request, 'auctions/categories.html', {
        'categories': categories
    })


def category_listings(request, category_id):
    category = Category.objects.get(id=category_id)
    # We will reuse the same template for Active Listings, but here we will specify the category
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
            # Add the current user to the Listing object
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
    # Since we know the user is logged in for this view, we can just get the user's current watchlist
    watchlist = request.user.watchlist.all()

    return render(request, 'auctions/watchlist.html', {
        'watchlist': watchlist
    })


# Submit a bid
@login_required(login_url="login")
def submit_bid(request, listing_id):
    # We only process POST requests
    if request.method == "POST":
        bid_amount = int(request.POST['bid_amount'])
        # Get the listing from the database using the listing_id submitted in the form
        listing = Listing.objects.get(id=listing_id)
        
        # Check existing bids for the listing
        bids = listing.bids.all()
        # The highest bid is either None (if there are no bids), or the highest bid...
        # ...which is obtained via order_by('-amount').first(); take note of the '-' sign before 'amount', denoting descending order)
        highest_bid = None if not bids else bids.order_by('-amount').first()
        # If there are no existing bids and the bid amount is less than the starting bid, OR the bid amount is less than the highest bid
        if (not bids and bid_amount <= listing.starting_bid) or (bids and bid_amount <= highest_bid.amount):
            # Show an error on the listing page
            return render(request, 'auctions/listing.html', {
                'listing': listing,
                'highest_bid': highest_bid,
                'failed_bid': True,
                'current_bid': bid_amount
            })

        # After validating the bid amount above, we can create a new bid and tag it to the current user who submitted the request
        bid = Bid(listing=listing, user=request.user, amount=bid_amount)
        bid.save()
        # And redirect to the listing page with the updated highest bid
        return redirect(reverse('listing', args=(listing.id,)))
    
    # If GET request, redirect to index
    return redirect(reverse('index'))


# Add a listing to the watchlist
@login_required(login_url="login")
def add_to_watchlist(request, listing_id):
    # We will only process POST requests
    if request.method == 'POST':
        # Get the Listing object
        listing = Listing.objects.get(id=listing_id)
        # If valid listing, add the listing to the user's watchlist and return to the listing page
        if listing:
            request.user.watchlist.add(listing)
            return redirect(reverse('listing', args=(listing.id,)))
        # Otherwise, don't process the request and redirect to index (which will happen via our last line below)

    # If GET request, redirect to index
    return redirect(reverse('index'))


# Remove a listing from the watchlist
@login_required(login_url='login')
def remove_from_watchlist(request, listing_id):
    # We will only process POST requests for
    if request.method == 'POST':
        # Get the Listing object
        listing = Listing.objects.get(id=listing_id)
        # If valid listing, remove from the user's watchlist
        if listing:
            # If the listing is not already in the user's watchlist, this won't do anything
            request.user.watchlist.remove(listing)
            # Redirect to the listing page or the watchlist page, depending on where the request was made
            if request.POST['request_source'] == 'watchlist':
                return redirect(reverse('watchlist'))
            return redirect(reverse('listing', args=(listing.id,)))

    # If GET request, redirect to index
    return redirect(reverse('index'))
from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime


class User(AbstractUser):
    pass


# Creating a Model for an auction listing, inhereting from models.Model
class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=1000)
    starting_bid = models.PositiveIntegerField()
    # Recall that related_name allows us to do a reverse search, i.e. for a given User, User.listings.all() gives us all related Listings for that User
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")
    # Optional Category and image URL fields
    category = models.ForeignKey('Category', on_delete=models.CASCADE, blank=True, null=True, related_name="category_listings")
    img_url = models.URLField(blank=True)

    # Creating a timestamp field for when the listing was created; we will make this field read-only in our admin page (see admin.py)
    created = models.DateTimeField(auto_now_add=True)
    # Timestamp for any updates
    last_updated = models.DateTimeField(auto_now=True)

    # Using choices for our status codes (since this list will be static), from https://docs.djangoproject.com/en/4.0/topics/db/models/
    STATUS_CHOICES = (
        ('Closed', 'Closed'),
        ('Active', 'Active')
    )
    status = models.CharField(max_length=64, choices=STATUS_CHOICES, default='Active')

    # Creating a Many to Many Field with Users to create our Watchlist
    watching = models.ManyToManyField(User, blank=True, related_name='watchlist')

    def __str__(self):
        return self.title


# Creating a Model for an auction bid
class Bid(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_bids")
    amount = models.PositiveIntegerField()
    # Adding a timestamp for when the Bid was placed
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{} bid for {} - amount: {}'.format(self.user, self.listing, self.amount)


# Creating a Model for a listing comment
class Comment(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="listing_comments")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_comments")
    content = models.CharField(max_length=5000)
    # Adding a timestamp for when the Comment was created
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 'Comment {} by {} on {}'.format(self.id, self.user, self.listing)


# Creating a Model for listing categories
class Category(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name
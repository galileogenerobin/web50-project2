from django.contrib.auth.models import AbstractUser
from django.db import models


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

    def __str__(self):
        return self.title


# Creating a Model for an auction bid
class Bid(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_bids")
    amount = models.PositiveIntegerField()

    def __str__(self):
        return '{} bid for {} - amount: {}'.format(self.user, self.listing, self.amount)


# Creating a Model for a listing comment
class Comment(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="listing_comments")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_comments")
    content = models.CharField(max_length=5000)

    def __str__(self):
        return 'Comment {} by {} on {}'.format(self.id, self.user, self.listing)


# Creating a Model for listing categories
class Category(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name
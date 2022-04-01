from django.contrib import admin
from .models import User, Listing, Bid, Comment, Category

# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "first_name", "last_name", "email")


class ListingAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "description", "starting_bid", "user", "category")


class BidAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "listing", "amount")


class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "content")


class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name")


admin.site.register(User, UserAdmin)
admin.site.register(Listing, ListingAdmin)
admin.site.register(Bid, BidAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Category, CategoryAdmin)
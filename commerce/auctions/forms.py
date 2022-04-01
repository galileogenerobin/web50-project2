# We import the ModelForm class
from django.forms import ModelForm
# And we import the models from our models module
from .models import Listing

# We create a separate forms.py file for our Django forms

class ListingForm(ModelForm):
    class Meta:
        model = Listing
        # We don't include the 'user' field since this will automatically be the current logged in user
        # Note: we don't use exclude = ['user'] because according to Django documentation this is less secure
        # See https://docs.djangoproject.com/en/4.0/topics/forms/modelforms/, 'Selecting the fields to use'
        fields = ['title', 'description', 'starting_bid', 'category', 'img_url']
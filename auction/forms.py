from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm
from django import forms
from .models import Listing


class CreateListingForm(ModelForm):
    image = forms.ImageField()
    price = forms.IntegerField()

    class Meta:
        model = Listing
        fields = '__all__'
        exclude = ['owner', 'date', 'watchlist', 'bid_price', 'image_url','is_active']

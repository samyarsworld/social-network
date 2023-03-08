from django.contrib import admin
from .models import *

admin.site.register(Listing)
admin.site.register(Category)
admin.site.register(Bid)
admin.site.register(ListingComment)
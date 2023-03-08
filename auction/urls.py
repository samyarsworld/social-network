from django.urls import path
from . import views

app_name = "auction"

urlpatterns = [
    path("", views.home, name="home"),
    path('listings/<int:listing_id>', views.listing, name='listing'),
    path('remove_listing/<int:listing_id>', views.removeListing, name='remove-listing'),
    path('sell_listing/<int:listing_id>', views.sellListing, name='sell-listing'),
    path("category", views.category, name="category"),
    path('create_listing', views.createListing, name='create-listing'),
    
    path("add_watchlist", views.addWatchlist, name="add-watchlist"),
    path("remove_watchlist", views.removeWatchlist, name="remove-watchlist"),
    path("watchlist", views.watchlist, name="watchlist"),
    
    path("add_comment", views.addComment, name="add-comment"),

    path("add_bid", views.addBid, name="add-bid")
]

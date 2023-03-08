from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import ListingComment, Listing, Bid, Category
from .forms import CreateListingForm


def home(request):
    listings = Listing.objects.filter(is_active=True)
    categories = Category.objects.all()
    return render(request, "auction/home.html", {
        'listings': listings,
        'categories': categories
    })

@login_required
def createListing(request):
    if request.method == 'POST':
        form = CreateListingForm(request.POST)
        listing = form.save(commit=False)
        listing.owner = request.user
        
        bid = Bid(bid=1000.0, bid_owner=request.user)
        bid.save()
        listing.price = bid

        listing.save()

        return redirect(reverse('auction:home'))
        
    form = CreateListingForm()
    return render(request, 'auction/createListing.html', {
        'form': form
    })


def category(request):
    if request.method == 'POST':
        category = request.POST['category']
        category_object = Category.objects.get(category_name=category)
        categories = Category.objects.exclude(category_name=category)
        listings = Listing.objects.filter(is_active=True, category=category_object) 
        return render(request, 'auction/category.html', {
            'listings': listings,
            'categories': categories,
            'category': category
        })

@login_required
def listing(request, listing_id):
    listing = Listing.objects.get(id=listing_id)
    comments = ListingComment.objects.filter(listing=listing)
    if listing in request.user.user_watchlists.all():
        watchlist = True
    else:
        watchlist = False

    return render(request, 'auction/listing.html', {
        'listing': listing,
        'watchlist': watchlist,
        'comments': comments
    })


@login_required
def addWatchlist(request):
    if request.method == 'POST':
        listing = Listing.objects.get(id=request.POST['listing_id'])
        listing.watchlist.add(request.user)
        listing.save()
        return redirect(reverse('auction:listing', args = (listing.id,)))

@login_required
def removeWatchlist(request):
    if request.method == 'POST':
        listing = Listing.objects.get(id=request.POST['listing_id'])
        listing.watchlist.remove(request.user)
        listing.save()
        return redirect(reverse('auction:listing', args = (listing.id,)))


@login_required
def watchlist(request):
    watchlists = request.user.user_watchlists.all()

    return render(request, 'auction/watchlist.html', {
        'watchlists': watchlists
    })

@login_required
def addComment(request):
    if request.method == 'POST':
        id = request.POST['listing_id']
        listing = Listing.objects.get(id=id)
        content = request.POST['comment']
        comment = ListingComment(content=content, listing=listing, author=request.user)
        comment.save()

        return redirect(reverse('auction:listing', args = (listing.id,)))


@login_required
def addBid(request):
    if request.method == 'POST':
        id = request.POST['listing_id']
        listing = Listing.objects.get(id=id)
        bid = float(request.POST['bid'])
        current_bid = listing.price.bid
        comments = ListingComment.objects.filter(listing=listing)
        if listing in request.user.user_watchlists.all():
            watchlist = True
        else:
            watchlist = False

        if bid > current_bid:
            newBid = Bid(bid=bid, bid_owner=request.user)
            newBid.save()
            listing.price = newBid
            listing.save()
            
            return render(request, 'auction/listing.html', {
                'listing': listing,
                'comments': comments,
                'update': True,
                'watchlist': watchlist
            })

        else:
            return render(request, 'auction/listing.html', {
                'listing': listing,
                'comments': comments,
                'update': False,
                'watchlist': watchlist
            })

@login_required
def removeListing(request, listing_id):
    if request.method == 'POST':
        listing = Listing.objects.get(id=listing_id)
        listing.delete()
        return redirect(reverse('auction:home'))

@login_required
def sellListing(request, listing_id):
    if request.method == 'POST':
        listing = Listing.objects.get(id=listing_id)
        listing.is_active = False
        listing.save()
        buyer = listing.price.bid_owner
        comments = ListingComment.objects.filter(listing=listing)


        return render(request, 'auction/listing.html', {
            'listing': listing,
            'comments': comments,
            'message': f'Sold to {buyer} for ${listing.price.bid}'
        })

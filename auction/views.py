from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import ListingComment, Listing, Bid, Category
from .forms import CreateListingForm
import os
import boto3


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
        form = CreateListingForm(request.POST , request.FILES)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.owner = request.user
            price = form.cleaned_data['price'] or 1
            bid = Bid(bid=price, bid_owner=request.user)
            bid.save()
            listing.bid_price = bid

            if request.FILES['image']:
                image_file = request.FILES['image']
                # Connect to S3
                s3 = boto3.client('s3')
                # Upload the image file to S3
                s3.upload_fileobj(image_file, os.getenv('AWS_STORAGE_BUCKET_NAME'), 'static/auction_images/' + image_file.name)
            
                # Get the URL of the uploaded image
                url = f"https://s3.amazonaws.com/{os.getenv('AWS_STORAGE_BUCKET_NAME')}/{'static/auction_images/' + image_file.name}"
                listing.image_url = url
            listing.save()

            return redirect(reverse('auction:home'))
        else:
            print(form.errors)
    
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
        current_bid = listing.bid_price.bid
        comments = ListingComment.objects.filter(listing=listing)
        if listing in request.user.user_watchlists.all():
            watchlist = True
        else:
            watchlist = False

        if bid > current_bid:
            newBid = Bid(bid=bid, bid_owner=request.user)
            newBid.save()
            listing.bid_price = newBid
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
        buyer = listing.bid_price.bid_owner
        comments = ListingComment.objects.filter(listing=listing)


        return render(request, 'auction/listing.html', {
            'listing': listing,
            'comments': comments,
            'message': f'Sold to {buyer} for ${listing.bid_price.bid}'
        })

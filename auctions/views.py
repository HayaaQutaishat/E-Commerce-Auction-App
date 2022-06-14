from distutils.command.bdist_dumb import bdist_dumb
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from auctions.models import Listing, User, Bid, Comment, Categories 
from django.contrib.auth.decorators import login_required
from django import forms
from django.contrib import messages
from django.db.utils import OperationalError
from django.db.models import Max
from django.contrib.auth.models import AnonymousUser



class NewListingForm(forms.Form):
    title = forms.CharField(label="Title", widget=forms.TextInput(attrs={
      "placeholder": "Listing Title",
      "class": "col-md-8 col-lg-7"}))
    description = forms.CharField(label="Description", widget=forms.Textarea(attrs={
      "placeholder": "Listing Description",
      "class": "col-md-8 col-lg-7",
      "rows": 7,
      }))
    bid = forms.DecimalField(label="Bid($)" ,max_digits=10, decimal_places=2,widget=forms.TextInput(attrs={
      "placeholder": "Listing Bid",
      "class": "col-md-8 col-lg-7"}))
    image = forms.URLField(label="Image URL" ,max_length=1000, required=False, widget=forms.TextInput(attrs={
      "placeholder": "Image URL",
      "class": "col-md-8 col-lg-7"}))
      #to get the categories from database
    CATEGORIES_CHOICES = [(obj.type,obj.type) for obj in Categories.objects.all()]
    category = forms.ChoiceField(required=False, widget=forms.Select, choices=CATEGORIES_CHOICES)


class NewCommentForm(forms.Form):
    comment = forms.CharField(label='',widget=forms.Textarea(attrs={
      "placeholder": "Add Comment...",
      "class": "form-control col-md-8 col-lg-12",
      "rows": 5,
      }))

def index(request):
    return render(request, "auctions/index.html",{
        "listings": Listing.objects.all(),
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

@login_required()
def new_listing(request):
    if request.method == "POST":
        #to get what the user submit in the form create new form instance
        form = NewListingForm(request.POST)
        #we don't trust what the user typed so we have to do this step:
        if form.is_valid():
            title = form.cleaned_data["title"]
            description = form.cleaned_data["description"]
            image = form.cleaned_data["image"]
            bid = form.cleaned_data["bid"]
            category = form.cleaned_data["category"]
            category_obj = Categories.objects.get(type=category)
            listing = Listing.create(title=title, description=description, bid=bid, image=image, category=category_obj, user=request.user)
            listing.save()
            bid_object = Bid.create(request.user,bid,listing)
            bid_object.save() 
            return HttpResponseRedirect(reverse("index"))
    
    else:
        return render(request, "auctions/newlisting.html",{
            "form": NewListingForm(),
            "categories": Categories.objects.all()
        })

def listing(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    comments = listing.comments.all()
    total_comments = comments.count()

    #get the user who created the listing
    user = listing.user
    #get the logged in user
    logged_in_user = request.user

    if user == logged_in_user:
        created_by_user = True
    else:
        created_by_user = False

    #total number of bids on this listing
    bids = listing.listings.all()
    total_bids = bids.count()

    # Only check watchlist and max bid for authenticated users
    if isinstance(user,User):
    
        user = request.user
        if listing in user.watchlist.all():
            in_watchlist = True
        else:
            in_watchlist = False

        current_winner = False
        #All bids on the current listing from all users
        bids = Bid.objects.filter(listing=listing)
        #the highest bid on this listing (DESC order)
        highest_bid = Bid.objects.filter(listing=listing).order_by('-amount').first() or 0
        #the user of this highest bid
        user = highest_bid.user
        #if the user who has the highest bid is the user who is currently logged in << current_winner = True
        if user == request.user:
            current_winner = True

    return render(request, "auctions/listing.html",{
        "listing": listing,
        "comment_form": NewCommentForm(),
        "in_watchlist": in_watchlist,
        "total_comments":  total_comments,
        "total_bids": total_bids,
        "created_by_user": created_by_user,
        "current_winner": current_winner,
    })

@login_required()
def place_bid(request, listing_id):
    if request.method=="POST":
        listing = Listing.objects.get(pk=listing_id)
        current_bid = int(listing.bid)
        # new_bid = int(request.POST["bid"])
        new_bid = int(request.POST.get('bid', False))

        if new_bid > current_bid:
            #create the new_bid and save it:
            new_bid_obj = Bid.create(request.user,new_bid,listing)     
            new_bid_obj.save() 
            #update listing class << bid field:
            # MyModel.objects.filter(pk=some_value).update(field1='some value')
            Listing.objects.filter(pk=listing_id).update(bid=new_bid)

            messages.success(request, 'Bid successfully added.')
            return HttpResponseRedirect(reverse("listing", args=(listing_id,)))
        else:
            messages.error(request, 'Your bid needs to be higher than the current bid.')
    return render(request, "auctions/listing.html",{
        "listing": listing,
    })


def categories(request):
        categories = Categories.objects.all()
        return render(request, "auctions/categories.html",{
            "categories": categories
        })

def category(request, category_id):
    category_obj = Categories.objects.get(pk=category_id)
    listings = Listing.objects.filter(category=category_obj)
    return render(request, "auctions/category.html",{
        "category": category_obj,
        "listings": listings
    })
     

@login_required()
def watchlist(request):

    user = request.user
    watchlist = user.watchlist.all() 

    return render(request, "auctions/watchlist.html", {
        "watchlist": watchlist
    })


@login_required()
def watchlist_add(request, listing_id):
    if request.method == 'POST':
        listing = Listing.objects.get(pk=int(listing_id))
        user = User.objects.get(pk=int(request.POST["user"]))
        user.watchlist.add(listing)
        messages.success(request, 'Listing successfully added to your Watchlist.')
        return HttpResponseRedirect(reverse("listing", args=(listing_id,)))
    else:
        return render(request, "auctions/watchlist.html")


@login_required()
def watchlist_remove(request, listing_id):
    if request.method == 'POST':
        listing = Listing.objects.get(pk=int(listing_id))
        user = User.objects.get(pk=int(request.POST["user"]))
        user.watchlist.remove(listing)
        messages.success(request, 'Listing successfully removed from your Watchlist.')
        return HttpResponseRedirect(reverse("listing", args=(listing_id,)))
    else:
        return render(request, "auctions/watchlist.html")
 
    
@login_required()
def comment(request, listing_id):
    if request.method == 'POST':
        form = NewCommentForm(request.POST)
        if form.is_valid():
            comment = form.cleaned_data["comment"]
            listing = Listing.objects.get(pk=listing_id)
            comment = Comment.objects.create(user=request.user,listing=listing,comment=comment)
            comment.save()
        
            messages.success(request, 'Comment successfully added.')
            return HttpResponseRedirect(reverse("listing", args=(listing_id,)))

        return render(request, "auctions/listing.html", {
            "comment_form": form,
            })        
    else:
        return render(request, "auctions/listing.html",{
            "comment_form": NewCommentForm(),
        })

@login_required()
def closeListing(request, listing_id):
    if request.method == 'POST':
        listing = Listing.objects.get(pk=listing_id)
        #get the user who created the listing
        user = listing.user
        #get the logged in user
        logged_in_user = request.user

        if user == logged_in_user:
            created_by_user = True
        else:
            created_by_user = False

        Listing.objects.filter(pk=listing_id).update(active=False)    
        messages.success(request, 'Auction successfully closed.')
        return HttpResponseRedirect(reverse("listing", args=(listing_id,)))

    else:
        return render(request, "auctions/listing.html")

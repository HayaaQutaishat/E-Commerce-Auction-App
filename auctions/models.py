from django.contrib.auth.models import AbstractUser
from django.db import models
# from auctions.views import category
# from pyexpat import model

class User(AbstractUser):
    pass

class Categories(models.Model):
    type = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.type}"

class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="users")
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.amount}"

    @classmethod
    def create(cls, user,amount):
        bid = cls(user=user,amount=amount)
        return bid

class Listing(models.Model):

    title = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
    bid = models.ForeignKey(Bid, on_delete=models.CASCADE, related_name="bids")
    image = models.URLField(max_length=1000, blank=True, null=True)
    category = models.ForeignKey(Categories, on_delete=models.CASCADE, blank=True, null=True)
    watchlist = models.ManyToManyField(User, blank=True, related_name="watchlist")


    def __str__(self):
        return f"{self.title}"
    

    @classmethod
    def create(cls, title, description, bid, image, category):
        listing = cls(title=title, description=description, bid=bid, image=image, category=category)
        return listing


class Comment(models.Model):
    comment = models.CharField(max_length=5000)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    time = models.DateTimeField(auto_now_add=True)

    @classmethod
    def create(cls, user, listing, comment):
        comment = cls(user=user, listing=listing, comment=comment)
        return comment

    def __str__(self):
        return f"{self.comment}"







 

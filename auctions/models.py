from django.contrib.auth.models import AbstractUser
from django.db import models
# from pyexpat import model


class User(AbstractUser):
    pass

class Categories(models.Model):
    type = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.type}"

class Listing(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
    bid = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.URLField(max_length=1000, blank=True, null=True)
    category = models.ForeignKey(Categories, on_delete=models.CASCADE, blank=True, null=True)
    watchlist = models.ManyToManyField(User, blank=True, related_name="watchlist")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")
    created_at = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)


    def __str__(self):
        return f"{self.title}"
    

    @classmethod
    def create(cls, title, description, bid, image, category, user):
        listing = cls(title=title, description=description, bid=bid, image=image, category=category, user=user)
        return listing

class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="users")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="listings")

    def __str__(self):
        return f"{self.amount}"

    @classmethod
    def create(cls, user,amount,listing):
        bid = cls(user=user,amount=amount,listing=listing)
        return bid

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







 

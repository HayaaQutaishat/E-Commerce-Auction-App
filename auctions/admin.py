from django.contrib import admin
from auctions.models import Bid, Listing, User, Comment
# Register your models here.
class ListingAdmin(admin.ModelAdmin):
    list_display= ("title", "description", "bid")


class BidAdmin(admin.ModelAdmin):
    list_display= ("listing", "user", "amount")

class CommentAdmin(admin.ModelAdmin):
    list_display= ("comment", "listing", "user")


admin.site.register(Bid, BidAdmin)
admin.site.register(Listing, ListingAdmin)
admin.site.register(User)
admin.site.register(Comment, CommentAdmin)







    

from django.contrib import admin
from auctions.models import Bid, Listing, User, Comment, Categories
# Register your models here.
class ListingAdmin(admin.ModelAdmin):
    list_display= ("title", "description", "bid")


# class BidAdmin(admin.ModelAdmin):
#     list_display= ("listing", "user", "amount")

class CommentAdmin(admin.ModelAdmin):
    list_display= ("comment", "listing", "user")


admin.site.register(Bid)
admin.site.register(Categories)
admin.site.register(Listing, ListingAdmin)
admin.site.register(User)
admin.site.register(Comment, CommentAdmin)







    

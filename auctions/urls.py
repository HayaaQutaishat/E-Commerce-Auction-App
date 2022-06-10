from django.urls import path
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("new_listing", views.new_listing, name="new_listing"),
    path("<int:listing_id>", views.listing, name="listing"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("place_bid/<int:listing_id>", views.place_bid, name="place_bid"),
    path("categories", views.categories, name="categories"),
    path("category/<int:category_id>", views.category, name="category"),
    path("<int:listing_id>/comment", views.comment, name="comment"),
    path("<int:listing_id>/watchlist_add", views.watchlist_add, name="watchlist_add"),
    path("<int:listing_id>/watchlist_remove", views.watchlist_remove, name="watchlist_remove"),
]

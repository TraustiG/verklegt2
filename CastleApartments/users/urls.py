from django.urls import path
from . import views

urlpatterns = [
    path("register/", views.register, name="register"),
    path("profile/", views.profile, name="profile"),
    path("seller/<int:id>", views.seller, name="profile"),
    path("filter/", views.saveFilter, name="filter"),
    path("my-properties/", views.my_properties, name="my-properties"),
    path("my-properties/<int:id>/offers", views.property_offers, name="seller_property_offers"),
]
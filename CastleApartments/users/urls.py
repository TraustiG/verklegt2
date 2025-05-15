from django.urls import path
from . import views

urlpatterns = [
    path("register/", views.register, name="register"),
    path("profile/", views.profile, name="profile"),
    path("seller/<int:id>", views.seller, name="seller-profile"),
    path("filters/", views.saveFilter, name="filter"),
    path("filters/<int:id>", views.editFilter, name="filter"),
    path("my-properties/", views.my_properties, name="my-properties"),
]
from django.urls import path

from . import views

urlpatterns  = [
    path("", views.index, name="real-estates"),
    path("real-estates/", views.createProperty, name="create-property"),
    path("real-estates/<int:id>", views.getRealEstateById, name="real-estate-by-id"),
    path("real-estates/<int:id>/images", views.imageGallery, name="image-gallery"),
    path("real-estates/<int:id>/offers/", views.createOffer, name="create-offer"),
    path("offers/<int:id>", views.deleteOffer, name="delete-offer"),
    path("search/", views.search, name="search"),
    path("fill-database/", views.databaseFiller, name="fill-database")
]
from django.urls import path

from . import views

urlpatterns  = [
    path("", views.index, name="real-estates"),
    path("real-estates/<int:id>", views.getRealEstateById, name="real-estate-by-id"),
    path("real-estates/<int:id>/image-gallery", views.imageGallery, name="image-gallery"),
]
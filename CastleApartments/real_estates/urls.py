from django.urls import path

from . import views

urlpatterns  = [
    path("", views.index, name="real-estates"),
    path("real-estates/<int:id>", views.getRealEstateById, name="real-estate-by-id"),
    path("real-estates/<int:id>/image-gallery", views.imageGallery, name="image-gallery"),
    path("search/", views.search, name="search"),
    path("real-estates/<int:id>/create-offer/", views.createOffer, name="create-offer"),
    path("create-property", views.createProperty, name="create-property"),
    path("edit-property/<int:id>/", views.editProperty, name="edit-property"),
    path("delete-property/<int:id>", views.deleteProperty, name="delete-property"),
    #path('profile/', views.profile_view, name='profile'),
    path('select-payment/<int:offer_id>/', views.selectPayment, name='selectPayment'),
]
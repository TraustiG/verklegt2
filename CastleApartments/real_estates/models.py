
from django.db import models
from babel.numbers import format_currency

class PropertyImages(models.Model):

    property = models.ForeignKey(
        "Property", on_delete=models.CASCADE)
    
    image_url = models.URLField()
    image_description = models.TextField()


    
    def __str__(self):
        return f"{self.image_url}"


class Property(models.Model):

    seller = models.ForeignKey(
        "users.Seller", on_delete=models.CASCADE, null=True, blank=True)
    
    street_name = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=5)
    description = models.TextField()
    property_type = models.CharField(max_length=100)
    listing_date = models.DateField()
    listing_price = models.CharField(max_length = 15)
    number_of_bedrooms = models.CharField(max_length=2)
    number_of_bathrooms = models.CharField(max_length=2)
    square_meters = models.CharField(max_length = 4)
    status = models.CharField(max_length = 100)
    image = models.URLField()

    def __str__(self):
        return f"{self.street_name}"
    

class OfferStatus(models.TextChoices):
        OPEN = 'OPEN', 'Open'
        REJECTED = 'REJECTED', 'Rejected'
        ACCEPTED = 'ACCEPTED', 'Accepted'
        CONTINGENT = 'CONTINGENT', 'Contingent'
        PROCESSED = 'PROCESSED', 'Processed'

class Offer(models.Model):

    property = models.ForeignKey(
        "Property", on_delete=models.CASCADE)
    
    buyer = models.ForeignKey(
        "users.Buyer", on_delete=models.CASCADE, null=True, blank=True)
    
    offer_amount = models.CharField(max_length=20)
    offer_expiry = models.DateField()
    offer_date = models.DateField(auto_now_add=True)

    offer_status = models.CharField(choices=OfferStatus.choices, default=OfferStatus.OPEN,)
    
    def __str__(self):
        return f"{self.offer_amount}"


    

class PaymentOption(models.TextChoices):
        CREDIT_CARD = "CREDIT_CARD", "Credit Card"
        BANK_ACCOUNT = "BANK_ACCOUNT", "Bank Account"
        MORTGAGE = "MORTGAGE", "Mortgage"

class Payment(models.Model):

    offer = models.OneToOneField(
         "Offer", on_delete=models.CASCADE)

    payment_option = models.CharField(max_length=16, choices=PaymentOption.choices)

    payment_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.offer} - {self.payment_option}"
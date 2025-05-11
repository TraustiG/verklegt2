from django.db import models

# Create your models here.

class PaymentOption(models.TextChoices):
        CREDIT_CARD = "CREDIT_CARD", "Credit Card"
        BANK_ACCOUNT = "BANK_ACCOUNT", "Bank Account"
        MORTGAGE = "MORTGAGE", "Mortgage"

class Payment(models.Model):

    offer = models.OneToOneField(
         "real_estates.Offer", on_delete=models.CASCADE)

    payment_option = models.CharField(max_length=16, choices=PaymentOption.choices)

    payment_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.offer} - {self.payment_option}"
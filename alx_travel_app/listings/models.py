from django.db import models
from django.contrib.auth.models import User
import uuid
from django.core.validators import MinValueValidator, MaxValueValidator


class Listing(models.Model):
    listing_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    host = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, null=False)
    description = models.TextField(null=False)
    location = models.CharField(max_length=100, null=False)
    price_per_night = models.DecimalField(decimal_places=2, max_digits=9, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)  # Changed to auto_now


class Booking(models.Model):
    PENDING = 'PENDING'
    CONFIRMED = 'CONFIRMED'
    CANCELLED = 'CANCELLED'
    
    BOOKING_STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (CONFIRMED, 'Confirmed'),
        (CANCELLED, 'Cancelled'),
    ]

    booking_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_date = models.DateField()  # Changed to DateField
    end_date = models.DateField()    # Changed to DateField
    total_price = models.DecimalField(decimal_places=2, max_digits=9, null=False)
    status = models.CharField(
        max_length=15,
        choices=BOOKING_STATUS_CHOICES,
        default=PENDING,
        null=False
    )
    created_at = models.DateTimeField(auto_now_add=True)


class Review(models.Model):
    review_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        null=False
    )
    comment = models.TextField(null=False)
    created_at = models.DateTimeField(auto_now_add=True)


class Payment(models.Model):
    PENDING = "PENDING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"

    PAYMENT_STATUS_CHOICES = [
        (PENDING, "Pending"),
        (COMPLETED, "Completed"),
        (FAILED, "Failed"),
    ]

    payment_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    booking = models.OneToOneField(
        Booking,
        on_delete=models.CASCADE,
        related_name="payment"
    )
    amount = models.DecimalField(max_digits=9, decimal_places=2)
    status = models.CharField(
        max_length=15,
        choices=PAYMENT_STATUS_CHOICES,
        default=PENDING,
        null=False
    )
    transaction_reference = models.CharField(max_length=100, unique=True)
    chapa_transaction_id = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Payment {self.payment_id} for Booking {self.booking.booking_id} - {self.status}"

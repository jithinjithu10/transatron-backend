from django.db import models

# List of predefined stops from Thrissur to Trivandrum
STOPS = [
    ("Thrissur", "Thrissur"),
    ("Irinjalakuda", "Irinjalakuda"),
    ("Chalakudy", "Chalakudy"),
    ("Angamaly", "Angamaly"),
    ("Aluva", "Aluva"),
    ("Ernakulam", "Ernakulam"),
    ("Tripunithura", "Tripunithura"),
    ("Piravom", "Piravom"),
    ("Ettumanoor", "Ettumanoor"),
    ("Kottayam", "Kottayam"),
    ("Changanassery", "Changanassery"),
    ("Thiruvalla", "Thiruvalla"),
    ("Kayamkulam", "Kayamkulam"),
    ("Kollam", "Kollam"),
    ("Trivandrum", "Trivandrum"),
]

class Bus(models.Model):
    number_plate = models.CharField(max_length=15, unique=True, default="KL-15-1234")
    total_seats = models.PositiveIntegerField(default=20)  # Assume 40 seats for the bus

    def __str__(self):
        return f"Bus {self.number_plate}"


class Seat(models.Model):
    seat_number = models.PositiveIntegerField()
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"Seat {self.seat_number}"
    
class SeatAllocation(models.Model):
    seat = models.ForeignKey(Seat, on_delete=models.CASCADE)
    start_stop = models.CharField(max_length=50, choices=STOPS)
    end_stop = models.CharField(max_length=50, choices=STOPS)
   

class Booking(models.Model):
    passenger_name = models.CharField(max_length=100)
    start_stop = models.CharField(max_length=50, choices=STOPS)
    end_stop = models.CharField(max_length=50, choices=STOPS)
    seat = models.ForeignKey(Seat, on_delete=models.CASCADE)
    booking_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Booking: {self.passenger_name} | Seat {self.seat.seat_number} | {self.start_stop} to {self.end_stop}"
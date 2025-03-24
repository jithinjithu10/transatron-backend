from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .seat_allocation import find_longest_available_segment
from .models import SeatAllocation, Seat

@csrf_exempt
def book_ticket_view(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            passenger_name = data.get("passenger_name")
            start = data.get("start")
            end = data.get("end")

            # Ensure required fields are provided
            if not passenger_name or not start or not end:
                return JsonResponse({"error": "Missing required fields"}, status=400)

            # Find the longest available segment
            segment = find_longest_available_segment(start, end)

            if not segment:
                return JsonResponse({"error": "No seats available for the selected route"}, status=400)

            seat = segment[2]  # Extract the seat object

            # Create the booking
            new_booking = SeatAllocation.objects.create(
                seat=seat,
                start_stop=start,
                end_stop=end
            )

            return JsonResponse({"message": f"Seat {seat.seat_number} booked from {start} to {end}"})

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

    return JsonResponse({"message": "Use POST to book a ticket"}, status=405)


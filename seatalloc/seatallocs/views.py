from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .seat_allocation import find_available_seat, find_longest_available_segment
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

            # Step 1: Try to book a full seat first
            full_seat = find_available_seat(start, end)

            if full_seat:
                SeatAllocation.objects.create(
                    seat=full_seat,
                    start_stop=start,
                    end_stop=end
                )
                return JsonResponse({
                    "message": f"Full ticket booked: Seat {full_seat.seat_number} from {start} to {end}"
                })

            # Step 2: If no full seat, find the longest available segment
            segment = find_longest_available_segment(start, end)

            if segment:
                partial_start = segment[0]
                partial_end = segment[1]
                seat = segment[2]  # Extract the allocated seat

                # Create the booking for the available segment
                SeatAllocation.objects.create(
                    seat=seat,
                    start_stop=partial_start,
                    end_stop=partial_end
                )

                return JsonResponse({
                    "message": f"Partial ticket booked: Seat {seat.seat_number} from {partial_start} to {partial_end}. "
                               f"Full journey ({start} to {end}) is not available."
                })

            # If no seats are available at all
            return JsonResponse({"error": "No seats available for the selected route"}, status=400)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

    return JsonResponse({"message": "Use POST to book a ticket"}, status=405)

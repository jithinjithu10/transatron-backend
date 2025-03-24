from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .seat_allocation import book_seat  # Import the centralized function

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

            # Call the central booking function
            booking_message = book_seat(passenger_name, start, end)

            return JsonResponse({"message": booking_message})

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

    return JsonResponse({"message": "Use POST to book a ticket"}, status=405)

from seatallocs.models import Seat, SeatAllocation, STOPS

# Function to get index of a stop
def get_stop_index(stop_name):
    """Returns the index of the stop from STOPS."""
    for i, stop in enumerate(STOPS):
        if stop[0] == stop_name:
            return i
    return None

# Function to check seat availability
def is_seat_available(seat, start, end):
    """Checks if a seat is available for the given start and end stops."""
    start_index = get_stop_index(start)
    end_index = get_stop_index(end)

    if start_index is None or end_index is None:
        return False  # Invalid stop

    bookings = SeatAllocation.objects.filter(seat=seat)
    for booking in bookings:
        booked_start_index = get_stop_index(booking.start_stop)
        booked_end_index = get_stop_index(booking.end_stop)

        # Overlap condition: If the new trip overlaps with existing booking
        if not (booked_end_index <= start_index or booked_start_index >= end_index):
            return False  # Seat is not available

    return True  # Seat is available

# Function to find an available seat
def find_available_seat(start, end):
    """Finds the first available seat for the given journey."""
    all_seats = Seat.objects.all().order_by("seat_number")

    for seat in all_seats:
        if is_seat_available(seat, start, end):
            return seat  # Return the available seat

    return None  # No available seat

# Function to find the longest available segment when a full ticket is unavailable
def find_longest_available_segment(start, end):
    """Finds the longest segment that can be booked while ensuring optimal seat utilization."""
    start_index = get_stop_index(start)
    end_index = get_stop_index(end)

    if start_index is None or end_index is None:
        return None  # Invalid stops

    longest_segment = None
    longest_length = 0

    # Forward search (towards the destination)
    for i in range(start_index + 1, end_index + 1):
        seat = find_available_seat(start, STOPS[i][0])
        if seat:
            segment_length = i - start_index
            if segment_length > longest_length:
                longest_length = segment_length
                longest_segment = (start, STOPS[i][0], seat)

    # Backward search (towards the origin)
    for i in range(end_index - 1, start_index - 1, -1):
        seat = find_available_seat(STOPS[i][0], end)
        if seat:
            segment_length = end_index - i
            if segment_length > longest_length:
                longest_length = segment_length
                longest_segment = (STOPS[i][0], end, seat)

    return longest_segment  # Returns (start, end, seat) if available

# Function to book a seat
def book_seat(passenger_name, start, end):
    """Books a seat for a passenger if available."""
    
    # Step 1: Try to book a full-ticket seat first
    full_seat = find_available_seat(start, end)
    
    if full_seat:
        SeatAllocation.objects.create(
            seat=full_seat,
            start_stop=start,
            end_stop=end
        )
        return f"Full ticket booked: Seat {full_seat.seat_number} from {start} to {end}"

    # Step 2: If no full ticket, book the longest available segment
    segment = find_longest_available_segment(start, end)

    if segment:
        partial_start = segment[0]
        partial_end = segment[1]
        seat = segment[2]  # Get the seat

        # Create booking
        SeatAllocation.objects.create(
            seat=seat,
            start_stop=partial_start,
            end_stop=partial_end
        )

        return f"Partial ticket booked: Seat {seat.seat_number} from {partial_start} to {partial_end}. Full journey ({start} to {end}) is not available."
    else:
        return "No seats available"

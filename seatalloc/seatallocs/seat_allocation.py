from seatallocs.models import Seat, SeatAllocation, STOPS

# Function 2: Find available seat
def find_available_seat(start, end):
    all_seats = Seat.objects.all()
    for seat in all_seats:
        bookings = SeatAllocation.objects.filter(seat=seat)
        is_available = True
        for booking in bookings:
            if not (booking.end_stop <= start or booking.start_stop >= end):
                is_available = False
                break
        if is_available:
            return seat
    return None  # No seat available

# Function 3: Find the longest available segment
def find_longest_available_segment(start, end):
    # Initialize start_index and end_index as None
    start_index = None
    end_index = None

    # Loop through STOPS to find start_index
    for i, stop in enumerate(STOPS):  # Loop through each stop with its index
        if stop[0] == start:  # Check if stop name matches the start stop
            start_index = i  # Store the index
            break  # Exit the loop once found

    # Loop through STOPS to find end_index
    for i, stop in enumerate(STOPS):  # Loop through each stop with its index
        if stop[0] == end:  # Check if stop name matches the end stop
            end_index = i  # Store the index
            break  # Exit the loop once found

    longest_segment = None
    longest_length = 0

    for i in range(start_index + 1, len(STOPS)):
        seat = find_available_seat(start, STOPS[i][0])
        if seat:
            segment_length = i - start_index
            if segment_length > longest_length:
                longest_length = segment_length
                longest_segment = (start, STOPS[i][0], seat)

    for i in range(end_index - 1, -1, -1):
        seat = find_available_seat(STOPS[i][0], end)
        if seat:
            segment_length = end_index - i
            if segment_length > longest_length:
                longest_length = segment_length
                longest_segment = (STOPS[i][0], end, seat)

    return longest_segment  # Returns (start, end, seat)

# Function 4: Book seat
def book_seat(passenger_name, start, end):
    segment = find_longest_available_segment(start, end)

    if segment:
        new_booking = SeatAllocation.objects.create(
            seat=segment[2], start_stop=segment[0], end_stop=segment[1]
        )
        return f"Seat {segment[2].seat_number} booked from {segment[0]} to {segment[1]}"
    else:
        return "No seats available"

from django.urls import path
from . import views  # Import your views

urlpatterns = [
    path("", views.book_ticket_view, name="book_ticket"),  # Maps `/seatallocs/` to `book_ticket_view`
]

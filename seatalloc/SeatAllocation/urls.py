from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("seatallocs/", include("seatallocs.urls")),  # Make sure this is included
]

from django.views.generic import ListView, DetailView
from django.shortcuts import render
from django_countries import countries
from . import models


# Create your views here.
class HomeView(ListView):
    model = models.Room
    paginate_by = 10
    paginate_orphans = 2
    ordering = "created"
    context_object_name = "rooms"


class RoomDetails(DetailView):
    model = models.Room


def search(request):
    city = request.GET.get("city", "Anywhere")
    city = str.capitalize(city)
    country = request.GET.get("country", "IN")
    room_type = int(request.GET.get("room_type", "0"))
    room_types = models.RoomType.objects.all()
    price = int(request.GET.get("price", 0))
    guests = int(request.GET.get("guests", 0))
    bedrooms = int(request.GET.get("bedrooms", 0))
    beds = int(request.GET.get("beds", 0))
    baths = int(request.GET.get("baths", 0))
    s_amenities = request.GET.getlist("amenities")
    s_facilities = request.GET.getlist("facilities")
    instant = request.GET.get("instant", False)
    super_host = request.GET.get("super_host", False)

    form = {
        "price": price,
        "guests": guests,
        "bedrooms": bedrooms,
        "beds": beds,
        "baths": baths,
        "s_amenities": s_amenities,
        "s_facilities": s_facilities,
        "instant": instant,
        "super_host": super_host,
    }

    amenities = models.Amenity.objects.all()
    facilities = models.Facility.objects.all()

    choices = {
        "amenities": amenities,
        "facilities": facilities,
    }

    return render(
        request,
        "rooms/search.html",
        {
            "city": city,
            "countries": countries,
            "room_types": room_types,
            "s_country": country,
            "s_room_type": room_type,
            **form,
            **choices,
        },
    )

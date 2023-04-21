import datetime
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import redirect, reverse
from rooms import models as room_models
from . import models


class CreateError(Exception):
    pass


@login_required
def create(request, room, year, month, day):
    try:
        date_obj = datetime.datetime(year, month, day)
        # room to create reservation for
        room = room_models.Room.objects.get(pk=room)
        # check if Already that day is booked or not
        models.BookedDay.objects.get(day=date_obj, reservation__room=room)
        # if day already booked raise exception and handle logic there
        raise CreateError()
    except (room_models.Room.DoesNotExist, CreateError):
        messages.error(request, "Can't Reserve That Room")
        return redirect(reverse("core:home"))
    except models.BookedDay.DoesNotExist:
        # create reservation if room is not booked for that particular day
        # reservation save method saves bookedDays object also.
        reservation = models.Reservation.objects.create(
            guest=request.user,
            room=room,
            check_in=date_obj,
            # current implementation only books for 1 day ,change later
            check_out=date_obj + datetime.timedelta(days=0),
        )
        return redirect(reverse("core:home"))

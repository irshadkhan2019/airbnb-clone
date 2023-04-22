import datetime
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import Http404
from django.views.generic import View
from django.shortcuts import redirect, reverse, render
from rooms import models as room_models
from reviews import forms as review_forms
from . import models


class CreateError(Exception):
    pass


# create reservation
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
        return redirect(reverse("reservations:detail", kwargs={"pk": reservation.pk}))


# view reservation
class ReservationDetailView(View):
    def get(self, *args, **kwargs):
        pk = kwargs.get("pk")
        reservation = models.Reservation.objects.get_or_none(pk=pk)
        if not reservation or (
            reservation.guest != self.request.user
            and reservation.room.host != self.request.user
        ):
            raise Http404()
        form = review_forms.CreateReviewForm()
        return render(
            self.request,
            "reservations/detail.html",
            {"reservation": reservation, "form": form},
        )


def edit_reservation(request, pk, verb):
    reservation = models.Reservation.objects.get_or_none(pk=pk)
    if not reservation or (
        reservation.guest != request.user and reservation.room.host != request.user
    ):
        raise Http404()
    if verb == "confirm":
        reservation.status = models.Reservation.STATUS_CONFIRMED
    elif verb == "cancel":
        reservation.status = models.Reservation.STATUS_CANCELED
        # remove room booked days since reservation got cancelled
        models.BookedDay.objects.filter(reservation=reservation).delete()
    reservation.save()
    messages.success(request, "Reservation Updated")
    return redirect(reverse("reservations:detail", kwargs={"pk": reservation.pk}))

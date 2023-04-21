import datetime
from django import template
from reservations import models as reservation_models

register = template.Library()


# checks if booking already exists for a given day
@register.simple_tag
def is_booked(room, day):
    if day.number == 0:
        return
    try:
        # create date object to compare
        date = datetime.datetime(year=day.year, month=day.month, day=day.number)
        reservation_models.BookedDay.objects.get(day=date, reservation__room=room)
        return True
    except reservation_models.BookedDay.DoesNotExist:
        return False

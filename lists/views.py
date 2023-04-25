from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, reverse
from django.views.generic import TemplateView
from rooms import models as room_models
from . import models


@login_required
def toggle_room(request, room_pk):
    action = request.GET.get("action", None)
    room = room_models.Room.objects.get_or_none(pk=room_pk)
    if room is not None and action is not None:
        the_list, _ = models.List.objects.get_or_create(
            user=request.user, name="My Favourites Houses"
        )
        # add in many to many field rooms via add()
        if action == "add":
            the_list.rooms.add(room)
        elif action == "remove":
            # remove from many to many field rooms via remove()
            the_list.rooms.remove(room)
    return redirect(reverse("rooms:detail", kwargs={"pk": room_pk}))

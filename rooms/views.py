from django.shortcuts import render,redirect
from django.urls import reverse
from django.views.generic import ListView
from django.http import Http404
from . import models


# Create your views here.
class HomeView(ListView):
    model=models.Room
    paginate_by=10
    paginate_orphans=2
    ordering="created"
    context_object_name="rooms"


def room_details(request,pk):
    try:
        room=models.Room.objects.get(pk=pk)
        return render(request,"rooms/detail.html",{"room":room}) 
    except models.Room.DoesNotExist:    
       raise Http404()

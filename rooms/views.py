from django.shortcuts import render
from django.views.generic import ListView
from . import models


# Create your views here.
class HomeView(ListView):
    model=models.Room
    paginate_by=10
    paginate_orphans=2
    ordering="created"
    context_object_name="rooms"


def room_details(request,pk):
    print(pk)
    return render(request,"rooms/detail.html") 

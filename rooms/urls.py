from django.urls import path
from . import views

app_name="rooms"

urlpatterns = [
    path("<int:pk>",views.room_details,name="detail")
]

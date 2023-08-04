from django.urls import path
from .views import order_details_view,create_trip,update_user_response,get_trip_info,update_user_location
from .views import trip_details_view,fleet_user_details,fleet_user_ids,assign_trip,get_assigned_trips
from .views import get_ongoing_trips
urlpatterns = [
    
    
    path('order_details_view/', order_details_view),
    path('create_trip/',create_trip),
    path('trip_details_view/',trip_details_view),
    path('fleet_user_details/',fleet_user_details),
    path('fleet_user_ids/',fleet_user_ids),
    path('assign_trip/',assign_trip),
    path('get_assigned_trips/',get_assigned_trips),
    path('update_user_response/',update_user_response),
    path('get_trip_info/',get_trip_info),
    path('update_user_location/',update_user_location),
    path('get_ongoing_trips/',get_ongoing_trips),
    

]
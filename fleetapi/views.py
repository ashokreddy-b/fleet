'''Importing the necessary libraries and
 the modes to connect with the database'''
from typing import ValuesView
from django.shortcuts import render
from django.http import JsonResponse
#from .models import FleetManagerData,OrderDetails
from django.core import serializers
from .models import OrderDetails,trip_details,fleet_users
from django.http import HttpResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
import datetime
import os
import json


# API for retrieving the order details where the order status is pending 
@csrf_exempt
def order_details_view(request):
    # Retrieve all records from the OrderDetails model where the status of orders is "pending"
    order_details = OrderDetails.objects.filter(order_status='pending').order_by('order_id')
    formatted_data = []
    # Iterate over the order_details queryset and format the data 
    for order in order_details: 
        order_data = { 
            'order_id': order.order_id,
            'pickup_location': order.pickup_location, 
            'drop_location': order.drop_location,
            'distance': order.distance,
            'order_type': order.order_type,
            'customer_name': order.customer_name,
            'customer_contact': order.customer_contact,
            'date_time': order.date_time,
            'remarks': order.remarks,
            'order_status': order.order_status
            }
        formatted_data.append(order_data) 
    # Return the formatted data as a JSON response return JsonResponse(formatted_data)  
    if len(formatted_data)>0:
        response_data = {
            'data': formatted_data,
            'message': 'Fetched data successfully',
            'status': 'SUCCESS'
         }
        return JsonResponse(response_data)
    elif len(formatted_data)==0:
        response_data = {
            'data': None,
            'message': 'Fetched data successfully',
            'status': 'SUCCESS'
         }
        return JsonResponse(response_data)



# API for inserting into the trip details table and also updating the status of the respective order_status to IN progess
@csrf_exempt
def create_trip(request):  
    if request.method == 'POST':       
        json_data = json.loads(request.body)  # Parse the JSON data

        order_id = json_data.get('order_id', None)
        if order_id:          
             # Check if trip_id already exists 
            if trip_details.objects.filter(order_id=order_id).exists():
                    response_data = {
                                'data': None,
                                'message': 'Trip already created for this order ID',
                                'status': 'FAIL'
                            }
                    return JsonResponse(response_data)
        else:
            response_data = {
                                'data': None,
                                'message': 'Invalid insertion without order ID',
                                'status': 'FAIL'
                            }
            return JsonResponse(response_data)
            
        if  json_data.get('trip_name', None):     
            trip_name = json_data.get('trip_name', None)     
        else:
            trip_name=None 
            
        if json_data.get('trip_name', None):
            trip_name = json_data.get('trip_name', None)
        else:
            user_id =None

        if  json_data.get('start_date', None):   
            trip_start_date = json_data.get('start_date', None)   
        else:
            trip_start_date =None

        if json_data.get('vehicle_type', None):    
            vehicle_type = json_data.get('vehicle_type', None)
        else:
            vehicle_type=None

        if json_data.get('delivery_type', None):    
            delivery_type = json_data.get('delivery_type', None)
        else:
            delivery_type=None

        if json_data.get('remarks', None):  
            remarks = json_data.get('remarks', None)
        else:
            remarks=None

        if json_data.get('user_id', None):    
            user_id = json_data.get('user_id', None)
        else:
            user_id=None
        
        image_model = trip_details(
            trip_id="TRIP"+order_id,
            trip_name=trip_name,
            order_id=order_id,
            user_id=user_id,
            trip_start_date=trip_start_date,
            #trip_start_time=trip_start_time,
            vehicle_type=vehicle_type,
            delivery_type=delivery_type,
            incident_image=None,
            remarks=None,
            trip_status="pending"
        )

        try: 
            image_model.save()   
            order = OrderDetails.objects.get(order_id=order_id)
            order.order_status = 'In progress'
            order.save() 
            return_trip_id="TRIP"+order_id   
            response_data = {
                'data': return_trip_id,
                'message': 'Trip Created Successfully',
                'status': 'SUCCESS'
            }
            return JsonResponse(response_data)
        except:
            response_data = {
                'data': None,
                'message': 'Error in trip creation',
                'status': 'FAIL'
              }
            return JsonResponse(response_data)

    else:
        response_data = {
                'data': None,
                'message': 'Invalid request method.',
                'status': 'FAIL'
              }
        return JsonResponse(response_data)

# API to return all the details of the trip along with additional values from orders table
def trip_details_view(request): 
    available_trip_details = trip_details.objects.order_by('order_id')
    formatted_data = []
    # Iterate over the order_details queryset and format the data 
    for trip in available_trip_details: 
        orders_table_data=OrderDetails.objects.get(order_id=trip.order_id)
        order_data = { 
                'trip_id': trip.trip_id,
                'trip_name' : trip.trip_name,
                'order_id' : trip.order_id,
                'user_id' : trip.user_id,
                'trip_start_date' :trip.trip_start_date,
                'trip_start_time':trip.trip_start_time,
                'vehicle_type' : trip.vehicle_type,
                'delivery_type' : trip.delivery_type,
                'incident_image' : trip.incident_image,
                'remarks': trip.remarks,
                'trip_status':trip.trip_status,
                'source':orders_table_data.pickup_location,
                'destination':orders_table_data.drop_location,
                'delivery_date':orders_table_data.date_time,
                'distance':orders_table_data.distance,
                'order_type':orders_table_data.order_type
            }
        formatted_data.append(order_data)

    # Return the formatted data as a JSON response return JsonResponse(formatted_data)   
    print(formatted_data)
    if len(formatted_data)>0:
        response_data = {
            'data': formatted_data,
            'message': 'Fetched available trips data successfully',
            'status': 'SUCCESS'
         }
        return JsonResponse(response_data)
    elif len(formatted_data)==0:
        response_data = {
            'data': None,
            'message': 'Fetched data successfully',
            'status': 'SUCCESS'
         }
        return JsonResponse(response_data)

#API to return the complete user details
def fleet_user_details(request):
    formatted_data = []
    # Query all users from the FleetUser model
    users =fleet_users.objects.all()
    for user in users:    
        user_data={
            'user_id' : user.user_id,
            'full_name' : user.full_name,
            'gender' : user.gender,
            'dob': user.dob,
            'contact_no' : user.contact_no,
            'email' : user.email,
            'profile_pic' :  user.profile_pic,
            'last_updated_location': user.last_updated_location,
            'last_updated_time':user.last_updated_time,
            'latitude':user.latitude,
            'longitude':user.longitude,
            'managerid':user.managerid,
            'licence_number':user.licence_number,
            'licence_expiry_date':user.licence_expiry_date,
            'vehicle_no':user.vehicle_no,
            'vehicle_type':user.vehicle_type,
            'rc_valid_till':user.rc_valid_till,
            'tax_valid_till':user.tax_valid_till,
            'insurance_valid_till':user.insurance_valid_till,
            'pollution_valid_till':user.pollution_valid_till,
            'documents':user.documents,
            'total_trips':user.total_trips,
            'user_status':user.user_status

           }
        formatted_data.append(user_data)  

    if len(formatted_data)>0:
        response_data = {
            'data': formatted_data,
            'message': 'Fetched available users data successfully',
            'status': 'SUCCESS'
         }
        return JsonResponse(response_data)
    elif len(formatted_data)==0:
        response_data = {
            'data': None,
            'message': 'No data avalable',
            'status': 'FAIL'
         }
        return JsonResponse(response_data)
 
    
# API for returning the fleet user names list
@csrf_exempt
def fleet_user_ids(request):
    formatted_data = []
    # Query all users from the FleetUser model
    users =fleet_users.objects.all()
    for user in users:     
        user_id=user.user_id
        formatted_data.append(user_id)          
            
    if len(formatted_data)>0:
        response_data = {
            'data': formatted_data,
            'message': 'Fetched available users data successfully',
            'status': 'SUCCESS'
         }
        return JsonResponse(response_data)
    elif len(formatted_data)==0:
        response_data = {
            'data': None,
            'message': 'NO data available',
            'status': 'FAIL'
         }
        return JsonResponse(response_data)


# API for updating the trip details tale on trip assignment
@csrf_exempt
def assign_trip(request): 
    
    if request.method == 'POST':    
        json_data = json.loads(request.body)  # Parse the JSON data
        if json_data.get('trip_id', None): 
            trip_id = json_data.get('trip_id', None)
            print(trip_id)
            try:
                trip_data=trip_details.objects.get(trip_id=trip_id)
            except:
                response_data = {
                                'data': None,
                                'message': 'Trip ID does not exist',
                                'status': 'FAIL'
                            }
                return JsonResponse(response_data)   

            if trip_data.trip_status=='Scheduled' : 
                response_data = {
                                'data': None,
                                'message': 'trip already assigned for the trip ID',
                                'status': 'FAIL'
                            }    
                return JsonResponse(response_data)       
        else:        
            response_data = {
                                'data': None,
                                'message': 'Invalid trip assigning without the trip ID',
                                'status': 'FAIL'
                            }
            return JsonResponse(response_data)
   
        if json_data.get('start_time', None): 
            start_time = json_data.get('start_time', None)           
        else:
            response_data = {
                                'data': None,
                                'message': 'Invalid trip assigning without the proper start time',
                                'status': 'FAIL'
                            }
            return JsonResponse(response_data)
  
        if json_data.get('user_id', None): 
            user_id = json_data.get('user_id', None)           
        else:
            response_data = {
                                'data': None,
                                'message': 'Invalid trip assigning without the user ID',
                                'status': 'FAIL'
                            }
            return JsonResponse(response_data)

        try: 
            trip_data.trip_start_time=start_time 
            trip_data.user_id=user_id 
            trip_data.trip_status='Scheduled'  
            trip_data.remarks='waiting for confirmation' 
            trip_data.save()
    
            response_data = {
                                'data': None,
                                'message': 'successfully assigned the order',
                                'status': 'SUCCESS'
                            }
            return JsonResponse(response_data)
            

        except:
            
            response_data = {
                                'data': None,
                                'message': 'error in assigning the order',
                                'status': 'FAIL'
                            }
            return JsonResponse(response_data)


# POST method API to get the assigned trip details for the given userID :
@csrf_exempt
def get_assigned_trips(request): 
    if request.method == 'POST':
        json_data = json.loads(request.body)  # Parse the JSON data

        if  json_data.get('user_id', None):   
            user_id = json_data.get('user_id', None)  
            available_trip_details=trip_details.objects.filter(user_id=user_id, remarks="waiting for confirmation")
            formatted_data = []
            # Iterate over the order_details queryset and format the data 
            for trip in available_trip_details: 
                orders_table_data=OrderDetails.objects.get(order_id=trip.order_id)
                order_data = { 
                        'trip_id': trip.trip_id,
                        'trip_name' : trip.trip_name,
                        'order_id' : trip.order_id,
                        'user_id' : trip.user_id,
                        'trip_start_date' :trip.trip_start_date,
                        'trip_start_time':trip.trip_start_time,
                        'vehicle_type' : trip.vehicle_type,
                        'delivery_type' : trip.delivery_type,
                        'incident_image' : trip.incident_image,
                        'remarks': trip.remarks,
                        'trip_status':trip.trip_status,
                        'source':orders_table_data.pickup_location,
                        'destination':orders_table_data.drop_location,
                        'delivery_date':orders_table_data.date_time,
                        'distance':orders_table_data.distance,
                        'order_type':orders_table_data.order_type
                    }
                formatted_data.append(order_data)
            if len(formatted_data)>0:
                response_data = {
                        'data': formatted_data,
                        'message': 'Fetched available users data successfully',
                        'status': 'SUCCESS'
                    }
                return JsonResponse(response_data)
            elif len(formatted_data)==0:
                response_data = {
                        'data': None,
                        'message': 'NO data available for given user ID',
                        'status': 'FAIL'
                    }
                return JsonResponse(response_data)

        else:
            response_data = {
                                'data': None,
                                'message': 'Invalid get trip request without the user ID',
                                'status': 'FAIL'
                            }
            return JsonResponse(response_data)


# API for updating the trip details  on users response of acceting/reecting the assigned trip 
@csrf_exempt
def update_user_response(request): 
    if request.method == 'POST':
        #need to add the logic here after discussion    
        json_data = json.loads(request.body)  # Parse the JSON data
        if  json_data.get('trip_id', None):
            trip_id = json_data.get('trip_id', None)
            user_id = json_data.get('user_id', None) 
            if json_data.get('user_response', None) :
                try:
                    user_response=json_data.get('user_response', None) 
                    trip_data=trip_details.objects.get(trip_id=trip_id,user_id=user_id)
                    trip_data.remarks=user_response
                    if user_response=="Accepted":
                        trip_data.trip_status='In Progress' 
                        user_data =fleet_users.objects.get(user_id=user_id)
                        user_data.user_status="Occupied"
                        user_data.save()

                    trip_data.save()
                    response_data = {
                                'data': None,
                                'message': 'Succesfully updated user response',
                                'status': 'SUCCESS'
                            }    
                    return JsonResponse(response_data) 

                except:
                    response_data = {
                                'data': None,
                                'message': 'error in updating the user response',
                                'status': 'FAIL'
                            }    
                    return JsonResponse(response_data) 

            else:
                response_data = {
                                'data': None,
                                'message': 'user reponse not given',
                                'status': 'FAIL'
                            }    
                return JsonResponse(response_data) 
         
        else:        
            response_data = {
                                'data': None,
                                'message': 'Invalid request without the trip ID',
                                'status': 'FAIL'
                            }
            return JsonResponse(response_data)


# API for getting the trip details 
@csrf_exempt
def get_trip_info(request): 
    
    if request.method == 'POST':
        json_data = json.loads(request.body)  # Parse the JSON data
        if json_data.get('trip_id', None):
            try:
                trip_id=json_data.get('trip_id', None)
                trip=trip_details.objects.get(trip_id=trip_id)
                formatted_data=[]

                orders_table_data=OrderDetails.objects.get(order_id=trip.order_id)
                order_data = { 
                        'trip_id': trip.trip_id,
                        'trip_name' : trip.trip_name,
                        'order_id' : trip.order_id,
                        'user_id' : trip.user_id,
                        'trip_start_date' :trip.trip_start_date,
                        'trip_start_time':trip.trip_start_time,
                        'vehicle_type' : trip.vehicle_type,
                        'delivery_type' : trip.delivery_type,
                        'incident_image' : trip.incident_image,
                        'remarks': trip.remarks,
                        'trip_status':trip.trip_status,
                        'source':orders_table_data.pickup_location,
                        'destination':orders_table_data.drop_location,
                        'delivery_date':orders_table_data.date_time,
                        'distance':orders_table_data.distance,
                        'order_type':orders_table_data.order_type
                    }
                formatted_data.append(order_data)
                response_data = {
                            'data': formatted_data,
                            'message': 'Succesfully fetched the trip details',
                            'status': 'SUCCESS'
                        }    
                return JsonResponse(response_data) 

            except:
                response_data = {
                            'data': None,
                            'message': 'error in fetching trip data',
                            'status': 'FAIL'
                        }    
                return JsonResponse(response_data) 
        else:
            response_data = {
                            'data': None,
                            'message': 'Invalid request withou a trip id',
                            'status': 'FAIL'
                        }    
            return JsonResponse(response_data) 

    else:
        response_data = {
                        'data': None,
                        'message': 'Invalid request type expecting a Post request',
                        'status': 'FAIL'
                    }    
        return JsonResponse(response_data) 

            

#API to update the current location of the user                
@csrf_exempt
def update_user_location(request): 
    if request.method == 'POST':   
        json_data = json.loads(request.body) 
        if  json_data.get('latitude') :
            latitude=json_data.get('latitude')
        else:
            response_data = {
                        'data': None,
                        'message': 'Invalid request expecting a Post request with latitude',
                        'status': 'FAIL'
                    }    
            return JsonResponse(response_data) 

        if  json_data.get('longitude') :
            longitude=json_data.get('longitude') 
        else:
            response_data = {
                        'data': None,
                        'message': 'Invalid request expecting a Post request with longitude',
                        'status': 'FAIL'
                    }    
            return JsonResponse(response_data) 
        
        if json_data.get('last_updated_location') :
            last_updated_location =json_data.get('last_updated_location') 
        else:
            response_data = {
                        'data': None,
                        'message': 'Invalid request expecting a Post request with last_updated_location',
                        'status': 'FAIL'
                    }    
            return JsonResponse(response_data) 

        if  json_data.get('last_updated_time') :
            last_updated_time=json_data.get('last_updated_time') 

        else:
            response_data = {
                        'data': None,
                        'message': 'Invalid request expecting a Post request with last_updated_location',
                        'status': 'FAIL'
                    }    
            return JsonResponse(response_data) 

        if  json_data.get('user_id') :
            user_id =json_data.get('user_id') 
        else:
            response_data = {
                        'data': None,
                        'message': 'Invalid request expecting a Post request with a valid user_id',
                        'status': 'FAIL'
                    }    
            return JsonResponse(response_data) 

        try:
            print("the values are")
            print("latitude",latitude,type(latitude))
            print("longitude",longitude,type(longitude))
           
            user_data =fleet_users.objects.get(user_id=user_id)
            user_data.latitude=latitude
            user_data.longitude=longitude
            print("after asssigning teh latitude and logitude")
            user_data.last_updated_location=last_updated_location
            print("after assigning teh last updated location",last_updated_location,type(last_updated_location))
            user_data.last_updated_time=last_updated_time
            print("after assignign the last upadted time",last_updated_time,type(last_updated_time))
            user_data.save()
            trip_data=trip_details.objects.get(user_id=user_id,trip_status="In Progress")
            trip_id=trip_data.trip_id
            response_data = {
                            'data': trip_id,
                            'message': 'succefully upadted latitude ,longitude',
                            'status': 'SUCCESS'
                        }    
            return JsonResponse(response_data) 

        except:
            response_data = {
                        'data': None,
                        'message': 'Error in updating the loaction for the user',
                        'status': 'FAIL'
                    }    
            return JsonResponse(response_data) 

    else:
        response_data = {
                        'data': None,
                        'message': 'Invalid request expecting a Post request with a valid user_id',
                        'status': 'FAIL'
                    }    
        return JsonResponse(response_data) 



#API to get the ongoing trips                
@csrf_exempt
def get_ongoing_trips(request):

    ongoing_trip_details=trip_details.objects.filter(trip_status="In Progress")
    formatted_data = []
    print("inside the get ongoing trips API")
    # Iterate over the order_details queryset and format the data 
    for trip in ongoing_trip_details: 
        user_table_data=fleet_users.objects.get(user_id=trip.user_id)
        orders_table_data=OrderDetails.objects.get(order_id=trip.order_id)
        trip_data = { 
                'trip_id': trip.trip_id,
                'trip_name' : trip.trip_name,
                'order_id' : trip.order_id,
                'user_id' : trip.user_id,
                'trip_start_date' :trip.trip_start_date,
                'trip_start_time':trip.trip_start_time,
                'vehicle_type' : trip.vehicle_type,
                'delivery_type' : trip.delivery_type,
                'incident_image' : trip.incident_image,
                'remarks': trip.remarks,
                'trip_status':trip.trip_status,
                'user_name':user_table_data.full_name,
                'vehicle_no':user_table_data.vehicle_no,
                'latitude':float(user_table_data.latitude),
                'longitude':float(user_table_data.longitude),
                'last_updated_location':user_table_data.last_updated_location,
                'last_updated_time':user_table_data.last_updated_time,   
                'source':orders_table_data.pickup_location,
                'destination':orders_table_data.drop_location,
                'delivery_date':orders_table_data.date_time,

            }
        print(user_table_data.latitude,type(user_table_data.latitude))
        formatted_data.append(trip_data)
    if len(formatted_data)>0:
        response_data = {
                'data': formatted_data,
                'message': 'Fetched available users data successfully',
                'status': 'SUCCESS'                                                                                                                                                             
            }
        return JsonResponse(response_data)
    elif len(formatted_data)==0:
        response_data = {
                'data': None,
                'message': 'NO data available for given user ID',
                'status': 'FAIL'
            }
        return JsonResponse(response_data)


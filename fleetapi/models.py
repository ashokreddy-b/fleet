from django.db import models
from django.contrib.postgres.fields import ArrayField

class FleetManagerData(models.Model):
    manager_id = models.CharField(max_length=15, primary_key=True)
    manager_name = models.CharField(max_length=20)
    dob = models.DateField()
    contact_no = models.TextField()
    email = models.CharField(max_length=20)
    organisation= models.CharField(max_length=20)
    class Meta:
        db_table = 'fleet_manager_data'
        managed = False

class OrderDetails(models.Model):
    order_id = models.CharField(max_length=10, primary_key=True)
    pickup_location = models.CharField(max_length=25)
    drop_location = models.CharField(max_length=25)
    distance = models.DecimalField(max_digits=10, decimal_places=2)
    order_type = models.CharField()
    customer_name= models.CharField(max_length=25)
    customer_contact = models.TextField()
    date_time = models.DateTimeField()
    remarks = models.TextField()
    order_status= models.TextField()
    class Meta:
        db_table = 'order_details'
        
class trip_details(models.Model):
    trip_id = models.CharField(max_length=10, primary_key=True)
    trip_name = models.CharField(max_length=25)
    order_id = models.CharField(max_length=10)
    user_id = models.CharField(max_length=10)
    trip_start_date = models.DateField()
    trip_start_time= models.TimeField()
    vehicle_type = models.TextField()
    delivery_type = models.TextField()
    incident_image =  models.BinaryField()
    remarks= models.TextField()
    trip_status=models.CharField(max_length=15)
    class Meta:
        db_table = 'trip_details'

class fleet_users(models.Model):
    user_id = models.CharField(max_length=10, primary_key=True)
    full_name = models.CharField(max_length=30)
    gender = models.CharField(max_length=10)
    dob= models.DateField()
    contact_no = models.IntegerField()
    email = models.CharField(max_length=25)
    profile_pic =  models.BinaryField()
    last_updated_location=models.CharField()
    latitude= models.DecimalField(max_digits=6, decimal_places=4)
    longitude= models.DecimalField(max_digits=6, decimal_places=4)
    #last_updated_time=models.TimeField()
    last_updated_time= models.DateTimeField()
    managerid=models.CharField(max_length=10)
    licence_number=models.CharField(max_length=10)
    licence_expiry_date=models.DateField()
    vehicle_no=models.CharField(max_length=10)
    vehicle_type=models.CharField(max_length=20)
    rc_valid_till=models.DateField()
    tax_valid_till=models.DateField()
    insurance_valid_till=models.DateField()
    pollution_valid_till=models.DateField()
    documents=ArrayField(models.BinaryField())
    total_trips=models.IntegerField()
    user_status=models.CharField(max_length=15)
    class Meta:
        db_table = 'fleet_users' 
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone



class ClientManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)

class DispatcherManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='%(class)s_groups',  # Уникальное имя для обратной связи
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='%(class)s_permissions',  # Уникальное имя для обратной связи
        blank=True,
    )


class Client(CustomUser):

    CLIENT_TYPE_CHOICES = [
        ('physical', 'Physical'),
        ('legal', 'Legal'),
    ]

    name = models.CharField(max_length=50)
    phone = models.CharField(max_length=20)
    email = models.EmailField(max_length=50, unique=True)
    type = models.CharField(max_length=10, choices=CLIENT_TYPE_CHOICES)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = ClientManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'phone', 'type']
    

    def __str__(self):
        return self.client_name

    class Meta:
        verbose_name = 'Client'
        verbose_name_plural = 'Clients'


class Dispatcher(CustomUser):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = DispatcherManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Dispatcher'
        verbose_name_plural = 'Dispatchers'


class City(models.Model):
    city_name = models.CharField(max_length=50)
    latitude = models.DecimalField(max_digits=10, decimal_places=8)
    longitude = models.DecimalField(max_digits=11, decimal_places=8)

    def __str__(self):
        return self.city_name


class CityConnection(models.Model):
    city1 = models.ForeignKey(City, related_name='city1_connections', on_delete=models.CASCADE)
    city2 = models.ForeignKey(City, related_name='city2_connections', on_delete=models.CASCADE)
    distance = models.IntegerField()

    class Meta:
        unique_together = ('city1', 'city2')

    def __str__(self):
        return f"{self.city1} - {self.city2} ({self.distance} km)"


class Vehicle(models.Model):
    load_capacity = models.IntegerField()
    vehicle_type = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.vehicle_type} ({self.load_capacity} kg)"
    
class Driver(models.Model):
    LICENSE_CATEGORIES = [
        ('C', 'Category C'),
        ('D', 'Category D'),
        ('E', 'Category E'),
    ]
    
    name = models.CharField(max_length=50)
    license_category = models.CharField(max_length=1, choices=LICENSE_CATEGORIES)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name


class Shipment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_transit', 'In Transit'),
        ('delivered', 'Delivered'),
        ('rejected', 'Rejected'),
    ]

    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    pickup_city = models.ForeignKey(City, related_name='pickup_shipments', on_delete=models.SET_NULL, null=True)
    delivery_city = models.ForeignKey(City, related_name='delivery_shipments', on_delete=models.SET_NULL, null=True)
    pickup_location = models.CharField(max_length=100)
    delivery_location = models.CharField(max_length=100)
    distance = models.IntegerField()
    cargo_type = models.CharField(max_length=20)
    shipment_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    planned_delivery = models.DateTimeField(default=timezone.now)
    dispatcher = models.ForeignKey(Dispatcher, on_delete=models.CASCADE)
    city_connection = models.ForeignKey(CityConnection, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"Shipment {self.id} - {self.client}"


class ShipmentReview(models.Model):
    shipment = models.ForeignKey(Shipment, on_delete=models.CASCADE)
    val = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    contents = models.CharField(max_length=100)
    review_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Review {self.id} for Shipment {self.shipment.id}"


class ShipmentStatusHistory(models.Model):
    shipment = models.ForeignKey(Shipment, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=Shipment.STATUS_CHOICES)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Status {self.status} at {self.timestamp} for Shipment {self.shipment.id}"

from django.db import models
from django.contrib.auth.models import User


class Agencys(models.Model):
    name = models.CharField(max_length=30, default="TravelerHub")
    owner = models.CharField(max_length=20)
    location = models.CharField(max_length=50)
    state = models.CharField(max_length=50, default="Kerala")
    country = models.CharField(max_length=50, default="india")

    def __str__(self):
        return self.location

class Packages(models.Model):
        PACKAGE_STATUS = (
            ("1", "available"),
            ("2", "not available"),
        )

        PACKAGE_TYPE = (
            ("1", "Diamond"),
            ("2", "Gold"),
            ("3", "Silver"),
        )

        package_type = models.CharField(max_length=50, choices=PACKAGE_TYPE)
        capacity = models.IntegerField()
        price = models.IntegerField()
        agency = models.ForeignKey(Agencys, on_delete=models.CASCADE)
        status = models.CharField(choices=PACKAGE_STATUS, max_length=15)
        packagenumber = models.IntegerField()

        def __str__(self):
            return self.agency.name

class Reservation(models.Model):
        check_in = models.DateField(auto_now=False)
        check_out = models.DateField(auto_now=False)
        package = models.ForeignKey(Packages, on_delete=models.CASCADE)
        guest = models.ForeignKey(User, on_delete=models.CASCADE)

        booking_id = models.CharField(max_length=100, default="null")

        def __str__(self):
            return self.guest.username

class StaffProfiles(models.Model):
        username = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
        AgencyName = models.CharField(max_length=50, blank=True)
        Ownername = models.CharField(max_length=50, blank=True)
        Mobilenumber = models.CharField(max_length=50, blank=True)
        AddressLine1 = models.CharField(max_length=50, blank=True)
        AddressLine2 = models.CharField(max_length=50, blank=True)
        Postcode = models.CharField(max_length=50, blank=True)
        State = models.CharField(max_length=250, blank=True)
        Area = models.CharField(max_length=50, blank=True)
        email = models.EmailField(max_length=254, blank=True, null=True)
        LicenceNumber = models.CharField(max_length=50, blank=True, primary_key=True)
        RegistrationDocument = models.ImageField()

        def __str__(self):
            return str(self.username)



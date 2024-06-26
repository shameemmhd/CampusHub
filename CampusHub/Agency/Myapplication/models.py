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


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    college_id = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(max_length=20, blank=True, null=True)
    id_file = models.FileField(upload_to='id_files/', blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True) 
    department = models.CharField(max_length=100, blank=True, null=True)  

    def __str__(self):
        return self.user.username

class Calendar(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    def __str__(self):
        return self.title
    
class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    isbn = models.CharField(max_length=13, unique=True)

    def __str__(self):
        return self.title

class BookPost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    description = models.TextField()
    posted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.book.title} by {self.user.username}"

class ExchangeRequest(models.Model):
    from_user = models.ForeignKey(User, related_name='sent_requests', on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name='received_requests', on_delete=models.CASCADE)
    book_post = models.ForeignKey(BookPost, on_delete=models.CASCADE)
    message = models.TextField()
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('approved', 'Approved'), ('declined', 'Declined')], default='pending')
    requested_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.from_user.username} -> {self.to_user.username} ({self.book_post.book.title})"
    
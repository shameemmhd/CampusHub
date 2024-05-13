from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .models import Agencys, Packages, Reservation, StaffProfiles
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
import datetime



def homepage(request):
    all_location = Agencys.objects.values_list('location', 'id').distinct().order_by()  
    packages = Packages.objects.all()
    
    data = {'packages': packages, 'all_location': all_location}
    response = render(request, 'index.html', data)
    
    return HttpResponse(response)



def aboutpage(request):
    return HttpResponse(render(request, 'about.html'))



def contactpage(request):
    return HttpResponse(render(request, 'contact.html'))



def user_sign_up(request):
    if request.method == "POST":
        user_name = request.POST['username']

        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 != password2:
            messages.warning(request, "Password didn't matched")
            return redirect('userloginpage')

        try:
            if User.objects.all().get(username=user_name):
                messages.warning(request, "Username Not Available")
                return redirect('userloginpage')
        except:
            pass

        new_user = User.objects.create_user(username=user_name, password=password1)
        new_user.is_superuser = False
        new_user.is_staff = False
        new_user.save()
        messages.success(request, "Registration Successfull")
        return redirect("userloginpage")
    return HttpResponse('Access Denied')


# staff sign up
def staff_sign_up(request):
    if request.method == "POST":
        user_name = request.POST['username']

        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 != password2:
            messages.success(request, "Password didn't Matched")
            return redirect('staffloginpage')
        try:
            if User.objects.all().get(username=user_name):
                messages.warning(request, "Username Already Exist")
                return redirect("staffloginpage")
        except:
            pass

        new_user = User.objects.create_user(username=user_name, password=password1)
        new_user.is_superuser = False
        new_user.is_staff = True
        new_user.save()
        messages.success(request, " Staff Registration Successfull")
        return redirect("staffloginpage")
    else:

        return HttpResponse('Access Denied')


# user login and signup page
def user_log_sign_page(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['pswd']

        user = authenticate(username=email, password=password)
        try:
            if user.is_staff:
                messages.error(request, "Incorrect username or Password")
                return redirect('staffloginpage')
        except:
            pass

        if user is not None:
            login(request, user)
            messages.success(request, "successful logged in")
            print("Login successfull")
            return redirect('homepage')
        else:
            messages.warning(request, "Incorrect username or password")
            return redirect('userloginpage')

    response = render(request, 'user/userlogsign.html')
    return HttpResponse(response)


# logout for admin and user
def logoutuser(request):
    if request.method == 'GET':
        logout(request)
        messages.success(request, "Logged out successfully")
        print("Logged out successfully")
        return redirect('homepage')
    else:
        print("logout unsuccessfull")
        return redirect('userloginpage')


# staff login and signup page
def staff_log_sign_page(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user.is_staff:
            login(request, user)
            return redirect('staffpanel')

        else:
            messages.success(request, "Incorrect username or password")
            return redirect('staffloginpage')
    response = render(request, 'staff/stafflogsign.html')
    return HttpResponse(response)

@login_required(login_url='/staff')
def panel(request):
    if request.user.is_staff == False:
        return HttpResponse('Access Denied')

    packages = Packages.objects.all()
    total_packages = len(packages)
    available_packages = len(Packages.objects.all().filter(status='1'))
    unavailable_packages = len(Packages.objects.all().filter(status='2'))
    reserved = len(Reservation.objects.all())

    agency = Agencys.objects.values_list('location', 'id').distinct().order_by()

    response = render(request, 'staff/panel.html',
                      {'location': agency, 'reserved': reserved, 'packages': packages, 'total_packages': total_packages,
                       'available': available_packages, 'unavailable': unavailable_packages})
    return HttpResponse(response)


# for editing package information
@login_required(login_url='/staff')
def edit_package(request):
    if request.user.is_staff == False:
        return HttpResponse('Access Denied')
    if request.method == 'POST' and request.user.is_staff:
        print(request.POST)
        old_package = Packages.objects.all().get(id=int(request.POST['packageid']))
        agency = Agencys.objects.all().get(id=int(request.POST['agency']))
        old_package.package_type = request.POST['packagetype']
        old_package.capacity = int(request.POST['capacity'])
        old_package.price = int(request.POST['price'])
        old_package.size = int(request.POST['size'])
        old_package.agency = agency
        old_package.status = request.POST['status']
        old_package.package_number = int(request.POST['packagenumber'])

        old_package.save()
        messages.success(request, "Package Details Updated Successfully")
        return redirect('staffpanel')
    else:

        package_id = request.GET['packageid']
        package = Packages.objects.all().get(id=package_id)
        response = render(request, 'staff/editpackage.html', {'package': package})
        return HttpResponse(response)
#for deleting package
@login_required(login_url='/staff')
def delete_package(request):
    if request.user.is_staff == False:
        return HttpResponse('Access Denied')

    if request.method == 'GET' and 'packageid' in request.GET:
        package_id = request.GET['packageid']
        try:
            package = Packages.objects.get(id=package_id)
            package.delete()
            messages.success(request, "Package Deleted Successfully")
        except Packages.DoesNotExist:
            messages.error(request, "Package does not exist")
        return redirect('staffpanel')
    else:
        return HttpResponse("Invalid request")


# for adding package
@login_required(login_url='/staff')
def add_new_package(request):
    if request.user.is_staff == False:
        return HttpResponse('Access Denied')
    if request.method == "POST":
        total_package = len(Packages.objects.all())
        new_package = Packages()
        agency = Agencys.objects.all().get(id=int(request.POST['agency']))
        print(f"id={agency.id}")
        print(f"name={agency.name}")

        new_package.packagenumber = total_package + 1
        new_package.package_type = request.POST['packagetype']
        new_package.capacity = int(request.POST['capacity'])
        new_package.size = int(request.POST['size'])
        new_package.capacity = int(request.POST['capacity'])
        new_package.agency = agency
        new_package.status = request.POST['status']
        new_package.price = request.POST['price']

        new_package.save()
        messages.success(request, "New Package Added Successfully")

    return redirect('staffpanel')


# booking package page
@login_required(login_url='/user')
def book_package_page(request):
    package = Packages.objects.all().get(id=int(request.GET['packageid']))
    return HttpResponse(render(request, 'user/bookpackage.html', {'package': package}))


# For booking the package
@login_required(login_url='/user')
def book_package(request):
    if request.method == "POST":
        package_id = request.POST['package_id']

        # Fetch package
        package = Packages.objects.get(id=package_id)

        # Check if the user has already applied for this event
        if Reservation.objects.filter(package=package, guest=request.user).exists():
            messages.warning(request, "You have already applied for this event.")
            return redirect("homepage")

        current_user = request.user
        total_person = int(request.POST['person'])
        booking_id = str(package_id) + str(datetime.datetime.now())


        reservation = Reservation()

        # Update package status
        package.status = '2'
        package.save()

        # Fetch user
        user_object = User.objects.get(username=current_user)

        # Save reservation
        reservation.guest = user_object
        reservation.package = package
        reservation.person = total_person
        reservation.check_in = request.POST['check_in']
        reservation.check_out = request.POST['check_out']
        reservation.save()

        messages.success(request, "Congratulations! Booking Successful")

        return redirect("homepage")
    else:
        return HttpResponse('Access Denied')

@login_required(login_url='/staff')
def view_package(request):
    package_id = request.GET['packageid']
    package = Packages.objects.all().get(id=package_id)

    reservation = Reservation.objects.all().filter(package=package)
    return HttpResponse(render(request, 'staff/viewpackage.html', {'package': package, 'reservations': reservation}))


@login_required(login_url='/user')
def user_bookings(request):
    if request.user.is_authenticated == False:
        return redirect('userloginpage')
    user = User.objects.all().get(id=request.user.id)
    print(f"request user id ={request.user.id}")
    bookings = Reservation.objects.all().filter(guest=user)
    if not bookings:
        messages.warning(request, "No Bookings Found")
    return HttpResponse(render(request, 'user/mybookings.html', {'bookings': bookings}))


@login_required(login_url='/staff')
def add_new_location(request):
    if request.method == "POST" and request.user.is_staff:
        owner = request.POST['new_owner']
        location = request.POST['new_city']
        state = request.POST['new_state']
        country = request.POST['new_country']

        agency = Agencys.objects.all().filter(location=location, state=state)
        if agency:
            messages.warning(request, "Sorry City at this Location already exist")
            return redirect("staffpanel")
        else:
            new_agency = Agencys()
            new_agency.owner = owner
            new_agency.location = location
            new_agency.state = state
            new_agency.country = country
            new_agency.save()
            messages.success(request, "New Location Has been Added Successfully")
            return redirect("staffpanel")

    else:
        return HttpResponse("Not Allowed")


# for showing all bookings to staff
@login_required(login_url='/staff')
def all_bookings(request):
    bookings = Reservation.objects.all()
    if not bookings:
        messages.warning(request, "No Bookings Found")
    return HttpResponse(render(request, 'staff/allbookings.html', {'bookings': bookings}))

@login_required(login_url='/staff')
def delete_agency(request):
    if request.method == 'GET':
        agency_id = request.GET.get('agencyid')
        if agency_id:
            try:
                agency = Agencys.objects.get(id=agency_id)
                agency.delete()
                messages.success(request, "Event Deleted Successfully")
            except Agencys.DoesNotExist:
                messages.error(request, "Event does not exist")
    return redirect('staffpanel')  
from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth.models import auth
from dashboard.models import User, Citizen
from datetime import datetime
from .models import *
from django.core.files.storage import FileSystemStorage
from tensorflow import keras
from keras.models import load_model
from PIL import Image
import numpy as np
from django.core.files.uploadedfile import InMemoryUploadedFile, TemporaryUploadedFile
from io import BytesIO


def register(request):
    if request.method == 'POST':
        f_name = request.POST['fname']
        l_name = request.POST['lname']
        email = request.POST['email']
        phone = request.POST['phone']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        
        if password == confirm_password:
            user = User.objects.create_user(first_name=f_name, last_name = l_name, email = email, password=password, user_type = 3)
            user.save()
            citizen = Citizen(user = user, mobile_no = phone)
            citizen.save()
            messages.success(request, "Account Created, You can Login Now")
            return render(request, 'dashboard/login.html')
        else:
            messages.error(request, "Password does not match")
            return render(request, 'dashboard/register.html')
    else:
        return render(request, 'dashboard/register.html')
    
    
def login(request):
    if request.method=='POST':
        email = request.POST['email']
        password = request.POST['password']
        user=authenticate(request, email=email,password=password)
        if user is not None:
            auth.login(request,user)
            if user.user_type == 3:
                return render(request, 'dashboard/citizen/dashboard.html')
            elif user.user_type == 2:
                complaints = Complaint.objects.filter(status = 1)
                return render(request, 'dashboard/driver/driverdashboard.html',{'complaints':complaints})
            elif user.user_type == 1:
                complaints = Complaint.objects.all()
                return render(request, 'dashboard/administrator/admindashboard.html',{'complaints':complaints})
            else:
                messages.error(request, "Create account before login")
                return render (request, 'dashboard/login.html')
        else:
            messages.error(request, "Something went Wrong, check email and password or create account")
            return render (request, 'dashboard/login.html')
    else:
        return render (request, 'dashboard/login.html')


def admin_register(request):
    if request.method == 'POST':
        f_name = request.POST['fname']
        l_name = request.POST['lname']
        email = request.POST['email']
        phone = request.POST['phone']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        
        if password == confirm_password:
            user = User.objects.create_user(first_name=f_name, last_name = l_name, email = email, password=password, user_type = 1)
            user.save()
            citizen = Administrator(user = user, mobile_no = phone)
            citizen.save()
            messages.success(request, "Account Created, You can Login Now")
            return render(request, 'dashboard/login.html')
        else:
            messages.error(request, "Password does not match")
            return render(request, 'dashboard/administrator/adminregister.html')
    else:
        return render(request, 'dashboard/administrator/adminregister.html')



#--------------Admin-------------------

def adminhome(request):
    if request.user.is_authenticated and request.user.user_type == 1:
        complaints = Complaint.objects.all()
        return render(request, 'dashboard/administrator/admindashboard.html',{'complaints':complaints})
    else:
        return render (request, 'dashboard/login.html')

def profile(request):
    if request.user.is_authenticated and request.user.user_type == 1:
        user = request.user
        return render(request, 'dashboard/administrator/profile.html',{'user':user})
    else:
        return render (request, 'dashboard/login.html')
    
def driverreg(request):
    if request.user.is_authenticated and request.user.user_type == 1:
        drivers = Driver.objects.all()
        return render(request, 'dashboard/administrator/driver.html',{'drivers':drivers})
    else:
        return render (request, 'dashboard/login.html')
    
def registerdriver(request):
    if request.method == 'POST':
        f_name = request.POST['fname']
        l_name = request.POST['lname']
        email = request.POST['email']
        phone = request.POST['phone']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        
        if password == confirm_password:
            user = User.objects.create_user(first_name=f_name, last_name = l_name, email = email, password=password, user_type = 2)
            user.save()
            citizen = Driver(user = user, mobile_no = phone)
            citizen.save()
            messages.success(request, "Account Created, You can Login Now")
            return render(request, 'dashboard/login.html')
        else:
            messages.error(request, "Password does not match")
            return render(request, 'dashboard/administrator/driverregistration.html')
    else:
        return render(request, 'dashboard/administrator/driverregistration.html')

    
#--------------Citizen-------------------

def citizen_dashboard(request):
    if request.user.is_authenticated and request.user.user_type == 3:
        complaints = Complaint.objects.filter(user = request.user)
        return render(request, 'dashboard/citizen/dashboard.html',{'complaints':complaints})
    else:
        return render (request, 'dashboard/login.html')
    
def citizenprofile(request):
    if request.user.is_authenticated and request.user.user_type == 3:
        user = request.user
        return render(request, 'dashboard/citizen/profile.html',{'user':user})
    else:
        return render (request, 'dashboard/login.html')
    
def detect_garbage(photo_path):
    # Load the trained model
    model_path = 'E:/Projects/Python/Django Projects/CitiWaste/citiwaste/dashboard/ml_model/citiwaste_model.keras'
    model = load_model(model_path)

    # Process the photo for inference
    img = Image.open(photo_path).convert('L').resize((100, 100))
    img_array = np.array(img).reshape((1, 100, 100, 1)) / 255.0

    # Perform inference
    prediction = model.predict(img_array)
    print("Prediction:", prediction)

    # Check if the image is classified as garbage
    is_garbage = prediction < 0.5

    return bool(is_garbage)

def complaint(request):
    if request.method == 'POST':
        user = request.user
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')
        photo = request.FILES.get('photo')
        description = request.POST.get('description')
        current_datetime = datetime.now()

        # Save the image using FileSystemStorage
        fs = FileSystemStorage()
        filename = fs.save(photo.name, photo)
        photo_path = fs.url(filename)

        # Check if the uploaded photo is garbage using your trained model
        is_garbage = detect_garbage(fs.path(filename))
        print('Garbage:', is_garbage)

        if is_garbage:
            # Save the complaint
            complaint = Complaint(user=user, latitude=latitude, longitude=longitude, photo=filename, description=description, status=1, datetime=current_datetime)
            complaint.save()

            messages.success(request, "Complaint registered successfully")
            return render(request, 'dashboard/citizen/complaint.html')
        else:
            # Delete the photo from the file system
            fs.delete(filename)

            messages.error(request, "This doesn't seem to be an image of garbage. Please upload a valid image.")
            return render(request, 'dashboard/citizen/complaint.html')
    else:
        return render(request, 'dashboard/citizen/complaint.html')





#--------------Driver-------------------
def driverhome(request):
    if request.user.is_authenticated and request.user.user_type == 2:
        complaints = Complaint.objects.filter(status = 1)
        return render(request, 'dashboard/driver/driverdashboard.html',{'complaints':complaints})
    else:
        return render (request, 'dashboard/login.html')
    
def completedcomplaints(request):
    if request.user.is_authenticated and request.user.user_type == 2:
        complaints = Complaint.objects.filter(status = 2)
        return render(request, 'dashboard/driver/completedcomplaints.html',{'complaints':complaints})
    else:
        return render (request, 'dashboard/login.html')
    
def driverprofile(request):
    if request.user.is_authenticated and request.user.user_type == 2:
        user = request.user
        return render(request, 'dashboard/driver/profile.html',{'user':user})
    else:
        return render (request, 'dashboard/login.html')
    
def change_status(request, complaint_id):
    if request.user.is_authenticated and request.user.user_type == 2:
        complaint = get_object_or_404(Complaint, pk=complaint_id)
        complaint.status = 2  # Set status to 'completed'
        complaint.save()
        complaints = Complaint.objects.filter(status = 1)
        return render(request, 'dashboard/driver/driverdashboard.html',{'complaints':complaints})

def mapview(request, complaint_id):
    complaint = get_object_or_404(Complaint, id=complaint_id)
    context = {
        'complaint': complaint
    }
    return render(request, 'dashboard/driver/mapview.html', context)






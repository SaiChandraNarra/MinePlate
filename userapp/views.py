from django.shortcuts import render,redirect
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login
from adminapp.models import *
import os
import easyocr
import torch
from django.core.files.storage import default_storage
from userapp.models import *



# Create your views here.


def user_admin(req):
    admin_email= "admin@gmail.com"
    admin_password="admin"
    if req.method=="POST":
        admin_e=req.POST.get("admin_email")
        admin_p=req.POST.get("admin_password")
        if (admin_e==admin_email and admin_p==admin_password):
            messages.success(req,'login successfull')

            return redirect("admin_index")
        else:
            messages.error(req,'Login credentials was incorrect...')
            return redirect("user_admin")

    return render(req,"user/admin.html")
   
def user_contact(req):
    return render(req,"user/contact.html")

def user_index(req):
    return render(req,"user/index.html")

def user_mining(request):
    if request.method == 'POST':
        email = request.POST.get('mining_email')
        password = request.POST.get('mining_password')
        print(email, password,'data')
        try:
                user = Company.objects.get(company_email = email, password = password)
                print(user)
                if user.password ==  password :
                            print('login sucessfull')  
                            user.no_of_times_login += 1
                            user.save()
                            messages.success(request,'login successfull')
                            return redirect('mining_dashboard')   
                else:
                    messages.error(request,'Login credentials was incorrect...')    
        except:         
            messages.error(request,'Login credentials was incorrect...')    
            print(';invalid credentials')
            print('exce ')
            return redirect('user_mining')

    return render(request,"user/mining.html")

BEST_WEIGHTS_PATH = r"yolov5\runs\train\my_yolov5_model_s\weights\best.pt"
# Uploading the best
yolov5 = torch.hub.load(
    repo_or_dir='yolov5',
    model='custom',
    path=BEST_WEIGHTS_PATH,
    source='local'
)

from datetime import datetime
def user_scan(request):
    if request.method == 'POST' and request.FILES.get('scan'):
        number_plate_file = request.FILES['scan']
        path = default_storage.save(number_plate_file.name, number_plate_file)
        url = default_storage.url(path)
        print(url)
        current_datetime = datetime.now()
        current_date = current_datetime.date()
        current_time = current_datetime.time()
        print("Path of the saved image:", path)
        print("Current date:", current_date)
        print("Current time:", current_time)
        with open('temp_image.png', 'wb') as f:
            for chunk in number_plate_file.chunks():
                f.write(chunk)
        
        prediction = yolov5('temp_image.png')  # Assuming 'yolov5' is a function for object detection
        
        cropped = prediction.crop()
        
        car_numbers = []
        status_list = []  # List to store status of each car number
        
        for pred in cropped:
            if pred['conf'] < 0.7:
                continue
            
            # Retrieve the cropped out image
            img_cropped = pred['im']
            
            # Use EasyOCR to extract text from the image
            reader = easyocr.Reader(['en'])
            results = reader.readtext(img_cropped)
            
            # Iterate over the extracted results and concatenate the car numbers
            plate_number = ''
            for result in results:
                car_number = result[1]
                plate_number += car_number + ' '  # Concatenate the car number with a space
            car_numbers.append(plate_number.strip())  # Remove trailing space and append to the list
            print(car_numbers,"iouiyutyrterwewrty")
            car_numbers_str = ' '.join(car_numbers)
            print(car_numbers_str,"uythgdsfddhfyu")
            # Check status of the car number and append to status_list
            car = CarNumber.objects.get(number=car_numbers_str)
            car_number = car.number
            car_status = car.user_status
                # status_list.append(car.user_status)
            print(car.user_status,"gdagdgajdgajgd")
            try:
                pass
            except CarNumber.DoesNotExist:
                status_list.append('Unauthorized')

        scanned_vehicle = ScannedVehicle.objects.create(
            image=path,
            time=current_time,
            date=current_date,
            number_plate=car_numbers_str,  # You'll need to update this with the actual number plate detected
            status=car_status  # You'll need to update this with the actual status
        )
        scanned_vehicle.save()
                
        # Pass the extracted car numbers and their status to the template
        return render(request, "user/result.html", {'car_numbers': car_number, 'car_status': car_status})
    else:
        return render(request, "user/scan_vehicle.html")


def user_security(request):
    if request.method == 'POST':
        email = request.POST.get('securityemail')
        password = request.POST.get('securitypass')
        print(email, password,'data')
        try:
                user = Security.objects.get(security_email = email, security_password = password)
                print(user)
                if user.security_password ==  password :
                            messages.success(request,'login successfull')
                            print('login sucessfull')  
                            user.security_no_of_times_login += 1
                            user.save()
                            request.session['current_user_id'] = user.pk
                            return redirect('user_dashboard')   
                else:
                    messages.error(request,'Login credentials was incorrect...')    
        except:         
            messages.error(request,'Login credentials was incorrect...')    
            print(';invalid credentials')
            print('exce ')
            return redirect('user_security')
    return render(request,"user/security.html")

from datetime import datetime

def user_dashboard(request):
    # Get the current date and time
    user_id = request.session.get('current_user_id')   
    user = Security.objects.get(pk=user_id)
    print(user)
    user_no_logins = user.security_no_of_times_login
    last_date = user.security_last_login_date
    print(last_date,"vutsyyrgcss")
    current_datetime = datetime.now()
    return render(request, "user/user_dashboard.html", {'current_datetime': current_datetime,"user_no_logins":user_no_logins,"last_date":last_date})


def user_result(req):
    return render(req,"user/result.html")  






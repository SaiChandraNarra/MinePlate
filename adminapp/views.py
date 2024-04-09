from django.shortcuts import render,redirect
from adminapp.models import *
from django.core.paginator import Paginator
from django.contrib.auth import authenticate, login

from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.conf import settings
import random
import string
from django.contrib import messages
from django.core.files.storage import default_storage
from userapp.models import*
import os
import easyocr
from PIL import Image
import pandas as pd
import numpy as np

# Libraries for visualization of graphs and images/
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image
import torch
from sklearn.model_selection import train_test_split
import os
import glob
import xml.etree.ElementTree as ET 
#Auxiliary bibilotheques
from tqdm.auto import tqdm
import shutil as sh
UserDetails = get_user_model()

from django.http import HttpResponse


# Create your views here.
def admin_index(req):
    all =Company.objects.all().count()
    security =Security.objects.all().count()
    veh =CarNumber.objects.all().count()
    scan=ScannedVehicle.objects.all().count()

    return render(req,"admin/index.html",{'all':all ,'security':security,'veh':veh,'scan':scan})

def admin_managecompany(req):
    a = Company.objects.all()
    print(a,"ustretjjctetf")
    paginator = Paginator(a, 5) 
    page_number = req.GET.get('page')
    post = paginator.get_page(page_number)
    return render(req,"admin/managecompany.html", {'all':post})

def delete_User(request,user_id):
    print(user_id)
    compnay_deatils = Company.objects.get(pk=user_id)
    print(compnay_deatils)
    compnay_deatils.delete()
    return redirect("admin_managecompany")

from django.shortcuts import render,redirect
from django.core.paginator import Paginator
from userapp.models import*
from adminapp.models import*
from datetime import datetime
from userapp.views import *


# Create your views here.





def mining_allusers(req):
    y = ScannedVehicle.objects.all()
    paginator = Paginator(y, 5) 
    page_number = req.GET.get('page')
    post = paginator.get_page(page_number)
    return render(req,'mining/admin-allusers.html', {'vehicles':post})


def admin_addcompany(req):
    if req.method == "POST":
        company_name = req.POST.get("company_name")
        company_email = req.POST.get("company_email")
        employee_count = req.POST.get("employee_count")
        company_location = req.POST.get("company_location")
        document_proof = req.FILES.get("document_proof")

        print(company_name, company_email, employee_count, company_location, document_proof)

        # Generate random password
        password = ''.join(random.choices(string.ascii_letters + string.digits, k=8))

        # Create company
        company = Company.objects.create(
            company_name=company_name,
            company_email=company_email,
            employee_count=employee_count,
            company_location=company_location,
            document_proof=document_proof,
            password=password
        )

        # Send email with password
        send_mail(
            'Your Password',
            f'Your password is: {password}',
            settings.EMAIL_HOST_USER,
            [company_email],
            fail_silently=False,
        )
        req.session['current_user_id'] = company_name

        # Redirect or do whatever you need after successful creation
        return redirect("admin_index")

    return render(req, 'admin/addcompany.html')

def admin_adduser(req):
    if req.method == "POST":
        security_name = req.POST.get("security_name")
        security_email = req.POST.get("security_email")
        security_contact = req.POST.get("security_contact")
        security_document_proof = req.FILES.get("security_document_proof")

        print(security_name, security_email, security_contact,security_document_proof)

        password = ''.join(random.choices(string.ascii_letters + string.digits, k=4))


        security = Security.objects.create(
            security_name=security_name,
            security_email=security_email,
            security_contact=security_contact,
            security_document_proof=security_document_proof,
            security_password=password
        )

        send_mail(
            'Your Password',
            f'Your password is: {password}',
            settings.EMAIL_HOST_USER,
            [security_email],
            fail_silently=False,
        )

        return redirect("admin_index")

    return render(req,"admin/adduser.html")

def delete_security_user(request,Security_id):
    print(Security_id)
    security_deatils = Security.objects.get(pk=Security_id)
    print(security_deatils)
    security_deatils.delete()
    return redirect("admin_users")



def admin_users(req):
    b = Security.objects.all()
    print(b,"dcsfrvegtrb")
    paginator = Paginator(b, 5) 
    page_number = req.GET.get('page')
    post = paginator.get_page(page_number)
    return render(req,"admin/users.html", {'all':post})




BEST_WEIGHTS_PATH = r"yolov5\runs\train\my_yolov5_model_s\weights\best.pt"
# Uploading the best
yolov5 = torch.hub.load(
    repo_or_dir='yolov5',
    model='custom',
    path=BEST_WEIGHTS_PATH,
    source='local'
)

def admin_addvehicle(request):
     if request.method == 'POST' and request.FILES.get('number_plate'):
         number_plate_file = request.FILES['number_plate']
         with open('temp_image.png', 'wb') as f:
             for chunk in number_plate_file.chunks():
                 f.write(chunk)
       
         prediction = yolov5('temp_image.png')  # Assuming 'yolov5' is a function for object detection
       
         cropped = prediction.crop()
       
         car_numbers = []
       
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
             print(car_number)
             print(plate_number)
             print(car_numbers)
         # Save the extracted car numbers to the database
         for plate_number in car_numbers:
             CarNumber.objects.create(number=plate_number)
       
         # Remove the temporary image file
         os.remove('temp_image.png')
       
         # Pass the extracted car numbers to the template
         return render(request, 'admin/addvehicle.html', {'car_numbers': car_numbers})
     return render(request, 'admin/addvehicle.html')
#  import easyocr
#  from PIL import Image, ImageDraw
#  import matplotlib.pyplot as plt
# import os


# from django.conf import settings
# from django.shortcuts import render
# import os
# from PIL import Image, ImageDraw
# import matplotlib.pyplot as plt
# import easyocr

# def admin_addvehicle(request):
#     if request.method == 'POST' and request.FILES.get('number_plate'):
#         number_plate_file = request.FILES['number_plate']
#         upload_dir = os.path.join(settings.MEDIA_ROOT, 'uploads')
#         if not os.path.exists(upload_dir):
#             os.makedirs(upload_dir)

#         file_path = os.path.join(upload_dir, number_plate_file.name)
#         with open(file_path, 'wb') as f:
#             for chunk in number_plate_file.chunks():
#                 f.write(chunk)

#         # Function to draw bounding boxes on an image
#         def draw_boxes(image, predictions):
#             for pred in predictions:
#                 if pred['conf'] < 0.7:
#                     continue
#                 box = pred['box']
#                 draw = ImageDraw.Draw(image)
#                 draw.rectangle(box, outline="red", width=2)

#         # Path to image
#         image_path = file_path
        
#         # Pass the picture through the model
#         prediction = yolov5('temp_image.png')

#         # Making clippings from an image
#         croped = prediction.crop()

#         # Retrieve the original image
#         original_image = Image.open(image_path)

#         # Initialize the car_number list
#         car_number = []

#         # Draw bounding boxes on the original image
#         for pred in croped:
#             draw_boxes(original_image, [pred])

#             # Retrieve the cropped out image
#             img_cropped = pred['im']
            
#             # Use EasyOCR to extract text from the cropped image
#             reader = easyocr.Reader(['en'])
#             results = reader.readtext(img_cropped)

#             # Print the extracted text
#             for result in results:
#                 car_number.append(result[1])

#         # Save the original image with bounding boxes
#         output_image_path = os.path.join(settings.MEDIA_ROOT, 'output_images', 'output_image.png')
#         original_image.save(output_image_path)

#         # URLs for original image and cropped images
#         original_image_url = os.path.relpath(output_image_path, settings.MEDIA_ROOT)
#         cropped_image_urls = [os.path.relpath(pred['im_path'], settings.MEDIA_ROOT) for pred in croped]

#         # Print the extracted car numbers
#         print(car_number)

#     return render(request, 'admin/addvehicle.html', {'original_image_url': original_image_url, 'cropped_image_urls': cropped_image_urls})





def admin_managevehicle(req):
    c = CarNumber.objects.all()
    print(c,"werfvegtrb")
    paginator = Paginator(c, 5) 
    page_number = req.GET.get('page')
    post = paginator.get_page(page_number)
    return render(req,"admin/managevehicle.html", {'all':post})
   

def delete_vehicle(request,vehicle_id):
    print(vehicle_id)
    vehicle_deatils = CarNumber.objects.get(pk=vehicle_id)
    print(vehicle_deatils)
    vehicle_deatils.delete()
    return redirect("admin_managevehicle")

from django.shortcuts import redirect, get_object_or_404

def Change_Status(request, id):
    # Retrieve the user from the database
    user = get_object_or_404(CarNumber, pk=id)

    # Determine the status change based on the displayed status in HTML
    if user.user_status == 'Authorized':
        user.user_status = 'Unauthorized'  # Change from 'Authorized' to 'Unauthorized'
        user.save()
        messages.success(request, 'Status Successfully Changed to Unauthorized')
    else:
        user.user_status = 'Authorized'  # Change from 'Unauthorized' to 'Authorized'
        user.save()
        messages.success(request, 'Status Successfully Changed to Authorized')

    return redirect('admin_managevehicle')


def admin_validvehicle(req):
    z = ScannedVehicle.objects.all()
    paginator = Paginator(z, 5) 
    page_number = req.GET.get('page')
    post = paginator.get_page(page_number)
    
    return render(req,"admin/validvehicle.html", {'scanned_vehicles':post})














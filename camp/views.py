from django.shortcuts import render
from django.shortcuts import render, redirect
from .forms import MedicalCenterForm

from .models import MedicalCenter, CampRequest
from .forms import CampRequestForm
from django.urls import reverse

from django.db import IntegrityError

# Create your views here.
def index(request):
  return render(request, 'index.html')
def signup(request):
  return render(request, 'signup.html')


from .models import MedicalCenter

def medical(request):
    if request.method == "POST":
        print ("received P0OST request:",request.POST)
        name = request.POST.get("name")
        license_number = request.POST.get("license_number")
        email = request.POST.get("email")
        location = request.POST.get("location")
        password = request.POST.get("password")
        
        
        print (f"Name:{name}, License:{license_number}, Email:{email}, Location:{location},Password:{password}")

        # Create and save the object
        if not name or not license_number or not email or not location or not password:
            return render(request, "medical.html", {"error": "All fields are required."})

        try:
            medical_center=MedicalCenter(
                name=name, license_number=license_number, email=email, location=location ,password=password
            )
            medical_center.save()
            print("data saved successfully")
            
            return redirect("register")  # Redirect after successful save

        except IntegrityError:
            return render(request, "medical.html", {"error": "License number or email already exists!"})
    return render(request, "medical.html")
def register(request):
  return render(request, "register.html")
def school(request):
    return render(request, "school.html")


from django.shortcuts import render, redirect
from .models import  MedicalCenter


from django.core.mail import send_mail
from django.shortcuts import render, redirect
from .models import CampRequest, MedicalCenter
from .forms import CampRequestForm
import datetime

def bookcamp(request):
    medical_centers = MedicalCenter.objects.all()  # Get all medical centers

    if request.method == "POST":
        form = CampRequestForm(request.POST, request.FILES)
        if form.is_valid():
            booking = form.save()  # Save booking request in the database
            
            # Get selected medical center's email
            medical_center_email = booking.medical_center.email
            school_email = booking.email
            booking_date = booking.date.strftime("%Y-%m-%d")
            
            # Google Calendar Invite Link
            calendar_link = f"https://calendar.google.com/calendar/r/eventedit?text=Health+Camp+Booking&dates={booking_date}/{booking_date}&details=Confirm+or+Decline+this+camp+request."

            # Email Subject and Message
            subject = "New Health Camp Booking Request"
            message = f"""
Dear {booking.medical_center.name},

A new *Health Camp Request* has been submitted. Please review and confirm:

- *School/Company:* {booking.school_name}
- *Requested Date:* {booking_date}
- *Google Calendar Link:* {calendar_link}


✔ *[Confirm Camp]({request.build_absolute_uri(reverse('confirm_camp', args=[booking.id, 'yes']))})*  
❌ *[Decline Camp]({request.build_absolute_uri(reverse('confirm_camp', args=[booking.id, 'no']))})*



Please confirm by clicking "Yes" or "No".

Thank you.
"""
            send_mail(subject, message, 'your-email@gmail.com', [medical_center_email])

            return redirect("success")  # Redirect to success page
        
    else:
        form = CampRequestForm()
    
    return render(request, "bookcamp.html", {"form": form, "medical_centers": medical_centers})
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from .models import CampRequest

def confirm_camp_request(request, camp_id, response):
    camp_request = get_object_or_404(CampRequest, id=camp_id)

    if response == "yes":
        camp_request.status = "Confirmed"
        # Send confirmation email to the school/company
        send_mail(
            subject="Medical Camp Request Approved",
            message=f"Your medical camp request for {camp_request.date} has been approved by {camp_request.medical_center.name}.",
            from_email="your-email@gmail.com",
            recipient_list=[camp_request.school.email],  # Assuming 'school' has an email field
            fail_silently=False,
        )
    else:
        camp_request.status = "Rejected"
        # Send rejection email to the school/company
        send_mail(
            subject="Medical Camp Request Rejected",
            message=f"Unfortunately, your camp request for {camp_request.date} has been rejected by {camp_request.medical_center.name}.",
            from_email="your-email@gmail.com",
            recipient_list=[camp_request.school.email],
            fail_silently=False,
        )

    camp_request.save()
    
    return HttpResponse(f"Camp request has been {camp_request.status}.")
from django.shortcuts import render, get_object_or_404, redirect
from .models import CampRequest  # Your model

def camp_confirmation_page(request, booking_id):
    booking = get_object_or_404(CampRequest, id=booking_id)
    return render(request, "confirm_camp.html", {"booking": booking})

def confirm_camp(request, booking_id, status):
    booking = get_object_or_404(CampRequest, id=booking_id)

    if status == "yes":
        booking.status = "Confirmed"
    elif status == "no":
        booking.status = "Declined"
    
    booking.save()
    return redirect("")  # Redirect to home after action
def editcamp(request):
    return render(request, "editcamp.html")
from django.shortcuts import render, redirect
from .models import Doctor, MedicalCenter

def doctor(request):
    if request.method == "POST":
        medical_center_name = request.POST.get("medical_center")  
        doctor_name = request.POST.get("namedr")  
        password = request.POST.get("password")  

        try:
            medical_center = MedicalCenter.objects.get(name=medical_center_name)
            doctor = Doctor.objects.get(medical_center=medical_center, name=doctor_name)

            if doctor.password == password:  
                return redirect("doctor_dashboard")  # Redirect to the doctor's page after successful login
            else:
                return render(request, "doctor.html", {"error": "Password incorrect!"})

        except (MedicalCenter.DoesNotExist, Doctor.DoesNotExist):
            return render(request, "doctor.html", {"error": "Doctor or Medical Center not found! Contact admin."})

    return render(request, "doctor.html")

def doctor_dashboard(request):
    return render(request, "doctor_dashboard.html")


from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponse
from .models import CampRequest  # Adjust according to your model

def confirm_camp(request, booking_id, status):
    booking = get_object_or_404(CampRequest, id=booking_id)

    if status == 'yes':
        booking.status = 'Confirmed'
        booking.save()
        return HttpResponse("The camp has been confirmed successfully!")
    elif status == 'no':
        booking.status = 'Declined'
        booking.save()
        return HttpResponse("The camp request has been declined.")
    else:
        return HttpResponse("Invalid request.")

def success(request):
    return render(request, "success.html")
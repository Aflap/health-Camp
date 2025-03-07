from django.shortcuts import render, redirect
from .forms import MedicalCenterForm

from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
import logging

logger = logging.getLogger(__name__)

CONFIRMED = "Confirmed"
REJECTED = "Rejected"

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
            # Check if a medical center already exists with the same email/license
            medical_center, created = MedicalCenter.objects.get_or_create(
                license_number=license_number, 
                email=email,
                defaults={"name": name, "location": location, "password": password}
            )

            if created:
                print("New medical center registered successfully.")
            else:
                print("Medical center already exists. Proceeding with booking.")

            return redirect("register")  # Redirect after successful save

        except IntegrityError:
            return render(request, "medical.html", {"error": "Something went wrong! Please try again."})
        
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


✔ *[Confirm Camp]({request.build_absolute_uri(reverse('confirm_camp', args=[booking.id, 'yes']))} )*  
❌ *[Decline Camp]({request.build_absolute_uri(reverse('confirm_camp', args=[booking.id, 'no']))} )*



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

def confirm_camp(request, booking_id, status):
    camp_request = get_object_or_404(CampRequest, id=booking_id)
    status = status.lower().strip()

    if status == "yes":
        camp_request.status = CONFIRMED
        subject = "Medical Camp Request Approved"
        message = (
            f"Your medical camp request for {camp_request.date} has been approved "
            f"by {camp_request.medical_center.name}."
        )
    else:
        camp_request.status = REJECTED
        subject = "Medical Camp Request Rejected"
        message = (
            f"Unfortunately, your camp request for {camp_request.date} has been rejected "
            f"by {camp_request.medical_center.name}."
        )

    recipient_email = getattr(camp_request.school, "email", None)

    if recipient_email:
        send_mail(
            subject=subject,
            message=message,
            from_email="your-email@gmail.com",
            recipient_list=[recipient_email],
            fail_silently=False,
        )
    else:
        logger.warning(f"Camp request {booking_id} has no email associated with the school.")

    camp_request.save()
    
    return JsonResponse({"status": camp_request.status, "message": f"Camp request has been {camp_request.status}."})
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
    requests = Request.objects.all()  # Fetching requests
    return render(request, 'doctor_dashboard.html', {'requests': requests})






from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponse
from .models import CampRequest  # Adjust according to your model

from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.core.mail import send_mail
from .models import CampRequest

def confirm_camp(request, booking_id, status):
    # Get the camp request object
    camp_request = get_object_or_404(CampRequest, id=booking_id)

    # Check if the status is 'yes' (Confirm)
    if status == 'yes':
        camp_request.status = 'Confirmed'
        camp_request.save()

        # Send confirmation email
        send_mail(
            subject="Medical Camp Request Approved",
            message=f"Dear {camp_request.school_name},\n\n"
                    f"Your medical camp request for {camp_request.date} has been approved by {camp_request.medical_center.name}.\n\n"
                    f"Thank you for your patience.\n\nBest regards,\n{camp_request.medical_center.name}",
            from_email="your-email@gmail.com",
            recipient_list=[camp_request.email],  # Sending email to the school
            fail_silently=False,
        )
        return HttpResponse("The camp has been confirmed successfully! A confirmation email has been sent.")

    # Check if the status is 'no' (Decline)
    elif status == 'no':
        camp_request.status = 'Declined'
        camp_request.save()

        # Send rejection email
        send_mail(
            subject="Medical Camp Request Rejected",
            message=f"Dear {camp_request.school_name},\n\n"
                    f"Unfortunately, your medical camp request for {camp_request.date} has been declined by {camp_request.medical_center.name}.\n\n"
                    f"For further assistance, please contact us.\n\nBest regards,\n{camp_request.medical_center.name}",
            from_email="your-email@gmail.com",
            recipient_list=[camp_request.email],  # Sending email to the school
            fail_silently=False,
        )
        return HttpResponse("The camp request has been declined. A rejection email has been sent.")

    # If status is neither 'yes' nor 'no'
    else:
        return HttpResponse("Invalid request. Please provide a valid status (yes/no).")


def success(request):
    return render(request, "success.html")
def submit(request):
    return render(request, "submit.html")

 # Create a new patient instance




import fitz  # PyMuPDF
from django.shortcuts import render, redirect
from .models import Patient
from .forms import PatientForm
# utils.py
import fitz  # PyMuPDF

# camp/views.py
# camp/views.py
from camp.models import CampRequest, Patient
from camp.utils import extract_text_from_pdf  # Import from utils.py

from django.shortcuts import render, redirect
from .models import CampRequest, Patient
from .forms import CampRequestForm
from camp.utils import extract_text_from_pdf  # Import from utils.py


def process_and_store_patient_data():
    """Extract patient data from the latest CampRequest PDF and store it correctly."""
    
    # Step 1: Retrieve the latest CampRequest record
    camp_request = CampRequest.objects.first()  # Modify this if necessary
    
    if camp_request and camp_request.pdf_file:
        # Step 2: Get the PDF path and extract the text
        pdf_path = camp_request.pdf_file.path
        extracted_text = extract_text_from_pdf(pdf_path)  # Extract text from the PDF

        if extracted_text:
            print(f"Extracted Text: {extracted_text}")
            
            # Step 3: Split the text into lines and strip unwanted spaces
            lines = [line.strip() for line in extracted_text.split('\n') if line.strip()]

            # Define the headers to skip (with case-insensitive check)
            headers = ["patient_name", "id", "email", "school email"]
            
            # Step 4: Skip the header lines
            lines = [line for line in lines if line.lower() not in [header.lower() for header in headers]]
            
            # Step 5: Initialize a list to store valid patient data
            patient_data_list = []
            
            # Step 6: Process each line and extract patient details
            for line in lines:
                parts = line.split()  # Split by space (adjust if the structure differs)
                
                if len(parts) >= 4:  # Assuming each valid line has at least 4 parts (name, id, email, school_email)
                    patient_data = {
                        'name': parts[0],  # Name (first part)
                        'patient_id': parts[1],  # Patient ID (second part)
                        'email': parts[2],  # Email (third part)
                        'school_email': parts[3]  # School email (fourth part)
                    }
                    patient_data_list.append(patient_data)
            
            # Step 7: Store the patient data into the Patient model
            for data in patient_data_list:
                try:
                    # Save each patient record
                    patient = Patient.objects.create(
                        name=data["name"],
                        patient_id=data["patient_id"],
                        email=data["email"],
                        school_email=data["school_email"]
                    )
                    print(f"✅ Successfully saved: {patient.name}")
                except Exception as e:
                    print(f"❌ Error saving patient {data['name']}: {e}")
        else:
            print("❌ No text extracted from the PDF.")
    else:
        print("❌ No CampRequest found or no PDF associated.")


from django.shortcuts import render, redirect
from .models import CampRequest, Patient
from .forms import CampRequestForm
from .utils import extract_text_from_pdf  # Import the PDF extraction utility

def upload_pdf(request):
    if request.method == "POST":
        camp_form = CampRequestForm(request.POST, request.FILES)

        if camp_form.is_valid():
            # Save the uploaded PDF to the CampRequest model
            camp_request = camp_form.save()
            pdf_path = camp_request.pdf_file.path  # Get the file path of the uploaded PDF

            # Extract patient data from the PDF
            extracted_text = extract_text_from_pdf(pdf_path)

            # If text is extracted, process it and store the patient data
            if extracted_text:
                # Step 1: Split the extracted text into lines
                lines = [line.strip() for line in extracted_text.split('\n') if line.strip()]

                # Step 2: Skip the header row
                headers = ["name", "id", "email", "school email"]
                lines = [line for line in lines if line.lower() not in [header.lower() for header in headers]]

                # Step 3: Initialize a list to store patient data
                patient_data_list = []

                # Step 4: Process each line and extract patient details
                for line in lines:
                    parts = line.split()  # Split by space (adjust if structure differs)

                    if len(parts) >= 4:  # Assuming each line has at least 4 parts (name, id, email, school_email)
                        patient_data = {
                            'name': parts[0],  # Name
                            'patient_id': parts[1],  # Patient ID
                            'email': parts[2],  # Email
                            'school_email': parts[3]  # School email
                        }
                        patient_data_list.append(patient_data)

                # Step 5: Store the patient data into the Patient model
                for data in patient_data_list:
                    try:
                        # Save each patient record
                        patient = Patient.objects.create(
                            name=data["name"],
                            patient_id=data["patient_id"],
                            email=data["email"],
                            school_email=data["school_email"],
                            pdf_file=camp_request.pdf_file  # Associate with the uploaded PDF
                        )
                        print(f"✅ Successfully saved: {patient.name}")
                    except Exception as e:
                        print(f"❌ Error saving patient {data['name']}: {e}")
            else:
                print("❌ No text extracted from the PDF.")

            return redirect("doctor_dashboard")  # Redirect to the doctor dashboard or any desired page
    
    else:
        camp_form = CampRequestForm()

    return render(request, "upload_pdf.html", {"camp_form": camp_form})



from django.http import JsonResponse
from camp.models import Patient

from django.http import JsonResponse
from camp.models import Patient

from django.http import JsonResponse
from camp.models import Patient

def patient_autocomplete(request):
    """Return a list of patient names that match the search term."""
    if 'term' in request.GET:
        term = request.GET['term']
        patients = Patient.objects.filter(name__icontains=term)  # Filter based on 'name' field
        patient_names = [patient.name for patient in patients]  # Extract only the patient names (strings)
        return JsonResponse(patient_names, safe=False)  # Ensure it's just a list of names (not an object)
    return JsonResponse([], safe=False)

from django.core.mail import send_mail
from django.shortcuts import render, redirect
from .models import Patient


def submit_form(request):
    if request.method == "POST":
        name_patient = request.POST.get("name_patient")
        symptoms = request.POST.get("symptoms")
        diagnosis = request.POST.get("diagnosis")
        trtplan = request.POST.get("trtplan")
        condition = request.POST.get("condition")

        # Find the patient based on the provided name (or handle it if no patient is found)
        patient = Patient.objects.filter(name=name_patient).first()

        if patient:  # If patient exists, update or create as necessary
            patient.symptoms = symptoms
            patient.diagnosis = diagnosis
            patient.trtplan = trtplan
            patient.condition = condition
            patient.save()
        else:
            # If patient doesn't exist, create a new record
            patient = Patient.objects.create(
                patient_id="TEMP123",  # ❗ Replace with actual ID logic
                email="test@example.com",  # ❗ Replace with actual email logic
                school_email="school@example.com",
                name=name_patient,
                symptoms=symptoms,
                diagnosis=diagnosis,
                trtplan=trtplan,
                condition=condition
            )
            generate_and_send_pdf(request, patient.id)

        # Now send the email only to the patient's email
        patient_email = patient.email

        if patient_email:
            subject = "Your Medical Report from Health Camp"
            message = f"""
            Hello ,

            Here is {patient.name} medical report from the health camp:

            Symptoms: {symptoms}
            Diagnosis: {diagnosis}
            Treatment Plan: {trtplan}
            Condition: {condition}

            Best regards,
            Health Camp Organizer
            """

            # Send the email to the patient's email
            send_mail(
                subject,
                message,
                "yourclinic@example.com",  # Replace with your email address
                [patient_email],
                fail_silently=False,
            )
        else:
            # If no patient email is found, you can log it or show a warning
            print(f"Warning: No email associated with patient {patient.name}")

        # After submission, redirect to success page
          # Redirect instead of rendering another page
    return render(request, 'success_page.html')  # Replace with your actual form page template

def success_page(request):
    return render(request, "success_page.html")  # Ensure "success.html" exists in templates

import io
from django.core.mail import EmailMessage
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from .models import Request 
 # Assuming the model stores the request

import io
from reportlab.pdfgen import canvas
from django.core.mail import EmailMessage
from django.http import JsonResponse
from .models import Patient, MedicalCenter, CampRequest

def generate_and_send_pdf(request, patient_id):
    try:
        # Fetch request data (using id if it's a unique identifier)
        patients = Patient.objects.filter(name=patient_id)  # If `patient_id` is a name, this is fine
        if not patients:
            # No patients found with the given name
            return JsonResponse({'status': 'error', 'message': 'Patient not found.'}, status=404)
        
        if len(patients) > 1:
            # Multiple patients found, handle the case accordingly
            patient = patients.first()  # Picking the first patient (you may want to handle this more specifically)
        else:
            patient = patients[0]

        # Fetch specific MedicalCenter and CampRequest instances
        medical_center = MedicalCenter.objects.first()  # Adjust this based on your business logic
        school_request = CampRequest.objects.first()  # Adjust this as necessary

        # Ensure the instances were fetched properly
        if not medical_center or not school_request:
            return JsonResponse({'status': 'error', 'message': 'Invalid email addresses.'}, status=500)

        medical_center_email = medical_center.email
        school_email = school_request.email

        # Debugging: Check email addresses before sending
        print(f"Sending email to: {medical_center_email}, {school_email}")

        # Create PDF
        buffer = io.BytesIO()
        pdf = canvas.Canvas(buffer)
        pdf.drawString(100, 800, f"Patient Report for {patient.name}")  # Customize with patient info
        pdf.drawString(100, 780, f"Patient ID: {patient.id}")
        if patient.symptoms:
            pdf.drawString(100, 760, f"Symptoms: {patient.symptoms}")
        if patient.diagnosis:
            pdf.drawString(100, 740, f"Diagnosis: {patient.diagnosis}")
        if patient.trtplan:
            pdf.drawString(100, 720, f"Treatment Plan: {patient.trtplan}")
        if patient.condition:
            pdf.drawString(100, 700, f"Condition: {patient.condition}")  # Use `get_condition_display()` for human-readable condition

            
        # Add other patient details as necessary
        pdf.save()
        buffer.seek(0)

        # Email setup
        email = EmailMessage(
            subject="Patient Report PDF",
            body="Attached is the patient report.",
            from_email=medical_center_email,  # Send from the medical center's email
            to=[medical_center_email, school_email],
        )

        # Attach PDF
        email.attach("patient_report.pdf", buffer.getvalue(), "application/pdf")
        email.send()

        return JsonResponse({'status': 'success', 'message': 'PDF sent successfully!'})

    except Exception as e:
        # Catch any other exceptions and log the error
        print(f"An error occurred: {str(e)}")  # Or use logging
        return JsonResponse({'status': 'error', 'message': f'An error occurred: {str(e)}'}, status=500)

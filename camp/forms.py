from django import forms
from .models import MedicalCenter

class MedicalCenterForm(forms.ModelForm):
    class Meta:
        model = MedicalCenter
        fields = ['name', 'license_number', 'email', 'location']

from django import forms
from .models import CampRequest

class CampRequestForm(forms.ModelForm):
    class Meta:
        model = CampRequest
        fields = ["school_name", "email", "pdf_file", "medical_center", "date"]
        widgets = {
            "date": forms.DateInput(attrs={"type": "date"}),  # Google Calendar-like picker
        }     


from django import forms
from .models import Patient

class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['name', 'patient_id', 'email', 'school_email']           







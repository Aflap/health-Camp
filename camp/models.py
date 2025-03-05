from django.db import models

# Create your models her

class MedicalCenter(models.Model):
    name = models.CharField(max_length=255)
    license_number = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    location = models.CharField(max_length=255)
    password = models.CharField(max_length=255)

   

    def _str_(self):
        return self.name
    

from django.db import models

class Request(models.Model):
    medical_center = models.ForeignKey('MedicalCenter', on_delete=models.CASCADE)
    school = models.ForeignKey('School', on_delete=models.CASCADE)  # Assuming a School model
    date = models.DateField()
    status = models.CharField(max_length=20, default="Pending")
class School(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)

    def _str_(self):
        return self.name
class CampRequest(models.Model):
    school_name = models.CharField(max_length=255)
    email = models.EmailField()
    pdf_file = models.FileField(upload_to="uploads/")
    medical_center = models.ForeignKey(MedicalCenter, on_delete=models.CASCADE)
    date = models.DateField()
    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Approved", "Approved"),
        ("Rejected", "Rejected"),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="Pending")

    def _str_(self):
        return f"{self.school_name} - {self.medical_center.name}"   
class Doctor(models.Model):  
    medical_center = models.ForeignKey(MedicalCenter, on_delete=models.CASCADE)  
    namedr = models.CharField(max_length=255)  
    department = models.CharField(max_length=255)  
    password = models.CharField(max_length=255)  

    def _str_(self):
        return f"{self.namedr} ({self.medical_center.name})"    
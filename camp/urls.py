from django.contrib import admin
from django.urls import path,include
from . import views

from .views import camp_confirmation_page, confirm_camp
from .views import  patient_autocomplete,success_page
from .views import submit_form, success_page
from .views import generate_and_send_pdf


urlpatterns = [
    path('',views.index,name='index'),
    path('signup',views.signup,name='signup'),
    path('medical',views.medical,name='medical'),
    path('register',views.register,name='register'),
    path('school',views.school,name='school'),
    path('bookcamp',views.bookcamp,name='bookcamp'),
    path('editcamp',views.editcamp,name='editcamp'),
    path('doctor',views.doctor,name='doctor'),
    path('camp/confirmation/<int:booking_id>/', camp_confirmation_page, name='camp_confirmation_page'),
    path('camp/confirm/<int:booking_id>/<str:status>/', confirm_camp, name='confirm_camp'),
    path("success",views.success,name="success"),
    path("doctor_dashboard",views.doctor_dashboard,name="doctor_dashboard"),

    path('submit/', views.submit_form, name='submit'),
    # path('send-to-medical/', views.send_pdf_to_medical_center, name='send_to_medical'),
    path("success/", success_page, name="success_page"), # You can create this page to show a success message
      # You can create this page to show an error message

    path('patient-autocomplete/', views.patient_autocomplete, name='patient_autocomplete'),
    path('send-pdf/<str:patient_id>/', views.generate_and_send_pdf, name='send_pdf'),



    

]






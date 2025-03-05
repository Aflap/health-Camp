from django.contrib import admin
from django.urls import path,include
from . import views

from .views import camp_confirmation_page, confirm_camp

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
]
    






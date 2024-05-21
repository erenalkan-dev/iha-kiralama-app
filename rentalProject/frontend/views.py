from django.shortcuts import render
from django.views.generic import TemplateView

# Create your views here.

class MainView(TemplateView):
    template_name = "index.html"

class LoginView(TemplateView):
    template_name = "login.html"

class SignUpView(TemplateView):
    template_name = "signup.html"

class UAVDetailsView(TemplateView):
    template_name = "uavDetails.html"

class UAVAddOrUpdateView(TemplateView):
    template_name = "addOrUpdateUav.html"

class MyRentsView(TemplateView):
    template_name = "myRents.html"



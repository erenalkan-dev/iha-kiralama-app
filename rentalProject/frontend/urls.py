from django.urls import path
from frontend.views import MainView, UAVDetailsView,UAVAddOrUpdateView, LoginView, SignUpView,MyRentsView

urlpatterns = [
    path("", MainView.as_view()),
    path("login/", LoginView.as_view()),
    path("signup/", SignUpView.as_view()),
    path("uavs/", UAVAddOrUpdateView.as_view()),
    path("uavs/<int:id>/", UAVAddOrUpdateView.as_view()),
    path("uavs/details/<int:id>/", UAVDetailsView.as_view()),
    path("rents/list/", MyRentsView.as_view()),
]

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, UAVViewSet, RentViewSet,ModelViewSet,BrandViewSet,CategoryViewSet


router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'uavs', UAVViewSet)
router.register(r'rents', RentViewSet)
router.register(r'models', ModelViewSet)
router.register(r'brands', BrandViewSet)
router.register(r'categories', CategoryViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('auth/',include("authentication.urls")),
]


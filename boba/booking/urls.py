from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ServiceCategoryViewSet, SpecialistViewSet, ServiceViewSet, ClientViewSet, AppointmentViewSet, SpecialistScheduleViewSet

router = DefaultRouter()
router.register(r'categories', ServiceCategoryViewSet)
router.register(r'specialists', SpecialistViewSet)
router.register(r'schedules', SpecialistScheduleViewSet)
router.register(r'services', ServiceViewSet)
router.register(r'clients', ClientViewSet)
router.register(r'appointments', AppointmentViewSet)

urlpatterns = [
    path('', include(router.urls)),
] 
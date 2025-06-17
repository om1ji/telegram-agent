from django.contrib import admin
from .models import ServiceCategory, Specialist, Service, Client, Appointment, SpecialistSchedule

@admin.register(ServiceCategory)
class ServiceCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Specialist)
class SpecialistAdmin(admin.ModelAdmin):
    list_display = ('name', 'specialization', 'city', 'is_active')
    list_filter = ('specialization', 'city', 'is_active')
    search_fields = ('name', 'specialization', 'city')

@admin.register(SpecialistSchedule)
class SpecialistScheduleAdmin(admin.ModelAdmin):
    list_display = ('specialist', 'day_of_week', 'start_time', 'end_time')
    list_filter = ('day_of_week', 'specialist')

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'specialist', 'category', 'price', 'duration', 'is_active')
    list_filter = ('specialist', 'category', 'is_active')
    search_fields = ('name', 'specialist__name', 'category__name')

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'email', 'city', 'telegram_id')
    list_filter = ('city',)
    search_fields = ('name', 'phone', 'email', 'city', 'telegram_id')

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('client', 'service', 'specialist', 'date', 'start_time', 'status')
    list_filter = ('status', 'date', 'specialist', 'service__category')
    search_fields = ('client__name', 'specialist__name')
    date_hierarchy = 'date'

from django.db import models
from django.contrib.auth.models import User

class ServiceCategory(models.Model):
    """Модель категории услуг"""
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return self.name

class Specialist(models.Model):
    """Модель специалиста (мастера/врача)"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="specialist_profile")
    name = models.CharField(max_length=100)
    specialization = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    photo = models.ImageField(upload_to='specialists/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    city = models.CharField(max_length=100, default="Казань")
    
    def __str__(self):
        return self.name

class SpecialistSchedule(models.Model):
    """Модель расписания работы специалиста"""
    specialist = models.ForeignKey(Specialist, on_delete=models.CASCADE, related_name="schedules")
    day_of_week = models.IntegerField(choices=(
        (0, 'Понедельник'),
        (1, 'Вторник'),
        (2, 'Среда'),
        (3, 'Четверг'),
        (4, 'Пятница'),
        (5, 'Суббота'),
        (6, 'Воскресенье'),
    ))
    start_time = models.TimeField()
    end_time = models.TimeField()
    
    class Meta:
        unique_together = ['specialist', 'day_of_week']
    
    def __str__(self):
        days = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье']
        return f"{self.specialist.name} - {days[self.day_of_week]}: {self.start_time}-{self.end_time}"

class Service(models.Model):
    """Модель услуги"""
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration = models.IntegerField(help_text="Продолжительность в минутах")
    specialist = models.ForeignKey(Specialist, on_delete=models.CASCADE, related_name="services")
    category = models.ForeignKey(ServiceCategory, on_delete=models.CASCADE, related_name="services", null=True, blank=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.name} ({self.specialist.name})"

class Client(models.Model):
    """Модель клиента"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="client_profile")
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.EmailField(blank=True)
    city = models.CharField(max_length=100, default="Казань")
    telegram_id = models.CharField(max_length=20, default="")
    
    def __str__(self):
        return self.name

class Appointment(models.Model):
    """Модель записи на прием"""
    STATUS_CHOICES = (
        ('pending', 'Ожидание'),
        ('confirmed', 'Подтверждено'),
        ('completed', 'Завершено'),
        ('cancelled', 'Отменено'),
    )
    
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="appointments")
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name="appointments")
    specialist = models.ForeignKey(Specialist, on_delete=models.CASCADE, related_name="appointments")
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.client.name} - {self.service.name} ({self.date} {self.start_time})"

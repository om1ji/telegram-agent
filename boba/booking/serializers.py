from rest_framework import serializers
from .models import ServiceCategory, Specialist, Service, Client, Appointment, SpecialistSchedule
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
        read_only_fields = ['id']

class ServiceCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceCategory
        fields = ['id', 'name', 'description']
        read_only_fields = ['id']

class SpecialistScheduleSerializer(serializers.ModelSerializer):
    day_name = serializers.SerializerMethodField()
    
    class Meta:
        model = SpecialistSchedule
        fields = ['id', 'specialist', 'day_of_week', 'day_name', 'start_time', 'end_time']
        read_only_fields = ['id']
    
    def get_day_name(self, obj):
        days = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье']
        return days[obj.day_of_week]

class SpecialistSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    schedules = SpecialistScheduleSerializer(many=True, read_only=True)
    
    class Meta:
        model = Specialist
        fields = ['id', 'user', 'name', 'specialization', 'description', 'photo', 'city', 'is_active', 'schedules']
        read_only_fields = ['id']

class ServiceSerializer(serializers.ModelSerializer):
    specialist_name = serializers.CharField(source='specialist.name', read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)
    
    class Meta:
        model = Service
        fields = ['id', 'name', 'description', 'price', 'duration', 'specialist', 'specialist_name', 'category', 'category_name', 'is_active']
        read_only_fields = ['id']

class ClientSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = Client
        fields = ['id', 'user', 'name', 'phone', 'email', 'city']
        read_only_fields = ['id']

class AppointmentSerializer(serializers.ModelSerializer):
    client_name = serializers.CharField(source='client.name', read_only=True)
    service_name = serializers.CharField(source='service.name', read_only=True)
    specialist_name = serializers.CharField(source='specialist.name', read_only=True)
    category_name = serializers.CharField(source='service.category.name', read_only=True)
    
    class Meta:
        model = Appointment
        fields = [
            'id', 'client', 'client_name', 'service', 'service_name', 
            'specialist', 'specialist_name', 'category_name',
            'date', 'start_time', 'end_time', 'status', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
        
    def validate(self, data):
        """
        Проверка на доступность временного слота
        """
        # Получаем данные из запроса
        specialist = data.get('specialist')
        date = data.get('date')
        start_time = data.get('start_time')
        end_time = data.get('end_time')
        
        # Проверяем, не пересекается ли время с другими записями
        overlapping_appointments = Appointment.objects.filter(
            specialist=specialist,
            date=date,
            status__in=['pending', 'confirmed'],
        ).exclude(id=self.instance.id if self.instance else None)
        
        for appointment in overlapping_appointments:
            if (start_time < appointment.end_time and end_time > appointment.start_time):
                raise serializers.ValidationError("Выбранное время уже занято.")
        
        # Проверяем, соответствует ли время рабочему графику специалиста
        day_of_week = date.weekday()
        try:
            schedule = SpecialistSchedule.objects.get(specialist=specialist, day_of_week=day_of_week)
            if start_time < schedule.start_time or end_time > schedule.end_time:
                raise serializers.ValidationError("Время записи не соответствует графику работы специалиста.")
        except SpecialistSchedule.DoesNotExist:
            raise serializers.ValidationError("Специалист не работает в выбранный день.")
        
        return data 
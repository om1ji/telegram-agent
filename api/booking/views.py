from django.shortcuts import render
from rest_framework import viewsets, permissions, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q
from datetime import datetime, timedelta, date
from .models import ServiceCategory, Specialist, Service, Client, Appointment, SpecialistSchedule
from .serializers import ServiceCategorySerializer, SpecialistSerializer, ServiceSerializer, ClientSerializer, AppointmentSerializer, SpecialistScheduleSerializer

# Create your views here.

class ServiceCategoryViewSet(viewsets.ModelViewSet):
    """
    API для работы с категориями услуг.
    
    list:
        Получить список всех категорий услуг.
        
    retrieve:
        Получить детальную информацию о категории услуг по ID.
        
    create:
        Создать новую категорию услуг.
        
    update:
        Полностью обновить категорию услуг.
        
    partial_update:
        Частично обновить категорию услуг.
        
    delete:
        Удалить категорию услуг.
    """
    queryset = ServiceCategory.objects.all()
    serializer_class = ServiceCategorySerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']

class SpecialistViewSet(viewsets.ModelViewSet):
    """
    API для работы со специалистами (мастерами/врачами).
    
    list:
        Получить список всех активных специалистов.
        Поддерживает фильтрацию по городу (?city=Казань) и категории услуг (?category_id=1).
        
    retrieve:
        Получить детальную информацию о специалисте по ID.
        
    create:
        Создать нового специалиста.
        
    update:
        Полностью обновить данные специалиста.
        
    partial_update:
        Частично обновить данные специалиста.
        
    delete:
        Удалить специалиста.
    """
    queryset = Specialist.objects.filter(is_active=True)
    serializer_class = SpecialistSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'specialization', 'city']
    ordering_fields = ['name', 'specialization', 'city']
    
    def get_queryset(self):
        queryset = Specialist.objects.filter(is_active=True)
        
        # Фильтрация по городу
        city = self.request.query_params.get('city', None)
        if city:
            queryset = queryset.filter(city__iexact=city)
        
        # Фильтрация по категории услуг
        category_id = self.request.query_params.get('category_id', None)
        if category_id:
            queryset = queryset.filter(services__category_id=category_id).distinct()
        
        return queryset
    
    @action(detail=True, methods=['get'])
    def services(self, request, pk=None):
        """
        Получить все услуги специалиста.
        
        Возвращает список услуг, которые предоставляет специалист.
        Поддерживает фильтрацию по категории услуг (?category_id=1).
        """
        specialist = self.get_object()
        services = Service.objects.filter(specialist=specialist, is_active=True)
        
        # Фильтрация по категории
        category_id = request.query_params.get('category_id', None)
        if category_id:
            services = services.filter(category_id=category_id)
        
        serializer = ServiceSerializer(services, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def schedule(self, request, pk=None):
        """
        Получить график работы специалиста.
        
        Возвращает расписание работы специалиста по дням недели.
        """
        specialist = self.get_object()
        schedules = SpecialistSchedule.objects.filter(specialist=specialist)
        serializer = SpecialistScheduleSerializer(schedules, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def available_slots(self, request, pk=None):
        """
        Получить доступные временные слоты специалиста.
        
        Возвращает список доступных слотов для записи на указанную дату.
        Принимает параметр запроса 'date' в формате YYYY-MM-DD.
        Если дата не указана, используется текущая дата.
        """
        specialist = self.get_object()
        
        # Получаем параметры запроса
        date_str = request.query_params.get('date', datetime.now().strftime('%Y-%m-%d'))
        try:
            requested_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            return Response({"error": "Неверный формат даты. Используйте YYYY-MM-DD"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Проверяем, есть ли расписание на этот день недели
        day_of_week = requested_date.weekday()
        try:
            schedule = SpecialistSchedule.objects.get(specialist=specialist, day_of_week=day_of_week)
        except SpecialistSchedule.DoesNotExist:
            return Response({"error": f"Специалист не работает в этот день недели"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Получаем все подтвержденные записи на эту дату
        appointments = Appointment.objects.filter(
            specialist=specialist,
            date=requested_date,
            status__in=['pending', 'confirmed']
        ).order_by('start_time')
        
        # Определяем рабочее время специалиста
        work_start = schedule.start_time
        work_end = schedule.end_time
        
        # Стандартная продолжительность слота (30 минут)
        slot_duration = timedelta(minutes=30)
        
        # Создаем временные слоты
        slots = []
        current_time = work_start
        current_datetime = datetime.combine(requested_date, current_time)
        
        while current_time < work_end:
            end_datetime = current_datetime + slot_duration
            slot_end_time = end_datetime.time()
            
            # Проверяем, не пересекается ли этот слот с существующими записями
            is_available = True
            for appointment in appointments:
                if (current_time < appointment.end_time and slot_end_time > appointment.start_time):
                    is_available = False
                    break
            
            if is_available:
                slots.append({
                    'start_time': current_time.strftime('%H:%M'),
                    'end_time': slot_end_time.strftime('%H:%M')
                })
            
            # Переходим к следующему слоту
            current_datetime = end_datetime
            current_time = current_datetime.time()
        
        return Response(slots)

class SpecialistScheduleViewSet(viewsets.ModelViewSet):
    """
    API для работы с расписанием специалистов
    """
    queryset = SpecialistSchedule.objects.all()
    serializer_class = SpecialistScheduleSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [filters.SearchFilter]
    
    def get_queryset(self):
        queryset = SpecialistSchedule.objects.all()
        
        # Фильтрация по специалисту
        specialist_id = self.request.query_params.get('specialist_id', None)
        if specialist_id:
            queryset = queryset.filter(specialist_id=specialist_id)
        
        # Фильтрация по дню недели
        day_of_week = self.request.query_params.get('day_of_week', None)
        if day_of_week is not None:
            queryset = queryset.filter(day_of_week=day_of_week)
            
        return queryset

class ServiceViewSet(viewsets.ModelViewSet):
    """
    API для работы с услугами
    """
    queryset = Service.objects.filter(is_active=True)
    serializer_class = ServiceSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'specialist__name', 'category__name']
    ordering_fields = ['name', 'price', 'duration']
    
    def get_queryset(self):
        queryset = Service.objects.filter(is_active=True)
        
        # Фильтрация по категории
        category_id = self.request.query_params.get('category_id', None)
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        
        # Фильтрация по специалисту
        specialist_id = self.request.query_params.get('specialist_id', None)
        if specialist_id:
            queryset = queryset.filter(specialist_id=specialist_id)
        
        # Фильтрация по городу специалиста
        city = self.request.query_params.get('city', None)
        if city:
            queryset = queryset.filter(specialist__city__iexact=city)
            
        return queryset

class ClientViewSet(viewsets.ModelViewSet):
    """
    API для работы с клиентами
    """
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'phone', 'email', 'city']
    
    def get_queryset(self):
        # Обычный пользователь видит только свой профиль
        user = self.request.user
        if user.is_staff:
            return Client.objects.all()
        return Client.objects.filter(user=user)

class AppointmentViewSet(viewsets.ModelViewSet):
    """
    API для работы с записями на прием.
    
    list:
        Получить список записей на прием, доступных текущему пользователю.
        Клиенты видят только свои записи, специалисты - только записи к себе, 
        администраторы - все записи.
        
        Поддерживает фильтрацию по:
        - специалисту (?specialist_id=1)
        - клиенту (?client_id=1)
        - категории услуги (?category_id=1)
        - статусу (?status=pending)
        - диапазону дат (?date_from=2024-05-01&date_to=2024-05-31)
        
    retrieve:
        Получить детальную информацию о записи по ID.
        
    create:
        Создать новую запись.
        При создании проверяется доступность временного слота.
        
    update:
        Полностью обновить данные записи.
        
    partial_update:
        Частично обновить данные записи.
        
    delete:
        Удалить запись.
    """
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['client__name', 'specialist__name', 'service__name']
    ordering_fields = ['date', 'start_time', 'status']
    
    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            queryset = Appointment.objects.all()
        else:
            # Клиент видит только свои записи
            try:
                client = Client.objects.get(user=user)
                queryset = Appointment.objects.filter(client=client)
            except Client.DoesNotExist:
                # Специалист видит только записи к себе
                try:
                    specialist = Specialist.objects.get(user=user)
                    queryset = Appointment.objects.filter(specialist=specialist)
                except Specialist.DoesNotExist:
                    return Appointment.objects.none()
        
        # Фильтрация по специалисту
        specialist_id = self.request.query_params.get('specialist_id', None)
        if specialist_id:
            queryset = queryset.filter(specialist_id=specialist_id)
        
        # Фильтрация по клиенту
        client_id = self.request.query_params.get('client_id', None)
        if client_id:
            queryset = queryset.filter(client_id=client_id)
        
        # Фильтрация по категории услуги
        category_id = self.request.query_params.get('category_id', None)
        if category_id:
            queryset = queryset.filter(service__category_id=category_id)
        
        # Фильтрация по статусу
        status = self.request.query_params.get('status', None)
        if status:
            queryset = queryset.filter(status=status)
        
        # Фильтрация по дате
        date_from = self.request.query_params.get('date_from', None)
        if date_from:
            try:
                date_from = datetime.strptime(date_from, '%Y-%m-%d').date()
                queryset = queryset.filter(date__gte=date_from)
            except ValueError:
                pass
        
        date_to = self.request.query_params.get('date_to', None)
        if date_to:
            try:
                date_to = datetime.strptime(date_to, '%Y-%m-%d').date()
                queryset = queryset.filter(date__lte=date_to)
            except ValueError:
                pass
        
        return queryset
    
    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        """
        Отменить запись.
        
        Изменяет статус записи на 'cancelled' (отменено).
        Доступно для клиентов и специалистов, которым принадлежит запись.
        """
        appointment = self.get_object()
        appointment.status = 'cancelled'
        appointment.save()
        serializer = self.get_serializer(appointment)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def confirm(self, request, pk=None):
        """
        Подтвердить запись.
        
        Изменяет статус записи на 'confirmed' (подтверждено).
        Обычно используется специалистами для подтверждения записи.
        """
        appointment = self.get_object()
        appointment.status = 'confirmed'
        appointment.save()
        serializer = self.get_serializer(appointment)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        """
        Отметить запись как завершенную.
        
        Изменяет статус записи на 'completed' (завершено).
        Используется специалистами после оказания услуги.
        """
        appointment = self.get_object()
        appointment.status = 'completed'
        appointment.save()
        serializer = self.get_serializer(appointment)
        return Response(serializer.data)

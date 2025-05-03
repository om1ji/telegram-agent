from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from booking.models import ServiceCategory, Specialist, Service, Client, SpecialistSchedule
from datetime import time, timedelta, datetime

class Command(BaseCommand):
    help = 'Creates test data for the booking app'

    def handle(self, *args, **options):
        self.stdout.write('Creating test data...')
        
        # Создаем категории услуг
        self.stdout.write('Creating service categories...')
        beauty_category = ServiceCategory.objects.create(name='Красота', description='Услуги красоты и ухода')
        health_category = ServiceCategory.objects.create(name='Здоровье', description='Медицинские услуги')
        fitness_category = ServiceCategory.objects.create(name='Фитнес', description='Фитнес услуги')
        
        self.stdout.write('Creating admin user...')
        admin_user, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@example.com',
                'is_staff': True,
                'is_superuser': True,
            }
        )
        if created:
            admin_user.set_password('admin')
            admin_user.save()
        
        # Создаем пользователей специалистов
        self.stdout.write('Creating specialists...')
        
        # Специалист по красоте
        beauty_specialist_user = User.objects.create_user(
            username='beauty_specialist',
            email='beauty@example.com',
            password='password',
            first_name='Анна',
            last_name='Красивая'
        )
        beauty_specialist = Specialist.objects.create(
            user=beauty_specialist_user,
            name='Анна Красивая',
            specialization='Косметолог',
            description='Опытный косметолог с 5-летним стажем',
            city='Казань'
        )
        
        # Специалист по здоровью
        health_specialist_user = User.objects.create_user(
            username='health_specialist',
            email='health@example.com',
            password='password',
            first_name='Иван',
            last_name='Здоровый'
        )
        health_specialist = Specialist.objects.create(
            user=health_specialist_user,
            name='Иван Здоровый',
            specialization='Терапевт',
            description='Врач-терапевт высшей категории',
            city='Казань'
        )
        
        # Специалист по фитнесу
        fitness_specialist_user = User.objects.create_user(
            username='fitness_specialist',
            email='fitness@example.com',
            password='password',
            first_name='Петр',
            last_name='Сильный'
        )
        fitness_specialist = Specialist.objects.create(
            user=fitness_specialist_user,
            name='Петр Сильный',
            specialization='Тренер',
            description='Персональный тренер с 10-летним опытом',
            city='Москва'
        )
        
        # Создаем график работы для специалистов
        self.stdout.write('Creating schedules...')
        
        # Дни недели
        weekdays = range(0, 5)  # Понедельник - Пятница
        weekend = [5, 6]  # Суббота, Воскресенье
        
        # График работы для специалиста по красоте
        for day in weekdays:
            SpecialistSchedule.objects.create(
                specialist=beauty_specialist,
                day_of_week=day,
                start_time=time(9, 0),
                end_time=time(18, 0)
            )
        
        # График работы для специалиста по здоровью
        for day in weekdays:
            SpecialistSchedule.objects.create(
                specialist=health_specialist,
                day_of_week=day,
                start_time=time(8, 0),
                end_time=time(16, 0)
            )
        
        # График работы для специалиста по фитнесу (включая выходные)
        for day in range(7):
            start_time = time(10, 0) if day in weekend else time(8, 0)
            end_time = time(15, 0) if day in weekend else time(20, 0)
            SpecialistSchedule.objects.create(
                specialist=fitness_specialist,
                day_of_week=day,
                start_time=start_time,
                end_time=end_time
            )
        
        # Создаем услуги
        self.stdout.write('Creating services...')
        
        # Услуги красоты
        Service.objects.create(
            name='Маникюр',
            description='Классический маникюр с покрытием',
            price=1500,
            duration=60,
            specialist=beauty_specialist,
            category=beauty_category
        )
        Service.objects.create(
            name='Массаж лица',
            description='Омолаживающий массаж лица',
            price=2000,
            duration=45,
            specialist=beauty_specialist,
            category=beauty_category
        )
        
        # Услуги здоровья
        Service.objects.create(
            name='Консультация терапевта',
            description='Первичный прием терапевта',
            price=2000,
            duration=30,
            specialist=health_specialist,
            category=health_category
        )
        Service.objects.create(
            name='Измерение давления',
            description='Измерение артериального давления',
            price=500,
            duration=15,
            specialist=health_specialist,
            category=health_category
        )
        
        # Услуги фитнеса
        Service.objects.create(
            name='Персональная тренировка',
            description='Индивидуальное занятие с тренером',
            price=2500,
            duration=60,
            specialist=fitness_specialist,
            category=fitness_category
        )
        Service.objects.create(
            name='Составление программы тренировок',
            description='Разработка индивидуальной программы',
            price=5000,
            duration=90,
            specialist=fitness_specialist,
            category=fitness_category
        )
        
        # Создаем клиентов
        self.stdout.write('Creating clients...')
        
        client1_user = User.objects.create_user(
            username='client1',
            email='client1@example.com',
            password='password',
            first_name='Мария',
            last_name='Клиентова'
        )
        client1 = Client.objects.create(
            user=client1_user,
            name='Мария Клиентова',
            phone='+79123456789',
            email='client1@example.com',
            city='Казань'
        )
        
        client2_user = User.objects.create_user(
            username='client2',
            email='client2@example.com',
            password='password',
            first_name='Алексей',
            last_name='Пользователев'
        )
        client2 = Client.objects.create(
            user=client2_user,
            name='Алексей Пользователев',
            phone='+79234567890',
            email='client2@example.com',
            city='Москва'
        )
        
        self.stdout.write(self.style.SUCCESS('Test data created successfully!')) 
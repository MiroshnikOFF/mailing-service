from django.core.management import BaseCommand
from django.contrib.auth.models import Group, Permission


class Command(BaseCommand):

    def handle(self, *args, **options):

        user_permissions = [
            Permission.objects.get(name='Can add Клиент'),
            Permission.objects.get(name='Can change Клиент'),
            Permission.objects.get(name='Can delete Клиент'),
            Permission.objects.get(name='Can view Клиент'),
            Permission.objects.get(name='Can add Сообщение'),
            Permission.objects.get(name='Can change Сообщение'),
            Permission.objects.get(name='Can delete Сообщение'),
            Permission.objects.get(name='Can view Сообщение'),
            Permission.objects.get(name='Can add Рассылка'),
            Permission.objects.get(name='Can change Рассылка'),
            Permission.objects.get(name='Can delete Рассылка'),
            Permission.objects.get(name='Can view Рассылка'),
            Permission.objects.get(name='Can active Рассылка'),
        ]

        manager_permissions = [
            Permission.objects.get(name='Can view Рассылка'),
            Permission.objects.get(name='Can view Пользователь'),
            Permission.objects.get(name='Can active user'),
            Permission.objects.get(name='Can active Рассылка'),
        ]
        group_users, users_created = Group.objects.get_or_create(name='users')
        group_managers, managers_created = Group.objects.get_or_create(name='managers')
        for perm in user_permissions:
            group_users.permissions.add(perm)
        for perm in manager_permissions:
            group_managers.permissions.add(perm)

        if users_created:
            print(f'Создана группа {group_users}')
        else:
            print(f'Группа {group_users} уже существует')
        if managers_created:
            print(f'Создана группа {group_managers}')
        else:
            print(f'Группа {group_managers} уже существует')





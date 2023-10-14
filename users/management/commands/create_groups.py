from django.core.management import BaseCommand
from django.contrib.auth.models import Group, Permission


class Command(BaseCommand):
    """Команда создает группы users и managers с необходимыми разрешениями"""

    def handle(self, *args, **options):

        user_permissions = Permission.objects.filter(content_type__model__in=['customer', 'message', 'mailing'])
        manager_permissions = [
            Permission.objects.get(name='Can view Рассылка'),
            Permission.objects.get(name='Can view Пользователь'),
            Permission.objects.get(name='Can active Пользователь'),
            Permission.objects.get(name='Can active Рассылка'),
        ]
        group_users, users_created = Group.objects.get_or_create(name='users')
        group_managers, managers_created = Group.objects.get_or_create(name='managers')

        if users_created:
            for perm in user_permissions:
                group_users.permissions.add(perm)
            print(f'Создана группа {group_users}')
        else:
            print(f'Группа {group_users} уже существует')
        if managers_created:
            for perm in manager_permissions:
                group_managers.permissions.add(perm)
            print(f'Создана группа {group_managers}')
        else:
            print(f'Группа {group_managers} уже существует')





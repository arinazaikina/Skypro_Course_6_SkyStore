from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Create moderator group and permissions'

    def handle(self, *args, **options):
        Group.objects.get_or_create(name='Модераторы')
        self.stdout.write(self.style.SUCCESS('Moderators group was created successfully.'))
        Group.objects.get_or_create(name='Контент менеджеры')
        self.stdout.write(self.style.SUCCESS('Content managers group was created successfully.'))

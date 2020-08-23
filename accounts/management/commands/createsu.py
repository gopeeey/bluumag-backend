from django.core.management.base import BaseCommand
from accounts.models import MyUser
import os


class Command(BaseCommand):

    def handle(self, *args, **options):
        if not MyUser.objects.filter(email=os.environ['SU_EMAIL']).exists():
            MyUser.objects.create_superuser(
                email=os.environ['SU_EMAIL'], password=os.environ['SU_PASSWORD'], is_staff=True, is_superuser=True)

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
import os

User = get_user_model()

class Command(BaseCommand):
    def handle(self, *args, **options):
        username = os.environ.get("ADMIN_USERNAME", "Nitish")
        email = os.environ.get("ADMIN_EMAIL", "girinitishkumar11@gmail.com")
        password = os.environ.get("ADMIN_PASSWORD", "Nitish_135")

        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(username=username, email=email, password=password)
            self.stdout.write(self.style.SUCCESS(f"Superuser '{username}' created."))
        else:
            self.stdout.write("Superuser already exists.")
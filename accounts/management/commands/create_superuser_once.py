from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.db import connection, transaction
import os

class Command(BaseCommand):
    help = "Create a superuser once, create groups, and set DB role privileges (race-safe)"

    def handle(self, *args, **kwargs):
        User = get_user_model()

        username = os.getenv("DJANGO_SUPERUSER_USERNAME")
        email = os.getenv("DJANGO_SUPERUSER_EMAIL")
        password = os.getenv("DJANGO_SUPERUSER_PASSWORD")

        if not username or not password:
            self.stdout.write(self.style.ERROR("USER OR PASSWORD NOT FOUND"))
            return

        # 🔐 Start atomic transaction
        with transaction.atomic():

            # 🔐 Advisory lock (prevents concurrent execution)
            with connection.cursor() as cursor:
                cursor.execute("SELECT pg_advisory_xact_lock(987654321);")

            # 1️⃣ Create superuser if not exists
            if not User.objects.filter(username=username).exists():
                User.objects.create_superuser(
                    username=username,
                    email=email,
                    password=password,
                )
                self.stdout.write(self.style.SUCCESS(f"Superuser '{username}' created"))
            else:
                self.stdout.write("Superuser already exists")

            # 2️⃣ Create groups (idempotent)
            Group.objects.get_or_create(name="Admin")
            Group.objects.get_or_create(name="Analyst")
            self.stdout.write(self.style.SUCCESS("Groups ensured: Admin, Analyst"))

            # 3️⃣ Execute raw SQL to set role parameters
            sql_commands = [
                f"ALTER ROLE {username} SET client_encoding TO 'utf8';",
                f"ALTER ROLE {username} SET default_transaction_isolation TO 'read committed';",
                f"ALTER ROLE {username} SET timezone TO 'UTC';",
                f'GRANT ALL PRIVILEGES ON DATABASE "threat-monitoring-db" TO {username};'
            ]

            try:
                with connection.cursor() as cursor:
                    for sql in sql_commands:
                        cursor.execute(sql)
                        self.stdout.write(self.style.SUCCESS(f"Executed: {sql}"))
            except Exception as e:
                self.stdout.write(
                    self.style.WARNING(f"Could not execute SQL commands: {e}")
                )

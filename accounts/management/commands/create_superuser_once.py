from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.db import connection, transaction
from django.conf import settings
import os
import dj_database_url


class Command(BaseCommand):
    help = "Create superuser, default groups, and ensure DB role settings safely (idempotent)"

    def handle(self, *args, **kwargs):
        User = get_user_model()

        username = os.getenv("DJANGO_SUPERUSER_USERNAME")
        email = os.getenv("DJANGO_SUPERUSER_EMAIL")
        password = os.getenv("DJANGO_SUPERUSER_PASSWORD")

        if not username or not password:
            self.stdout.write(
                self.style.ERROR("DJANGO_SUPERUSER_USERNAME or PASSWORD not found")
            )
            return

        # 🔒 Prevent race conditions across multiple containers
        with transaction.atomic():
            with connection.cursor() as cursor:
                cursor.execute("SELECT pg_advisory_xact_lock(987654321);")

            # 1️⃣ Create superuser (idempotent)
            user, created = User.objects.get_or_create(
                username=username,
                defaults={
                    "email": email,
                    "is_staff": True,
                    "is_superuser": True,
                },
            )

            if created:
                user.set_password(password)
                user.save()
                self.stdout.write(
                    self.style.SUCCESS(f"Superuser '{username}' created")
                )
            else:
                self.stdout.write("Superuser already exists")

            # 2️⃣ Create default groups (idempotent)
            Group.objects.get_or_create(name="Admin")
            Group.objects.get_or_create(name="Analyst")

            self.stdout.write(
                self.style.SUCCESS("Groups ensured: Admin, Analyst")
            )

        # 3️⃣ Database role configuration (OUTSIDE atomic block)
        try:
            db_config = dj_database_url.parse(settings.DATABASE_URL)
            db_user = db_config["USER"]
            db_name = db_config["NAME"]

            sql_commands = [
                f"ALTER ROLE {db_user} SET client_encoding TO 'utf8';",
                f"ALTER ROLE {db_user} SET default_transaction_isolation TO 'read committed';",
                f"ALTER ROLE {db_user} SET timezone TO 'UTC';",
                f'GRANT ALL PRIVILEGES ON DATABASE "{db_name}" TO {db_user};',
            ]

            with connection.cursor() as cursor:
                for sql in sql_commands:
                    cursor.execute(sql)

            self.stdout.write(
                self.style.SUCCESS("Database role settings ensured")
            )

        except Exception as e:
            # SQL failure should NEVER block deploy
            self.stdout.write(
                self.style.WARNING(
                    f"Database role setup skipped: {e}"
                )
            )

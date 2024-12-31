from django.core.management.base import BaseCommand

from ...models import Users


class Command(BaseCommand):
    help = 'Creates admin user'

    def handle(self, *args, **options):
        Users.objects.get_or_create(
            login='admin',
            password='admin'
        )
        self.stdout.write(self.style.SUCCESS('Admin user created successfully'))
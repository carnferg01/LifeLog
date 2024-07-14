
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand, CommandError
from LifeLog import Injury

class Command(BaseCommand):
    help = 'Create groups and assign permissions for Athletes and Coaches'

    def handle(self, *args, **kwargs):
        # Create Athletes group
        athletes_group, created = Group.objects.get_or_create(name='Athletes')
        if created:
            self.stdout.write(self.style.SUCCESS('Athletes group created'))
        else:
            self.stdout.write(self.style.WARNING('Athletes group already exists'))

        # Create Coaches group
        coaches_group, created = Group.objects.get_or_create(name='Coaches')
        if created:
            self.stdout.write(self.style.SUCCESS('Coaches group created'))
        else:
            self.stdout.write(self.style.WARNING('Coaches group already exists'))


        # Define the models to assign permissions for
        models = [Activity, Injury, Illness, Gear, Height, Weight]

        # Assign permissions to Athletes group for each model
        for model in models:
            content_type = ContentType.objects.get_for_model(model)
            permissions = Permission.objects.filter(content_type=content_type, codename__in=[
                f'add_{model._meta.model_name}', f'change_{model._meta.model_name}', f'delete_{model._meta.model_name}', f'view_{model._meta.model_name}'
            ])
            athletes_group.permissions.add(*permissions)
            self.stdout.write(self.style.SUCCESS(f'Permissions set for Athletes group for {model._meta.model_name}'))

        # Assign view permission to Coaches group for each model
        for model in models:
            content_type = ContentType.objects.get_for_model(model)
            view_permission = Permission.objects.get(content_type=content_type, codename=f'view_{model._meta.model_name}')
            coaches_group.permissions.add(view_permission)
            self.stdout.write(self.style.SUCCESS(f'View permission set for Coaches group for {model._meta.model_name}'))

        self.stdout.write(self.style.SUCCESS('Permissions successfully set for Athletes and Coaches groups'))

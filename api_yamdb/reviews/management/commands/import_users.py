import csv

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

User = get_user_model()


class Command(BaseCommand):
    help = 'Import users from csv file into database'

    def add_arguments(self, parser):
        parser.add_argument('csv_file_path', type=str, help='CSV file path')

    def handle(self, *args, **options):
        csv_file_path = options['csv_file_path']

        with open(csv_file_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                User.objects.create(
                    id=int(row['id']),
                    username=row['username'],
                    email=row['email'],
                    role=row['role'],
                    bio=row['bio'],
                    first_name=row['first_name'],
                    last_name=row['last_name'],
                )

        self.stdout.write(self.style.SUCCESS('Пользователи успешно'
                                             ' импортированы.'))

import csv

from django.core.management.base import BaseCommand

from reviews.models import Category, Title


class Command(BaseCommand):
    help = 'Import titles from csv file into database'

    def add_arguments(self, parser):
        parser.add_argument('csv_file_path', type=str, help='CSV file path')

    def handle(self, *args, **options):
        csv_file_path = options['csv_file_path']

        with open(csv_file_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                Title.objects.create(
                    id=int(row['id']),
                    name=row['name'],
                    year=row['year'],
                    category=Category.objects.get(id=row['category']),
                )

        self.stdout.write(self.style.SUCCESS('Произведения успешно'
                                             ' импортированы.'))

import csv

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from reviews.models import Review, Title

User = get_user_model()


class Command(BaseCommand):
    help = 'Import review from csv file into database'

    def add_arguments(self, parser):
        parser.add_argument('csv_file_path', type=str, help='CSV file path')

    def handle(self, *args, **options):
        csv_file_path = options['csv_file_path']

        with open(csv_file_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                Review.objects.create(
                    id=int(row['id']),
                    title=Title.objects.get(id=row['title_id']),
                    text=row['text'],
                    author=User.objects.get(id=row['author']),
                    score=row['score'],
                    pub_date=row['pub_date'],
                )

        self.stdout.write(self.style.SUCCESS('Отзывы успешно импортированы.'))

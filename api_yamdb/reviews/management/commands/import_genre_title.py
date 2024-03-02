import csv

from django.core.management.base import BaseCommand

from reviews.models import GenreTitle


class Command(BaseCommand):
    help = 'Import genre_title from csv file into database'

    def add_arguments(self, parser):
        parser.add_argument('csv_file_path', type=str, help='CSV file path')

    def handle(self, *args, **options):
        csv_file_path = options['csv_file_path']

        with open(csv_file_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                GenreTitle.objects.create(
                    id=int(row['id']),
                    title_id=row['title_id'],
                    genre_id=row['genre_id'],)

        self.stdout.write(self.style.SUCCESS('Связи жанров и произведений'
                                             ' успешно импортированы.'))

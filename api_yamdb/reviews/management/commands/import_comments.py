import csv

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from reviews.models import Comment, Review

User = get_user_model()


class Command(BaseCommand):
    help = 'Import comments from csv file into database'

    def add_arguments(self, parser):
        parser.add_argument('csv_file_path', type=str, help='CSV file path')

    def handle(self, *args, **options):
        csv_file_path = options['csv_file_path']

        with open(csv_file_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                Comment.objects.create(
                    id=int(row['id']),
                    review=Review.objects.get(id=row['review_id']),
                    text=row['text'],
                    author=User.objects.get(id=row['author']),
                    pub_date=row['pub_date'],
                )
        self.stdout.write(self.style.SUCCESS('Комментари к отзывам '
                                             'успешно импортированы.'))

import csv
import io

from django.apps import apps
from django.core.management.base import BaseCommand

PATHS_MODELS = {
    'static/data/category.csv': 'Category',
    'static/data/genre.csv': 'Genre',
    'static/data/titles.csv': 'Title',
    'static/data/users.csv': 'User',
    'static/data/genre_title.csv': 'GenreTitle',
    'static/data/review.csv': 'Review',
    'static/data/comments.csv': 'Comment'
}


class Command(BaseCommand):
    help = 'Imports csv data into database'

    def handle(self, *args, **options):
        for path, model in PATHS_MODELS.items():
            if model != 'User':
                _model = apps.get_model('reviews', model)
            else:
                _model = apps.get_model('users', model)
            with io.open(path, mode='r', encoding='utf-8') as csv_file:
                reader = csv.reader(csv_file, delimiter=',')
                header = next(reader)
                for row in reader:
                    _object_dict = {
                        key: value for key, value in zip(header, row)
                    }
                    _model.objects.create(**_object_dict)

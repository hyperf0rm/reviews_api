import csv
from django.core.management.base import BaseCommand
from django.apps import apps


class Command(BaseCommand):
    help = 'Imports category.csv data into database'

    def add_arguments(self, parser):
        parser.add_argument('--path', type=str, help='file path')
        parser.add_argument('--model_name', type=str, help='model name')
        # parser.add_argument('--app_name', type=str,
        #                    help='django app name that the model is connected to')

    def handle(self, *args, **options):
        file_path = options['path']
        _model = apps.get_model(['reviews'], options['model_name'])
        with open(file_path, 'r') as csv_file:
            reader = csv.reader(csv_file, delimiter=',')
            header = next(reader)
            for row in header:
                _object_dict = {key: value for key, value in zip(header, row)}
                _model.objects.create(**_object_dict)

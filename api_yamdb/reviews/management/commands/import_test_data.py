import subprocess

from django.core.management.base import BaseCommand

DATA = {
    "import_category": "static/data/category.csv",
    "import_genre": "static/data/genre.csv",
    "import_users": "static/data/users.csv",
    "import_titles": "static/data/titles.csv",
    "import_genre_title": "static/data/genre_title.csv",
    "import_review": "static/data/review.csv",
    "import_comments": "static/data/comments.csv",
}


class Command(BaseCommand):
    help = 'Import test data from csv file into database'

    def handle(self, *args, **options):
        for name_command, file_path in DATA.items():
            subprocess.run(["py", "manage.py", name_command, file_path])

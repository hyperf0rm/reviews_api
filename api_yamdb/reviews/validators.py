from django.core.exceptions import ValidationError
import datetime as dt


def validate_year(value):
    if value > dt.date.today().year:
        raise ValidationError(
            'The year cannot be greater than the current one.'
        )

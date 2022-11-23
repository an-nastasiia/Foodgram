import sys

from django.core.management.base import BaseCommand, CommandError

from ._read_csv import read_csv


class Command(BaseCommand):
    '''Perform data load from CSV file into database via manage.py command.'''

    def handle(self, *args, **options):
        try:
            read_csv()
            sys.stdout.write('Data uploaded successfully')
            sys.stdout.write('')
        except FileNotFoundError as error:
            raise CommandError(error)

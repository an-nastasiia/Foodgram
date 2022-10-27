import sys
from django.core.management.base import BaseCommand, CommandError

from ._read_csv import read_csv


class Command(BaseCommand):
    '''Загрузка данных из csv-файла в базу данных через команду manage.py.'''

    def handle(self, *args, **options):
        try:
            read_csv()
            sys.stdout.write('Данные успешно загружены')
        except FileNotFoundError as error:
            raise CommandError(error)

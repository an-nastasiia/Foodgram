import os
import sys

import csv
import psycopg2


def read_csv():
    '''Загрузка данных из csv-файла в базу данных PostgreSQL.'''
    connection = psycopg2.connect(database="postgres", user='postgres',
                                  password='410861342', host='db',
                                  port='5432')
    connection.autocommit = True
    cur = connection.cursor()

    with open(os.path.abspath('data/ingredients.csv'), 'r', newline='',
              encoding='utf-8') as csv_file:
        reader = csv.reader(csv_file, delimiter=',')

        try:
            for row in reader:
                cur.execute('''INSERT INTO recipes_ingredient
                            (name,measurement_unit)
                            VALUES (%s, %s)
                            ''',
                            (str(row[0]),
                             str(row[1])))
        except Exception() as error:
            sys.stdout.write(f'Не удалось загрузить данные: {error}.')

    connection.commit()
    connection.close()

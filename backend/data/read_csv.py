import csv
import psycopg2
import os

conn = psycopg2.connect(database="postgres",
                        user='postgres', password='410861342', 
                        host='db', port='5432'
)

conn.autocommit = True
cur = conn.cursor()


with open('./ingredients.csv', 'r', newline='', encoding='utf-8') as csv_file:
    reader = csv.reader(csv_file, delimiter=',')

    for row in reader:
        try:
            cur.execute('''
                    INSERT INTO recipes_ingredient
                    (name,measurement_unit)
                    VALUES (?,?)''',
                        (str(row[0]),
                         str(row[1])))
        except sqlite3.IntegrityError:
            print(f'Ingredient {str(row[1])} already exists.')

con.commit()
con.close()

import csv
import sqlite3


con = sqlite3.connect('C://Dev/foodgram-project-react/backend/foodgram/db.sqlite3')
cur = con.cursor()


with open('C://Dev/foodgram-project-react/data/ingredients.csv', 'r', newline='', encoding='utf-8') as csv_file:
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

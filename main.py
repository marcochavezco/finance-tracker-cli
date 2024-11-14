import pandas as pd
import csv
from data_entry import get_date, get_amount, get_category, get_description

class CSV:
    CSV_FILE = 'finance_data.csv'
    COLUMNS = ['date', 'amount', 'category', 'description']

    @classmethod
    def initalize_csv(cls):
        try:
            pd.read_csv(cls.CSV_FILE)
        except FileNotFoundError:
            df = pd.DataFrame(columns=cls.COLUMNS)
            df.to_csv(cls.CSV_FILE, index=False)

    @classmethod
    def add_entry(cls, date, amount, category, description):
        new_entry = {
            'date': date,
            'amount': amount,
            'category': category,
            'description': description,
        }

        with open(cls.CSV_FILE, 'a', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=cls.COLUMNS)
            writer.writerow(new_entry)
            print('Entry added!')

def add():
    CSV.initalize_csv()
    date = get_date("Enter the transaction date (dd-mm-yyyy). Leave empty to use today's date: ", allow_default=True) 
    amount = get_amount()
    category = get_category()
    description= get_description()
    CSV.add_entry(date, amount, category, description)

add()
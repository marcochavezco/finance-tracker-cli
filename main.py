import pandas as pd

class CSV:
    CSV_FILE = 'finance_data.csv'

    @classmethod
    def initalize_csv(cls):
        try:
            pd.read_csv(cls.CSV_FILE)
        except FileNotFoundError:
            df = pd.DataFrame(columns=['date', 'amount', 'category', 'description'])
            df.to_csv(cls.CSV_FILE, index=False)

CSV.initalize_csv()

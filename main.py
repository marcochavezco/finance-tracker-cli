import pandas as pd
import csv
from datetime import datetime
from data_entry import get_date, get_amount, get_category, get_description
import matplotlib.pyplot as plt

class CSV:
    CSV_FILE = 'finance_data.csv'
    COLUMNS = ['date', 'amount', 'category', 'description']
    DATE_FORMAT = '%d-%m-%Y'

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

    @classmethod
    def get_transactions(cls, start_date, end_date):
        df = pd.read_csv(cls.CSV_FILE)
        df['date'] = pd.to_datetime(df['date'], format=CSV.DATE_FORMAT)
        start_date = datetime.strptime(start_date, CSV.DATE_FORMAT)
        end_date = datetime.strptime(end_date, CSV.DATE_FORMAT)

        mask = (df['date'] >= start_date) & (df['date'] <= end_date)
        filtered_df = df.loc[mask]

        if filtered_df.empty:
            print("No transactions found in the given data range")
            return filtered_df

        print(f'Transactions from {start_date.strftime(CSV.DATE_FORMAT)} to {end_date.strftime(CSV.DATE_FORMAT)}')
        print(filtered_df.to_string(
            index=False, formatters={'date': lambda x: x.strftime(CSV.DATE_FORMAT)}
        ))

        total_income = filtered_df[filtered_df['category'] == 'I']['amount'].sum()
        total_expense = filtered_df[filtered_df['category'] == 'E']['amount'].sum()

        print('\nSummany:')
        print(f'Total Incomes: ${total_income:.2f}')
        print(f'Total Expenses: ${total_expense:.2f}')
        print(f'Net Savings: ${(total_income - total_expense):.2f}')

        return filtered_df

def add():
    CSV.initalize_csv()
    date = get_date("Enter the transaction date (dd-mm-yyyy). Leave empty to use today's date: ", allow_default=True) 
    amount = get_amount()
    category = get_category()
    description= get_description()
    CSV.add_entry(date, amount, category, description)

def plot_transactions(df):
    df.set_index('date', inplace=True)

    income_df = (
        df[df['category'] == 'I'].resample('D').sum().reindex(df.index, fill_value=0)
    )

    expense_df = (
        df[df['category'] == 'E'].resample('D').sum().reindex(df.index, fill_value=0)
    )

    plt.figure(figsize=(15,5))
    plt.plot(income_df.index, income_df['amount'], label='Income', color='g')
    plt.plot(expense_df.index, expense_df['amount'], label='Expense', color='r')
    plt.xlabel('Date')
    plt.ylabel('Amount')
    plt.title('Income and Expenses Over Time')
    plt.legend()
    plt.grid(True)
    plt.show()

def main():
    while True:
        print('\n1. Add a new transaction')
        print('2. View transactions and summary within a date range')
        print('3. Exit')
        option = input('Enter option number (1-3): ')

        match option:
            case '1':
                add()
            case '2':
                start_date = get_date('Enter the start date (dd-mm-yyyy): ')
                end_date = get_date('Enter the end date (dd-mm-yyyy): ')
                df = CSV.get_transactions(start_date, end_date)
                if input('Do you want to plot the results? (y/n)').lower() == 'y':
                    plot_transactions(df)
            case '3':
                print('Exiting...')
                break
            case _:
                print('Invalid option, try again.') 
    

if __name__ == '__main__':
    main()
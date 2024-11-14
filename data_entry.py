from datetime import datetime

DATE_FORMAT = '%d-%m-%Y'
CATEGORIES = {'I': 'Income', 'E': 'Expense'}


def get_date(prompt, allow_default=False):
    date_str = input(prompt);
    if allow_default and not date_str:
        return datetime.today().strftime(DATE_FORMAT)
    
    try:
        valid_date = datetime.strptime(date_str, DATE_FORMAT)
        return valid_date.strftime(DATE_FORMAT)
    except:
        print('Invalid date format. Please enter the date in dd-mm-yyyy format')
        get_date(prompt, allow_default)

def get_amount():
    try:
        amount = float(input('Enter amount: '))
        if amount <= 0:
            raise ValueError('Invalid amount. The amount must be greater positive or greater than 0. Please try again')

        return amount
    
    except ValueError as e:
        print(e)
        return get_amount()

def get_category():
    category = input("Enter amount's category (I: Income, E: Expense): ").upper()

    if category in CATEGORIES:
        return category

    print('Enter a valid category, try again')
    get_category()

def get_description():
    return input('Enter description (optional): ')
    
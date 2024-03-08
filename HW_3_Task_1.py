# У вимогах до боту для ДЗ№3 для команд інтерфейсу користувача не використовуюються ці функції із ДЗ№2, тому я іх закоментував.
# Якщо вони всежтаки потрібні, то розкоментуйте їх будь ласка, вони готові до використання.         
from datetime import datetime, timedelta
from collections import UserDict, defaultdict

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    pass

class Phone(Field):
    def __init__(self, value):
        super().__init__(value)
        if not self.validate():
            raise ValueError("Phone number must be 10 digits long")
    
    def validate(self):
        return len(self.value) == 10 and self.value.isdigit()

class Birthday(Field):
    def __init__(self, value):
        super().__init__(value)
        if not self.validate():
            raise ValueError("Birthday must be in DD.MM.YYYY format")

    def validate(self):
        try:
            datetime.strptime(self.value, "%d.%m.%Y")
            return True
        except ValueError:
            return False

class Record:
    def __init__(self, name, birthday=None):
        self.name = Name(name)
        self.phones = []
        self.birthday = None if birthday is None else Birthday(birthday)

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

# У вимогах до боту для ДЗ№3 для команд інтерфейсу користувача не використовуюються ці функції із ДЗ№2, тому я іх закоментував.
# Якщо вони всежтаки потрібні, то розкоментуйте їх будь ласка, вони готові до використання.         
    # def remove_phone(self, phone): 
    #     self.phones.remove(phone)

    # def edit_phone(self, old_phone, new_phone):
    #     found_phone = self.find_phone(old_phone)
    #     if found_phone:
    #         found_phone.value = new_phone

    # def find_phone(self, phone):
    #     for p in self.phones:
    #         if p.value == phone:
    #             return p

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def show_birthday(self):
        if self.birthday:
            return self.birthday.value
        else:
            return "Birthday not set."

    def __str__(self):
        phones_str = '; '.join(p.value for p in self.phones)
        birthday_str = f", birthday: {self.birthday.value}" if self.birthday else ""
        return f"Contact name: {self.name.value}, phone: {phones_str}{birthday_str}"

class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        if name in self.data:
            del self.data[name]

    def get_birthdays_per_week(self):
        today = datetime.today().date()
        birthdays = defaultdict(list)
        for name, record in self.data.items():
            if record.birthday:  
                birthday_date = datetime.strptime(record.birthday.value, "%d.%m.%Y").date()
                birthday_this_year = birthday_date.replace(year=today.year)

                if birthday_this_year < today:
                    birthday_this_year = birthday_this_year.replace(year=today.year + 1)

                delta_days = (birthday_this_year - today).days

                if 0 <= delta_days < 7:
                    weekday = (today + timedelta(days=delta_days)).strftime("%A")

                    if weekday in ["Saturday", "Sunday"]:
                        weekday = "Monday"

                    birthdays[weekday].append(name)

        return birthdays

def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            return str(e)
        except KeyError:
            return "Contact not found."
        except IndexError:
            return "Please provide enough information."
    return inner

@input_error
def add_contact(args, book):
    name, phone = args
    if name in book:
        return "Contact already exists. Use change to update the phone number."
    record = Record(name)
    record.add_phone(phone)
    book.add_record(record)
    return "Contact added."

@input_error
def change_contact(args, book):
    name, new_phone = args
    record = book.find(name)
    if record:
        record.phones = []  
        record.add_phone(new_phone)
        return "Contact updated."
    else:
        return "Contact not found."

@input_error
def show_phone(args, book):
    name = args[0]
    record = book.find(name)
    if record:
        return ', '.join(phone.value for phone in record.phones)
    else:
        raise KeyError

@input_error
def add_birthday(args, book):
    name, birthday = args
    record = book.find(name)
    if record:
        record.add_birthday(birthday)
        return "Birthday added."
    else:
        return "Contact not found."

@input_error
def show_birthday(args, book):
    name = args[0]
    record = book.find(name)
    if record and record.birthday:
        return record.show_birthday()
    else:
        return "Birthday not set or contact not found."

def show_all(book):
    if book:
        return '\n'.join(str(record) for record in book.values())
    else:
        return "No contacts saved."

def show_birthdays(book):
    birthdays = book.get_birthdays_per_week()
    if birthdays:
        messages = [f"{weekday}: {', '.join(names)}" for weekday, names in birthdays.items()]
        return '\n'.join(messages)
    else:
        return "No birthdays this week."

def parse_input(user_input):
    command, *args = user_input.split()
    command = command.strip().lower()
    return command, args

def main():
    book = AddressBook()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, args = parse_input(user_input)

        if command == "close" or command == "exit":
            print("Good bye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(add_contact(args, book))
        elif command == "change":
            print(change_contact(args, book))
        elif command == "phone":
            print(show_phone(args, book))
        elif command == "all":
            print(show_all(book))
        elif command == "add-birthday":
            print(add_birthday(args, book))
        elif command == "show-birthday":
            print(show_birthday(args, book))
        elif command == "birthdays":
            print(show_birthdays(book))
        else:
            print("Invalid command.")

if __name__ == "__main__":
    main()
class Account:
    def __init__(self, account_id, customer_id, account_number, balance):
        self.account_id = account_id
        self.customer_id = customer_id
        self.account_number = account_number
        self.balance = balance
        self.transactions = []  # List to track transactions

    def deposit(self, amount, timestamp):
        self.balance += amount
        self.transactions.append({'type': 'deposit', 'amount': amount, 'timestamp': timestamp})

    def withdraw(self, amount, timestamp):
        if self.balance >= amount:
            self.balance -= amount
            self.transactions.append({'type': 'withdrawal', 'amount': amount, 'timestamp': timestamp})
        else:
            raise ValueError("Insufficient balance")

    def get_balance(self):
        return self.balance


class Customer:
    def __init__(self, customer_id, name, email, phone_number):
        self.customer_id = customer_id
        self.name = name
        self.email = email
        self.phone_number = phone_number

from models import Account


class CreateAccountUseCase:
    def create_account(self, customer):
        customer_id = customer.customer_id
        # Generate account_number
        account_number = "PDAX" + str(customer_id)
        return Account(customer_id, customer_id, account_number, 0)


class TransactionUseCase:
    def __init__(self, account_repo):
        self.account_repo = account_repo

    def make_transaction(self, account_id, amount, transaction_type, timestamp):
        account = self.account_repo.find_account_by_id(account_id)
        if transaction_type == 'deposit':
            account.deposit(amount, timestamp)
        elif transaction_type == 'withdraw':
            account.withdraw(amount, timestamp)
        else:
            raise ValueError("Invalid transaction type")


class AccountStatementUseCase:
    def __init__(self, account_repo):
        self.account_repo = account_repo

    def generate_account_statement(self, account_id):
        account = self.account_repo.find_account_by_id(account_id)
        transactions = account.transactions 

        statement = "Account Statement for Account Number: {}\n".format(account.account_number)
        statement += "Balance: {}\n".format(account.get_balance())

        statement += "Transaction History:\n"
        for transaction in transactions:
            statement += "Date: {}\n".format(transaction['timestamp'])  
            statement += "Amount: {}\n".format(transaction['amount'])  
            statement += "Type: {}\n".format(transaction['type'])
            statement += "\n"

        return statement



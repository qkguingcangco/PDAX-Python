import unittest
from models import Account, Customer
from repositories import AccountRepository
from use_cases import CreateAccountUseCase, TransactionUseCase, AccountStatementUseCase
import datetime

class TestBankingSystem(unittest.TestCase):
    def setUp(self):
        # Initialize repository
        self.account_repo = AccountRepository()

        # Create a test customer
        self.customer = Customer(1, "John Doe", "john@example.com", "1234567890")

        # Create a new account
        self.create_account_use_case = CreateAccountUseCase()
        self.new_account = self.create_account_use_case.create_account(
            self.customer.customer_id, self.customer.name, self.customer.email, self.customer.phone_number)
        self.account_repo.save_account(self.new_account)

        self.transaction_use_case = TransactionUseCase(self.account_repo)

        self.account_statement_use_case = AccountStatementUseCase(self.account_repo)

    def test_deposit(self):
        print("========== DEPOSIT TEST ==========")
        print(f"Balance before deposit: {self.new_account.get_balance()}")
        
        timestamp = datetime.datetime.now()
        self.transaction_use_case.make_transaction(
            self.new_account.account_id, 1000, 'deposit', timestamp)
        
        self.assertEqual(self.new_account.get_balance(), 1000)
        print(f"Balance after deposit: {self.new_account.get_balance()}")

    def test_withdraw(self):
        print("========== WITHDRAW TEST ==========")
        print(f"Balance before withdraw: {self.new_account.get_balance()}")
        
        timestamp_deposit = datetime.datetime.now()
        self.transaction_use_case.make_transaction(
            self.new_account.account_id, 1000, 'deposit', timestamp_deposit)
        
        print(f"Balance after deposit: {self.new_account.get_balance()}")

        timestamp_withdraw = datetime.datetime.now()
        self.transaction_use_case.make_transaction(
            self.new_account.account_id, 500, 'withdraw', timestamp_withdraw)

        self.assertEqual(self.new_account.get_balance(), 500)
        print(f"Balance after withdraw: {self.new_account.get_balance()}")

    def test_insufficient_balance_withdraw(self):
        print("========== INSUFFICIENT BALANCE TEST ==========")
        print(f"Balance before test: {self.new_account.get_balance()}")
        
        timestamp = datetime.datetime.now()
        try:
            self.transaction_use_case.make_transaction(
                self.new_account.account_id, 1000, 'withdraw', timestamp)
            print("Unexpected success. Expected ValueError.")
        except ValueError as e:
            print("Expected failure:", str(e))
        print("test_insufficient_balance_withdraw passed.")

    def test_generate_account_statement(self):
        print("========== ACCOUNT STATEMENT TEST ==========")
        
        # Making some transactions for testing purposes
        timestamp_deposit = datetime.datetime.now()
        self.transaction_use_case.make_transaction(
            self.new_account.account_id, 1000, 'deposit', timestamp_deposit)
        print(f"Deposited 1000 at: {timestamp_deposit}")

        timestamp_withdraw = datetime.datetime.now()
        self.transaction_use_case.make_transaction(
            self.new_account.account_id, 500, 'withdraw', timestamp_withdraw)
        print(f"Withdrew 500 at: {timestamp_withdraw}")

        # Generating account statement
        statement = self.account_statement_use_case.generate_account_statement(
            self.new_account.account_id)
        expected_statement = "Account Statement for Account Number: {}\nBalance: {}\n".format(
            self.new_account.account_number, self.new_account.get_balance())

        # Add transaction history to the expected statement
        expected_statement += "Transaction History:\n"
        for transaction in self.new_account.transactions:
            expected_statement += "Date: {}\n".format(transaction['timestamp'])
            expected_statement += "Amount: {}\n".format(transaction['amount'])
            expected_statement += "Type: {}\n".format(transaction['type'])
            expected_statement += "\n"

        
        print(f"Statement:\n{statement}")
        
        # Comparing the generated statement with the expected one
        self.assertEqual(statement, expected_statement)
        print("test_generate_account_statement passed.")

if __name__ == '__main__':
    unittest.main()

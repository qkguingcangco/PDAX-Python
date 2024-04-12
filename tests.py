import unittest
from models import Account, Customer
from repositories import AccountRepository
from use_cases import CreateAccountUseCase, TransactionUseCase, AccountStatementUseCase


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
        self.transaction_use_case.make_transaction(
            self.new_account.account_id, 1000, 'deposit')
        self.assertEqual(self.new_account.get_balance(), 1000)

    def test_withdraw(self):
        self.transaction_use_case.make_transaction(
            self.new_account.account_id, 1000, 'deposit')
        
        self.transaction_use_case.make_transaction(
            self.new_account.account_id, 500, 'withdraw')

        self.assertEqual(self.new_account.get_balance(), 500)


    def test_insufficient_balance_withdraw(self):
        with self.assertRaises(ValueError):
            self.transaction_use_case.make_transaction(
                self.new_account.account_id, 1000, 'withdraw')

    def test_generate_account_statement(self):
        statement = self.account_statement_use_case.generate_account_statement(
            self.new_account.account_id)
        expected_statement = "Account Statement for Account Number: {}\nBalance: 0\n".format(
            self.new_account.account_number)
        self.assertEqual(statement, expected_statement)


if __name__ == '__main__':
    unittest.main()

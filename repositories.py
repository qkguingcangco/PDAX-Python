class AccountRepository:
    def __init__(self):
        self.accounts = {}

    def save_account(self, account):
        self.accounts[account.account_id] = account

    def find_account_by_id(self, account_id):
        return self.accounts.get(account_id)

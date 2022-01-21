from requests import get
from transaction import Transaction
from transaction_group import TransactionGroup
ACCOUNT_URL = 'https://algoindexer.algoexplorerapi.io/v2/accounts/'

class Wallet:
    def __init__(self, address):
        self.address = address
        self.transactions_cache = []
        self.transaction_group = {}
        self.account_api_url = ACCOUNT_URL + self.address
        print(self.account_api_url)

    def get_address(self):
        return self.address

    def transactions(self):
        if self.transactions_cache:
            return self.transactions_cache
        else:
            return self.get_transactions()

    def get_transactions(self, limit=None):
        response = get(self.account_api_url + '/transactions', params={'limit': limit})
        response_json = response.json()
        self.transactions = []
        
        while 'next-token' in response_json:
            for transaction_json in response_json['transactions']:
                transaction = Transaction(self, transaction_json)
                if 'group' in transaction_json:
                    self.add_to_transaction_group(transaction)
                self.transactions.append(transaction)
            response_json = get(self.account_api_url + '/transactions', params={'next': response_json['next-token'], 'limit': limit}).json()

        return self.transactions

    def add_to_transaction_group(self, transaction):
        if transaction.group_id not in self.transaction_group:
            print(f"New Group {transaction.group_id}")
            self.transaction_group[transaction.group_id] = TransactionGroup(transaction.group_id)
        
        self.transaction_group[transaction.group_id].transactions.append(transaction)
from requests import get
from transaction import transaction_builder
from transaction_group import TransactionGroup
ACCOUNT_URL = 'https://algoindexer.algoexplorerapi.io/v2/accounts/'

class Wallet:
    def __init__(self, address):
        self.address = address
        self.transactions_cache = []
        self.transaction_groups = {}
        self.account_api_url = ACCOUNT_URL + self.address

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
                if 'group' in transaction_json:
                    if transaction_json['group'] not in self.transaction_groups:
                        self.transaction_groups[transaction_json['group']] = TransactionGroup(transaction_json['group'])
                    transaction = transaction_builder(self, transaction_json)
                    self.transaction_groups[transaction.group_id].transactions.append(transaction)
                else:
                    transaction = transaction_builder(self, transaction_json)
                self.transactions.append(transaction)
            response_json = get(self.account_api_url + '/transactions', params={'next': response_json['next-token'], 'limit': limit}).json()

        return self.transactions
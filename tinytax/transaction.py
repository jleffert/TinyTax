from datetime import datetime

class Transaction:
    def __init__(self, wallet, transaction_data):
        self.wallet = wallet
        self.id = transaction_data['id']
        self.sender = transaction_data['sender']
        self.date = str(datetime.fromtimestamp(transaction_data['round-time']))
        if 'group' in transaction_data:
            self.group_id = transaction_data['group']
        
        if transaction_data['sender'] == self.wallet.address:
            self.fee = transaction_data['fee']
        else:
            # No fees when user is not sender
            self.fee = 0


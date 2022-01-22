from datetime import datetime
from contracts import yieldlyDB, algofiDB

TRANSACTION_TYPES = {
    'pay' : 'ALGO Transaction',
    'axfer' : 'ASA Transaction',
    'appl' : 'Application Transaction'
}

class Transaction:
    def __init__(self, wallet, data):
        self.wallet = wallet
        self.id = data['id']
        self.sender = data['sender']
        self.date = str(datetime.fromtimestamp(data['round-time']))
        self.platform = None

        if 'group' in data:
            self.group_id = data['group']
        else:
            self.group_id = None
        
        if data['sender'] == self.wallet.address:
            self.fee = data['fee']
        else:
            # No fees when user is not sender
            self.fee = 0
        
    def readable_transaction_type(self):
        if self.transaction_type in TRANSACTION_TYPES:
            return TRANSACTION_TYPES[self.transaction_type]
        else:
            return 'Unknown'

    def set_platform(self):
        if self.sender in yieldlyDB or self.receiver in yieldlyDB:
            self.platform = 'Yieldly'
        elif self.sender in algofiDB or self.receiver in algofiDB:
            self.platform = 'Algofi'
        else:
            self.platform = None
        # TODO: Detect Tinyman

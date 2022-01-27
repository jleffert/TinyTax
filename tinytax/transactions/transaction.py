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
        self.out_quantity = ''
        self.out_asset_id = ''
        self.in_quantity = ''
        self.in_asset_id = ''
        self.fee_id = 'ALGO'

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

    def set_rewards(self, data):
        if self.sender == self.wallet.address and data['sender-rewards'] > 0:
            self.rewards = data['sender-rewards']
        elif self.receiver == self.wallet.address and data['receiver-rewards'] > 0:
            self.rewards  = data['receiver-rewards']
        else:
            self.rewards = 0

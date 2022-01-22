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
        if 'group' in data:
            self.group_id = data['group']
        
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

class PaymentTransaction(Transaction):
    def __init__(self, wallet, data):
        super().__init__(wallet, data)
        self.transaction_type = 'pay'
        payment_data = data['payment-transaction']
        self.receiver = payment_data['receiver']
        if payment_data['amount'] != 0: # 0 Transactions are for compounding rewards
            if self.receiver == wallet.address:
                self.type = 'Receive'
                self.receive_quantity = payment_data['amount'] 
                self.receive_asset_id = 'ALGO'
            else:
                self.type = 'Send'
                self.out_quantity = payment_data['amount']
                self.out_asset_id = 'ALGO'
        elif self.sender == wallet.address and self.receiver == wallet.address:
            self.type = 'Staking'
        else:
            self.type = 'Unkown Payment'
        self.set_platform()
    

class AsaTransaction(Transaction):
    def __init__(self, wallet, data):
        super().__init__(wallet, data)
        self.transaction_type = 'axfer'
        self.receiver = data['asset-transfer-transaction']['receiver']
        self.set_platform()

class ApplicationTransaction(Transaction):
    def __init__(self, wallet, data):
        super().__init__(wallet, data)
        self.transaction_type = 'appl'
        self.receiver = data['application-transaction']['application-id']
        self.set_platform()

def transaction_builder(wallet, data):
    match data['tx-type']:
        case 'pay':
            return PaymentTransaction(wallet, data)
        case 'axfer':
            return AsaTransaction(wallet, data)
        case 'appl':
            return ApplicationTransaction(wallet, data)
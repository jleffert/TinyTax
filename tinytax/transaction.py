from datetime import datetime

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
        
        self.transaction_type = data['tx-type']
        self.initalize_amount(data)

    def readable_transaction_type(self):
        if self.transaction_type in TRANSACTION_TYPES:
            return TRANSACTION_TYPES[self.transaction_type]
        else:
            return 'Unknown'

    def initalize_amount(self, data):
        match self.transaction_type:
            case 'pay':
                pass
            case 'axfer':
                pass
            case 'appl':
                pass

class PaymentTransaction(Transaction):
    def __init__(self, wallet, data):
        super().__init__(wallet, data)
        self.transaction_type = 'pay'
        print('pay')

class AsaTransaction(Transaction):
    def __init__(self, wallet, data):
        super().__init__(wallet, data)
        self.transaction_type = 'axfer'
        print('axfer')

class ApplicationTransaction(Transaction):
    def __init__(self, wallet, data):
        super().__init__(wallet, data)
        self.transaction_type = 'appl'
        print('appl')

def transaction_builder(wallet, data):
    match data['tx-type']:
        case 'pay':
            return PaymentTransaction(wallet, data)
        case 'axfer':
            return AsaTransaction(wallet, data)
        case 'appl':
            return ApplicationTransaction(wallet, data)
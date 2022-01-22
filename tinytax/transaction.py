from ctypes import addressof
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
        asset_transfer_data = data['asset-transfer-transaction']
        self.receiver = asset_transfer_data['receiver']
        
        asset_id = str(asset_transfer_data['asset-id'])
        if 'close-to' in asset_transfer_data: # Remove ASA
            self.type = 'Close ASA'
            self.out_asset_id = asset_id
            self.platform = asset_id
        elif self.sender == wallet.address:
            if self.receiver == wallet.address:
                self.type = 'Sign for ASA'
                self.in_asset_id = asset_id
            else:
                self.type = 'Send'
                self.out_quantity = asset_transfer_data['amount']
                self.out_asset_id = asset_id
        elif self.sender is not wallet.address and self.receiver == wallet.address:
            self.type = 'Receive'
            self.in_quantity = asset_transfer_data['amount']
            self.in_asset_id = asset_id
        else:
            self.type = 'Unkown ASA Transaction'

        if self.platform is None:
            self.set_platform()

class ApplicationTransaction(Transaction):
    def __init__(self, wallet, data):
        super().__init__(wallet, data)
        self.transaction_type = 'appl'
        applilcation_transaction_data = data['application-transaction']
        self.receiver = str(applilcation_transaction_data['application-id'])

        if 'application-args' in applilcation_transaction_data:
            app_arguments = applilcation_transaction_data['application-args']
            # First arguement defines Tinyman actions
            if app_arguments != []:
                # First transaction of a group does not contain defining info
                if app_arguments[0] == 'Ym9vdHN0cmFw':
                    wallet.transaction_groups[self.group_id].action = 'Begin pool'
                elif app_arguments[0] == 'c3dhcA==':
                    if app_arguments[1] == 'Zmk=':
                        wallet.transaction_groups[self.group_id].action = 'Sell'
                    elif app_arguments[1] ==  'Zm8=':
                        wallet.transaction_groups[self.group_id].action = 'Buy'
                elif app_arguments[0] == 'bWludA==':
                    wallet.transaction_groups[self.group_id].action = 'Add to pool'
                elif app_arguments[0] == 'YnVybg==':
                    wallet.transaction_groups[self.group_id].action = 'Remove from pool'
                elif app_arguments[0] == 'cmVkZWVt':
                    wallet.transaction_groups[self.group_id].action = 'Redeed Slippage'
                else:
                    wallet.transaction_groups[self.group_id].action = 'Unkown'
            elif applilcation_transaction_data['on-completion'] == 'optin': 
                self.type = 'App opt in'
            else:
                wallet.transaction_groups[self.group_id].action = 'Unkown'

        self.set_platform()

def transaction_builder(wallet, data):
    match data['tx-type']:
        case 'pay':
            return PaymentTransaction(wallet, data)
        case 'axfer':
            return AsaTransaction(wallet, data)
        case 'appl':
            return ApplicationTransaction(wallet, data)
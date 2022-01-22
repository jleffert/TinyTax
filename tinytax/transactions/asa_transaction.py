from transactions.transaction import Transaction

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
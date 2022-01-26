from transactions.transaction import Transaction

class PaymentTransaction(Transaction):
    def __init__(self, wallet, data):
        super().__init__(wallet, data)
        self.transaction_type = 'pay'
        payment_data = data['payment-transaction']
        self.receiver = payment_data['receiver']
        self.set_rewards(data)
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
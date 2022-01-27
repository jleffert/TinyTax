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
                self.in_quantity = float(payment_data['amount']) / 1000000
                self.in_asset_id = 'ALGO'
            else:
                self.type = 'Send'
                self.out_quantity = float(payment_data['amount']) / 1000000
                self.out_asset_id = 'ALGO'
        elif self.sender == wallet.address and self.receiver == wallet.address:
            self.type = 'Staking'
        else:
            self.type = 'Unkown Payment'
        self.set_platform()
        
        if self.fee > 0:
            self.fee = self.fee / 1000000
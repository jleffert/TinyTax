from transactions.transaction import Transaction

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
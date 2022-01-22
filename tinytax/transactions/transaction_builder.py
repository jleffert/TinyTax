from transactions.payment_transaction import PaymentTransaction
from transactions.asa_transaction import AsaTransaction
from transactions.application_transaction import ApplicationTransaction

def transaction_builder(wallet, data):
    match data['tx-type']:
        case 'pay':
            return PaymentTransaction(wallet, data)
        case 'axfer':
            return AsaTransaction(wallet, data)
        case 'appl':
            return ApplicationTransaction(wallet, data)
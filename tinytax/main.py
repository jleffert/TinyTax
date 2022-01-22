from wallet import Wallet

wallet = Wallet(input('Enter Wallet Address: '))
transactions = wallet.get_transactions(50)

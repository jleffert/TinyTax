from contracts import yieldlyDB, algofiDB
from wallet import Wallet

wallet = Wallet(input('Enter Wallet Address: '))
print(wallet.get_address())
transactions = wallet.get_transactions(50)

# wallet = str(input('Paste wallet ID and press Enter: '))
from requests import get
from string import digits
import re
from transactions.transaction import Transaction

ASA_URL = 'https://algoindexer.algoexplorerapi.io/v2/assets/'
TINYMAN_VERSION_REGEX = "Tinyman\s?Pool([0-9]+\.[0-9])? .*"
TINYMAN_TICKER_REGEX = "Tinyman\s?Pool.* ([A-Z]+-[A-Z]+)"
asa_dictionary = {}

# TODO: Put in own class
def build_asset(asset_id):
    response = get(ASA_URL + str(asset_id))
    data = response.json()
    if 'asset' not in data:
        asa_dictionary[asset_id] = { 'name' : asset_id, 'ticker' : asset_id, 'decimals' : 0 }
    else:
        asset = {}
        asset_data = data['asset']
        params = asset_data['params']
        asset['decimals'] = params['decimals']
        if 'unit-name' in params:
            name_with_no_digits = params['unit-name'].translate({ord(k): None for k in digits}) 
            # Detect tinyman both v1 and v1.1
            if name_with_no_digits == 'TMPOOL':
                asset['ticker'] = params['name']
                version = re.findall(TINYMAN_VERSION_REGEX, params['name'])[0]
                if version != '':
                    asset['tinyman_version'] = version
                else:
                    asset['tinyman_version'] = '1'
                asset['ticker'] = re.findall(TINYMAN_TICKER_REGEX, params['name'])[0]
                asa_dictionary[asset_id] = asset['tinyman_version']
            else:
                asset['ticker'] = params['unit-name']
        else:
            asset['ticker'] = asset_id
        if 'name' in params:
            asset['name'] = params['name']
        
        asa_dictionary[asset_id] = asset

class AsaTransaction(Transaction):
    def __init__(self, wallet, data):
        super().__init__(wallet, data)
        self.transaction_type = 'axfer'
        asset_transfer_data = data['asset-transfer-transaction']
        self.receiver = asset_transfer_data['receiver']
        self.set_rewards(data)
        
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

        if asset_id not in asa_dictionary:
            build_asset(asset_id)                
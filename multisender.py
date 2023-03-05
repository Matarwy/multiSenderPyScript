from web3 import Web3
from web3.middleware import geth_poa_middleware
import time
import json

with open('config.json', 'r') as f:
    config = json.load(f)
    priveteKey = config['priveteKey']
    RPCEndpoint = config['RPCEndpoint']
    tokenAddress = config['tokenAddress']
    SenderAddress = config['SenderAddress']

# Initialize web3 provider
web3 = Web3(Web3.HTTPProvider(RPCEndpoint))
web3.middleware_onion.inject(geth_poa_middleware, layer=0)


# Set the private key of the sender wallet
private_key = priveteKey

# Set the token contract address and ABI
contract_address = tokenAddress
with open('abi.json', 'r') as f:
    contract_abi = json.load(f)

# Set the recipient addresses and token amounts
with open('usersnew.json', 'r') as f:
    recipients = json.load(f)


# Get the token contract instance
contract = web3.eth.contract(address=contract_address, abi=contract_abi)

# Create and sign the transactions
txs = []
for recipient in recipients:
    address = web3.toChecksumAddress(recipient['bep20'])
    tx = contract.functions.transfer(address, recipient['amount']).buildTransaction({
        'nonce': web3.eth.getTransactionCount(SenderAddress),
        'gasPrice': Web3.toWei('5', 'gwei'),
        'from': SenderAddress,
        'chainId': 56  # BSC chain ID
    })
    signed_tx = web3.eth.account.sign_transaction(tx, private_key=private_key)
    try:
        tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
        print(f'Transaction sent: {tx_hash.hex()}')
        txs.append(tx_hash.hex())
        while True:
            try:
                receipt = web3.eth.get_transaction_receipt(tx_hash)
                if receipt is not None:
                    break
            except:
                pass
            time.sleep(5)
    except Exception as e:
        print(e)

for recipient in recipients:
    address = web3.toChecksumAddress(recipient['bep20'])
    tx = contract.functions.setIsDividendExempt(address, True).buildTransaction({
        'nonce': web3.eth.getTransactionCount(SenderAddress),
        'gasPrice': Web3.toWei('5', 'gwei'),
        'from': SenderAddress,
        'chainId': 56  # BSC chain ID
    })
    signed_tx = web3.eth.account.sign_transaction(tx, private_key=private_key)
    try:
        tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
        print(f'Transaction sent: {tx_hash.hex()}')
        txs.append(tx_hash.hex())
        while True:
            try:
                receipt = web3.eth.get_transaction_receipt(tx_hash)
                if receipt is not None:
                    break
            except:
                pass
            time.sleep(5)
    except Exception as e:
        print(e)
with open('txs.txt', 'w') as f:
    for tx in txs:
        f.write(f'{tx}\n')


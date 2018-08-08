import json

from argparse import ArgumentParser
from web3 import Web3
from eth_keys import keys
from ethereum.transactions import Transaction
from web3.utils.validation import (
    validate_abi,
    validate_address,
)
from web3.utils.encoding import (
    hexstr_if_str,
    to_bytes,
    to_hex,
)

def main(provider_endpoint_uri, private_key):
  contract_address = '0xB7E7AeD7a722ccb62cBE1C87b950D5792512589d'
  contract_abi = json.loads('[{"constant":true,"inputs":[],"name":"name","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"spender","type":"address"},{"name":"tokens","type":"uint256"}],"name":"approve","outputs":[{"name":"success","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"totalSupply","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"from","type":"address"},{"name":"to","type":"address"},{"name":"tokens","type":"uint256"}],"name":"transferFrom","outputs":[{"name":"success","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"decimals","outputs":[{"name":"","type":"uint8"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"_totalSupply","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"tokenOwner","type":"address"}],"name":"balanceOf","outputs":[{"name":"balance","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[],"name":"acceptOwnership","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"owner","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"symbol","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"a","type":"uint256"},{"name":"b","type":"uint256"}],"name":"safeSub","outputs":[{"name":"c","type":"uint256"}],"payable":false,"stateMutability":"pure","type":"function"},{"constant":false,"inputs":[{"name":"to","type":"address"},{"name":"tokens","type":"uint256"}],"name":"transfer","outputs":[{"name":"success","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"name":"a","type":"uint256"},{"name":"b","type":"uint256"}],"name":"safeDiv","outputs":[{"name":"c","type":"uint256"}],"payable":false,"stateMutability":"pure","type":"function"},{"constant":false,"inputs":[{"name":"spender","type":"address"},{"name":"tokens","type":"uint256"},{"name":"data","type":"bytes"}],"name":"approveAndCall","outputs":[{"name":"success","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"name":"a","type":"uint256"},{"name":"b","type":"uint256"}],"name":"safeMul","outputs":[{"name":"c","type":"uint256"}],"payable":false,"stateMutability":"pure","type":"function"},{"constant":true,"inputs":[],"name":"newOwner","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"tokenAddress","type":"address"},{"name":"tokens","type":"uint256"}],"name":"transferAnyERC20Token","outputs":[{"name":"success","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"name":"tokenOwner","type":"address"},{"name":"spender","type":"address"}],"name":"allowance","outputs":[{"name":"remaining","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"a","type":"uint256"},{"name":"b","type":"uint256"}],"name":"safeAdd","outputs":[{"name":"c","type":"uint256"}],"payable":false,"stateMutability":"pure","type":"function"},{"constant":false,"inputs":[{"name":"_newOwner","type":"address"}],"name":"transferOwnership","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"inputs":[],"payable":false,"stateMutability":"nonpayable","type":"constructor"},{"payable":true,"stateMutability":"payable","type":"fallback"},{"anonymous":false,"inputs":[{"indexed":true,"name":"_from","type":"address"},{"indexed":true,"name":"_to","type":"address"}],"name":"OwnershipTransferred","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"from","type":"address"},{"indexed":true,"name":"to","type":"address"},{"indexed":false,"name":"tokens","type":"uint256"}],"name":"Transfer","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"tokenOwner","type":"address"},{"indexed":true,"name":"spender","type":"address"},{"indexed":false,"name":"tokens","type":"uint256"}],"name":"Approval","type":"event"}]')
  # MIST Account
  to_address = '0x1441cF38f688C15Fb07741E390948CbA3C7B2590'
  to_amount = 1

  web3 = Web3(Web3.HTTPProvider(provider_endpoint_uri))

  # make sure connection is established
  isConnected = web3.isConnected()
  print('isConnected:{}'.format(isConnected))

  # validate contract address and abi
  print('validate_address:{}'.format(validate_address(contract_address)))
  print('validate_abi:{}'.format(validate_abi(contract_abi)))

  # init contract instance
  token_contract = web3.eth.contract(contract_address, abi=contract_abi)

  private_key_bytes = hexstr_if_str(to_bytes, private_key)
  print('private_key_bytes:{}'.format(private_key_bytes))
  pk = keys.PrivateKey(private_key_bytes)
  print('pk:{}'.format(pk))

  # get default account address
  address = web3.eth.defaultAccount = pk.public_key.to_checksum_address()
  print('address:{}'.format(address))

  # get Ether balance of the wallet
  balance = web3.fromWei(web3.eth.getBalance(address), 'ether')
  print('Ether balance:{}'.format(balance))

  # get JMToken balance of the wallet
  balance = web3.fromWei(token_contract.call().balanceOf(address), 'ether')
  print('JMToken balance:{}'.format(balance))

  # In order to transact with Infura nodes, you will need to create and sign 
  # transactions offline before sending them, as Infura nodes have no visibility 
  # of your encrypted Ethereum key files, which are required to unlock accounts 
  # via the Personal Geth/Parity admin commands.

  nonce = web3.eth.getTransactionCount(address, 'pending')
  print('nonce:{}'.format(nonce))

  jmt_tx = token_contract.functions.transfer(
    to_address,
    to_amount).buildTransaction({
      # testnet
      'chainId': 3,
      # gas limit
      'gas': 100000,
      # gas price in Gwei = 10^-9 Eth
      'gasPrice': web3.eth.gasPrice,
      'nonce': nonce,
    })
  print('jmt_tx:{}'.format(jmt_tx))

  signed_txn = web3.eth.account.signTransaction(
    jmt_tx,
    private_key_bytes
  )
  print('signed_txn:{}'.format(signed_txn))

  tx_id = web3.toHex(web3.eth.sendRawTransaction(signed_txn.rawTransaction))
  print('tx_id:{}'.format(tx_id))


if __name__ == '__main__':
  parser = ArgumentParser(description='a simple demo of JMToken transfer')
  parser.add_argument('provider_endpoint_uri', help='Infura endpoint, ex: https://ropsten.infura.io/[API KEY]')
  parser.add_argument('private_key', help='Account private key, ex: 3192b...40506')

  args = parser.parse_args()
  main(args.provider_endpoint_uri, args.private_key)

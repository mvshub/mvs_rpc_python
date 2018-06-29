# -*- encoding:utf-8 -*-

import os
import sys
import time
from threading import Thread

# refer to: https://github.com/mvshub/mvs_rpc_python
from mvs_rpc import mvs_api

#===============================================================================
#                   MVS API METHOD
#===============================================================================
def generate_new_address(name, pwd):
    errmsg, result = mvs_api.getnewaddress(name, pwd, 1)
    if None == errmsg:
        return result["addresses"][0]
    return None

def get_public_key(name, pwd, address):
    errmsg, result = mvs_api.getpublickey(name, pwd, address)
    if None == errmsg:
        return result["public-key"]
    return None

def send_etp(name, pwd, address, amount):
    errmsg, result = mvs_api.send(name, pwd, address, amount)
    return errmsg

def register_did(name, pwd, address, did):
    errmsg, result = mvs_api.registerdid(name, pwd, address, did)
    return errmsg

def transfer_did(name, pwd, address, did):
    errmsg, result = mvs_api.didchangeaddress(name, pwd, address, did)
    if None == errmsg:
        return result
    return None

def get_did(did):
    errmsg, result = mvs_api.getdid(did)
    if None == errmsg:
        return result['addresses']
    return None

def generate_multisig_address(name, pwd, self_publickey, parter_publickey):
    errmsg, result = mvs_api.getnewmultisig(name, pwd, 1, 2, self_publickey, parter_publickey)
    if None == errmsg:
        return result["address"]
    return None

def broadcast_rawtx(rawtx):
    errmsg, result = mvs_api.sendrawtx(rawtx)
    return errmsg

def get_etp(address):
    errmsg, result = mvs_api.getaddressetp(address)
    if None == errmsg:
        return int(result['balance']['unspent'])
    return 0

#===============================================================================
#                   MAIN
#===============================================================================
def wait_mining(param, func):
    i = 0
    while i < 20:
        if func(param):
            print("waiting for miner to package")
            time.sleep(10)
        else:
            return False
    return True

account_name = 'Exchange'       # account name of exchange
account_pwd = 'exchangepwd'     # password of account

if __name__ == '__main__':
    print('Exchange register evatar example')

    #===========================================================================
    # register DID
    #===========================================================================

    # get DID from user
    did = input('Please input the name of DID:')
    print('user want to register DID: {}'.format(did))

    # generate new address
    address = generate_new_address(account_name, account_pwd)
    if None == address:
        print('Failed to generate new address')
        sys.exit(0)
    print("generate a new address: {}".format(address))

    # send 1 ETP to the new address
    errmsg = send_etp(account_name, account_pwd, address, 100000000)
    if None != errmsg:
        print("Failed to send ETP to {}. error: {}".format(address, errmsg))
        sys.exit(0)

    # register DID to the new address
    errmsg = register_did(account_name, account_pwd, address, did)
    if None != errmsg:
        print("Failed to register DID {} to {}. error: {}".format(did, address, errmsg))
        sys.exit(0)

    if wait_mining(did, lambda x : get_did(x) == None):
        sys.exit(0)

    print("** Successfully registered did {} to {}\n".format(did, address))

    #===========================================================================
    # transfer DID
    #===========================================================================

    # get public key from user
    user_public_key = input("Please input user's public key:")
    print("User's public key: {}".format(user_public_key))

    # get public key of the new address
    self_public_key = get_public_key(account_name, account_pwd, address)
    if None == address:
        print('Failed to get public key from address {}'.format(address))
        sys.exit(0)
    print("the public key of the address: {}".format(self_public_key))

    # generate multisig address
    multisig_address = generate_multisig_address(
        account_name, account_pwd, self_public_key, user_public_key)
    if None == multisig_address:
        print('Failed to generate multisig address {}'.format(address))
        sys.exit(0)
    print("generate a multisig address: {}".format(multisig_address))

    # send 0.0001 ETP to the multisig address
    print("sending etp to multisig address")
    errmsg = send_etp(account_name, account_pwd, multisig_address, 10000)
    if None != errmsg:
        print("Failed to send ETP to {}. error: {}".format(address, errmsg))
        sys.exit(0)

    if wait_mining(multisig_address, lambda x : get_etp(multisig_address) == 0):
        sys.exit(0)

    # transfer DID to the multisig address
    print("transfering did to multisig address")
    rawtx = transfer_did(account_name, account_pwd, multisig_address, did)
    if None == rawtx:
        print("Failed to transfer DID {} to {}.\nerror: {}".format(did, multisig_address, errmsg))
        sys.exit(0)

    errmsg = broadcast_rawtx(rawtx)
    if None != errmsg:
        print("Failed to broadcast rawtx {}. error: {}".format(rawtx, errmsg))
        sys.exit(0)

    if wait_mining([did, multisig_address], lambda x : get_did(x[0])[0]['address'] != x[1]):
        sys.exit(0)

    print("** Successfully transfered did {} to {}".format(did, multisig_address))

# Exchange register evatar example
# Please input the name of DID:'avatar01@Alice'
# user want to register DID: avatar01@Alice
# generate a new address: MUfeU351P7ipuUFJcotzQzDesKHHpuiFpA
# waiting for miner to package
# ** Successfully registered did avatar01@Alice to MUfeU351P7ipuUFJcotzQzDesKHHpuiFpA
#
# Please input user's public key:"0344befcd59670651a6441c00ef26caa104bab8ff9e5ec3f6e9b65bac9194cad0a"
# User's public key: 0344befcd59670651a6441c00ef26caa104bab8ff9e5ec3f6e9b65bac9194cad0a
# the public key of the address: 034354fb24938a6b061341e9fdae6b35e3391958c52dccdfc27213ae3ae68288b7
# generate a multisig address: 3H62VSQPshYgxmDqCUbyZcaPCenLfJQrUH
# sending etp to multisig address
# waiting for miner to package
# transfering did to multisig address
# waiting for miner to package
# ** Successfully transfered did avatar01@Alice to 3H62VSQPshYgxmDqCUbyZcaPCenLfJQrUH

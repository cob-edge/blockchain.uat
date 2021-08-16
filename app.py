#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (c) 2016 Roger Light <roger@atchoo.org>
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Eclipse Distribution License v1.0
# which accompanies this distribution.
#
# The Eclipse Distribution License is available at
#   http://www.eclipse.org/org/documents/edl-v10.php.
#
# Contributors:
#    Roger Light - initial implementation

# This shows an example of using the subscribe.simple helper function. JARVIS WAS HERE

#import context  # Ensures paho is in PYTHONPATH
#import paho.mqtt.subscribe as subscribe

#topics = ['CTI/Sensors/#']

#m = subscribe.simple(topics, hostname="broker.hivemq.com", retained=False, msg_count=2)
#for a in m:
#    print(a.topic)
#    print(a.payload)



import json
from web3 import Web3, HTTPProvider

# truffle development blockchain address
blockchain_address = 'http://127.0.0.1:7545'
# Client instance to interact with the blockchain
web3 = Web3(HTTPProvider(blockchain_address))
# Set the default account (so we don't need to set the "from" for every transaction call)
web3.eth.defaultAccount = web3.eth.accounts[0]

# Path to the compiled contract JSON file
compiled_contract_path = 'build/contracts/IoT.json'
# Deployed contract address (see `migrate` command output: `contract address`)
deployed_contract_address = '0xD18BD733d43Ea1a76Bd80Ec097426033Da62f471'

with open(compiled_contract_path) as file:
    contract_json = json.load(file)  # load contract info as JSON
    contract_abi = contract_json['abi']  # fetch contract's abi - necessary to call its functions

# Fetch deployed contract reference
contract = web3.eth.contract(address=deployed_contract_address, abi=contract_abi)

# Call contract function (this is not persisted to the blockchain)
#message = contract.functions.sayHello().call()

#print(message)
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



## import json
##from web3 import Web3, HTTPProvider

# truffle development blockchain address
## blockchain_address = 'http://127.0.0.1:7545'
# Client instance to interact with the blockchain
## web3 = Web3(HTTPProvider(blockchain_address))
# Set the default account (so we don't need to set the "from" for every transaction call)
## web3.eth.defaultAccount = web3.eth.accounts[0]

# Path to the compiled contract JSON file
## compiled_contract_path = 'build/contracts/IoT.json'
# Deployed contract address (see `migrate` command output: `contract address`)
## deployed_contract_address = '0xD18BD733d43Ea1a76Bd80Ec097426033Da62f471'

## with open(compiled_contract_path) as file:
##    contract_json = json.load(file)  # load contract info as JSON
##    contract_abi = contract_json['abi']  # fetch contract's abi - necessary to call its functions

# Fetch deployed contract reference
## contract = web3.eth.contract(address=deployed_contract_address, abi=contract_abi)

# Call contract function (this is not persisted to the blockchain)
#message = contract.functions.sayHello().call()

#print(message)

import random
import pyodbc 
import numpy
import pandas

# Some other example server values are
# server = 'localhost\sqlexpress' # for a named instance
# server = 'myserver,port' # to specify an alternate port
server = 'tcp:cob-edge-uat.database.windows.net' 
database = 'IoTDB' 
username = 'cob.edge.uat' 
password = 'Aoed7Test' 
cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
cursor = cnxn.cursor()

rows = numpy.array(pandas.read_csv("blocks.csv"))

#Sample insert query
# for row in rows:
# 	count = cursor.execute("""
# 	INSERT INTO [dbo].[IOTBlocks] (number, hash, parent_hash, nonce, sha3_uncles, logs_bloom , transactions_root, state_root , receipts_root, miner, difficulty, total_difficulty, size, extra_data, gas_limit, gas_used, timestamp, transaction_count, base_fee_per_gas) 
# 	VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
# 	row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11], row[12], row[13], row[14], row[15], row[16], row[17], 0).rowcount
# 	cnxn.commit()
# print ("updated databse")

rows = numpy.array(pandas.read_csv("transactions.csv"))

#Sample insert query
#row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11], row[12], row[13], row[14]).rowcount
#row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11], 0, 0, 0).rowcount
#'hello', 1, 'hello', 1, 1, 'hello', 'hello', 1, 1, 11, "hello", 1, 0, 0, 0).rowcount
for row in rows:
	try:
		count = cursor.execute("""
		INSERT INTO [dbo].[IOTTransactions] (hash, nonce, block_hash, block_number, transaction_index, from_address , to_address, value , gas, gas_price, input, block_timestamp, max_fee_per_gas, max_priority_fee_per_gas, transaction_type, sensor_id) 
		VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
		row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11], 0, 0, 0, random.randint(0,150)).rowcount
		cnxn.commit()
	except:
		print("bad row")
print ("updated databse")





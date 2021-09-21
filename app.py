# Edge Test python file

#import paho.mqtt.client as mqtt
#import time
#
#def on_log(client, userdata, level, buf):
	#print("log: " + buf)
#
#def on_connect(client, userdata, flags, rc):
	#if rc == 0:
	#	print("Successfully connected")
	#else:
	#	print("Error connecting, returned: ", rc)
#
#def on_disconnect(client, userdata, flags, rc = 0):
	#print("Disconnected from client: " + str(rc))
#
#def on_message(client, userdata, msg):
	#topic = msg.topic
	#m_decode = str(msg.payload.decode("utf-8"))
	#print("Message received", m_decode)
#
#broker = "broker.hivemq.com"
#client = mqtt.Client("cob-edge-1", clean_session = False)
#
#client.on_connect = on_connect
#client.on_disconnect = on_disconnect
#client.on_message = on_message
##client.on_log = on_log
#
#print("Connecting to broker:", broker)
#
#time.sleep(2)
#
#client.connect(broker)
#client.loop_start()
#client.subscribe("CTI/Sensors/#")
#client.publish("CTI/Sensors/")
#
#time.sleep(20)
#
#client.loop_stop()
#client.disconnect()

# End of file

import json
from web3 import Web3, HTTPProvider

# truffle development blockchain address
#blockchain_address = 'http://127.0.0.1:9545'

# ganache development blockchain address
blockchain_address = 'http://127.0.0.1:8545'

# Client instance to interact with the blockchain
web3 = Web3(HTTPProvider(blockchain_address))

# Set the default account (so we don't need to set the "from" for every transaction call)
web3.eth.defaultAccount = web3.eth.accounts[0]

# Path to the compiled contract JSON file
compiled_contract_path = 'build/contracts/IoT.json'

# Deployed contract address (see `migrate` command output: `contract address`)
deployed_contract_address = '0x918785Aed064773FEC58c759DdA90Bb234F7ddFd'

# truffle transaction address
#0x53F10682Fd87AB7CC41c4701DB41eb6bB0bBF522

# ganache transaction address Hot-Duck
#0x07A05C601b16616bc46A7b74fCA9F0285331777c

# ganache transaction address COB-Edge
#0x918785Aed064773FEC58c759DdA90Bb234F7ddFd

print('--Program Executing--')

with open(compiled_contract_path) as file:
    contract_json = json.load(file)  # load contract info as JSON
    contract_abi = contract_json['abi']  # fetch contract's abi - necessary to call its functions

# Fetch deployed contract reference
contract = web3.eth.contract(address=deployed_contract_address, abi=contract_abi)

# Call contract function (this is persisted to the blockchain)
#tx_hash = contract.functions.setPayload('').transact()

#tx_receipt = web3.eth.waitForTransactionReceipt(tx_hash)
#print('tx_hash: {}'.format(tx_hash.hex()))

contract.functions.createTask(1, 'timestamp', 'hello world', 'Static', 22, 100, 2, 1234567, 875432).transact()

#message = contract.functions.sayHello().call()
#print(message)

print('--End Execution--')
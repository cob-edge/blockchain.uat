import json
import time
import random
import pyodbc 
import numpy
import pandas
#import context
import paho.mqtt.client as mqtt
import paho.mqtt.subscribe as subscribe
from web3 import Web3, HTTPProvider

def on_log(client, userdata, level, buf):
	print("log: " + buf)

def on_connect(client, userdata, flags, rc):
	if rc == 0:
		print("Successfully connected")
	else:
		print("Error connecting, returned: ", rc)

def on_disconnect(client, userdata, flags, rc = 0):
	print("Disconnected from client: " + str(rc))

def on_message(client, userdata, msg):
	topic = msg.topic
	m_decode = str(msg.payload.decode("utf-8"))
	if m_decode:
		print("Message received", m_decode)

broker = "broker.hivemq.com"
client = mqtt.Client("cob-edge-1", clean_session = True)

# ganache development blockchain address
blockchain_address = 'http://127.0.0.1:8545'

# Client instance to interact with the blockchain
web3 = Web3(HTTPProvider(blockchain_address))

# Set the default account (so we don't need to set the "from" for every transaction call)
web3.eth.defaultAccount = web3.eth.accounts[0]

# Path to the compiled contract JSON file
compiled_contract_path = 'build/contracts/IoT.json'

# Deployed contract address (see `migrate` command output: `contract address`)
deployed_contract_address = '0x3A6Af68aC79D9F1560D1dA7a71F4B9375BA990DA'

server = 'tcp:cob-edge.database.windows.net' 
database = 'IoTDB' 
username = 'cob.edge.admin' 
password = 'Aoed7Test' 
cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
cursor = cnxn.cursor()

client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_message = on_message
#client.on_log = on_log

print("Connecting to broker:", broker)

client.connect(broker)
client.loop_start()
client.subscribe("CTI/Sensors/#")
client.publish("CTI/Sensors/")

with open(compiled_contract_path) as file:
    contract_json = json.load(file)  # load contract info as JSON
    contract_abi = contract_json['abi']  # fetch contract's abi - necessary to call its functions

# Fetch deployed contract reference
contract = web3.eth.contract(address=deployed_contract_address, abi=contract_abi)

time.sleep(2)

run = True
Timeout = 25

print("Waiting for messages...")

while run:
	client._msgtime_mutex.acquire()
	client._msgtime_mutex.release()
	last_msg_in = client._last_msg_in

	now = time.monotonic()

	print(now - last_msg_in)

	# Call contract function (this is persisted to the blockchain)
	#contract.functions.createTask(2, 'timestamp', 'Ganache IoT contract test', 'Vehicle', 18, 79, 5, 1534188, 7220981).transact()

	if now - last_msg_in > Timeout:
		print("No messages to send \nDisconnecting...")
		client.loop_stop()
		client.disconnect()
		run = False

time.sleep(2)

rows = numpy.array(pandas.read_csv("blocks.csv"))

#Insert query for Blocks
for row in rows:
	try:
		count = cursor.execute("""
		INSERT INTO [dbo].[Block] (Block_Number, Hash, Parent_Hash, Nonce, SHA3_Uncles, Logs_Bloom, Transactions_Root, State_Root, Receipts_Root, Miner, Difficulty, Total_Difficulty, Size, Extra_Data, Gas_Limit, Gas_Used, Timestamp, Transaction_Count, Base_Fee_Per_Gas) 
		VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
		row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11], row[12], row[13], row[14], row[15], row[16], row[17], 0).rowcount
		cnxn.commit()

		print("Row Inserted")
	except:
		print("Unable to Insert")

print ("Updated Block Table in database")

rows = numpy.array(pandas.read_csv("transactions.csv"))

#Insert query for Transactions
for row in rows:
	try:
		count = cursor.execute("""
		INSERT INTO [dbo].[Block Transactions] (Hash, Nonce, Block_Hash, Block_Number, Transaction_Index, From_Address, To_Address, Value, Gas, Gas_Price, Input, Timestamp, Max_Fee_Per_Gas, Max_Priority_Fee_Per_Gas, Transaction_Type, Sensor_ID, Vehicle_ID) 
		VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
		row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11], 0, 0, 0, random.randint(0,150), random,randit(0,50)).rowcount
		cnxn.commit()

		print("Row Inserted")
	except:
		print("Unable to Insert")

print ("Updated Transactions Table in database")

# truffle development blockchain address
#blockchain_address = 'http://127.0.0.1:9545'

# ganache transaction address Hot-Duck
#0x3A6Af68aC79D9F1560D1dA7a71F4B9375BA990DA

# ganache transaction address COB-Edge
#0x918785Aed064773FEC58c759DdA90Bb234F7ddFd

# Call contract function (this is persisted to the blockchain)
#contract.functions.createTask(2, 'timestamp', 'second test', 'Vehicle', 18, 79, 5, 1534188, 7220981).transact()
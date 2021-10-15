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
		#print("Message received", m_decode)
		set_IoT(str(m_decode))

def set_IoT(msg):
	#print("Message to change " + msg)
	jsonMsg = json.loads(msg)

	id = jsonMsg["id"]
	timestamp = jsonMsg["Timestamp"]
	desc = jsonMsg["Desc"]
	type = jsonMsg["EntityType"]
	v1 = jsonMsg["v1"]
	v2 = jsonMsg["v2"]
	v3 = jsonMsg["v3"]
	Latitude = jsonMsg["Latitude"]
	Longitude = jsonMsg["Longitude"]

	iot = IoT(id, timestamp, desc, type, v1, v2, v3, Latitude, Longitude)
	arr.append(iot)

	print("IoT Object: ", iot)

class IoT: 
    def __init__(self, id, timestamp, desc, type, v1, v2, v3, lat, long):
        self.id = id
        self.timestamp = timestamp
        self.desc = desc
        self.type = type
        self.v1 = v1
        self.v2 = v2
        self.v3 = v3
        self.lat = lat
        self.long = long
    
    def __str__(self):
	    return str(self.__dict__)

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
deployed_contract_address = '0x8fA20508f768806159A9Eb57c08dfA98748E33d7'

server = 'tcp:cob-edge.database.windows.net' 
database = 'IoTDB' 
username = 'cob.edge.admin' 
password = 'Aoed7Test' 
cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
cursor = cnxn.cursor()
arr = []

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
Timeout = 30

print("Waiting for messages...")

while run:
	client._msgtime_mutex.acquire()
	client._msgtime_mutex.release() 
	
	last_msg_in = client._last_msg_in

	now = time.monotonic()

	#print(now - last_msg_in)
	#add lag potench

	if now - last_msg_in > Timeout:
		print("No messages to send \nDisconnecting...")
		client.loop_stop()
		client.disconnect()
		run = False

# Call contract function and push IoT data into blockchain (this is persisted to the blockchain)
for iot in arr:
	#print("IoT Object: ", iot)
	latitude = iot.lat
	longitude = iot.long
	contract.functions.createTask(iot.id, iot.timestamp, iot.desc, iot.type, iot.v1, iot.v2, iot.v3, str(latitude), str(longitude)).transact()

time.sleep(2)

# Runs command to take new text files and push into SQL

rows = numpy.array(pandas.read_csv("blocks.csv"))

# Insert query for Blocks
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

# Insert query for Transactions
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

# ganache transaction address COB-Edge
#0x8fA20508f768806159A9Eb57c08dfA98748E33d7
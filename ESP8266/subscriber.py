import paho.mqtt.client as mqtt
 
# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, rc, hehe):
	print("Connected with result code "+str(rc))
	client.subscribe("#")
 
def on_message(client, userdata, msg):
	print(msg.topic + " : " + msg.payload.decode('utf-8'))
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
 
client.connect("15.164.149.11", 1883, 60)
 
client.loop_forever()
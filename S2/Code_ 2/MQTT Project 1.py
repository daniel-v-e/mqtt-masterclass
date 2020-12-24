import paho.mqtt.client as mqtt
from gpiozero import OutputDevice
import adafruit_dht
import sys
import time
import board

# Initialization of variables
# broker = "broker.hivemq.com"
broker = "192.168.137.1"
port = 1883
keepalive = 60
relay = OutputDevice(17)
print("1")

# Function for processing subscribed messages
def on_message(client, userdata, message): #forprocessingsubscribedmessages
    msg = str(message.payload.decode("utf-8"))
    print("message received ", msg)
    automation(msg)
    print("2")

# Function for controlling the relay
def automation(msg):
    if msg == "on":
        relay.on()
    elif msg == "off":
        relay.off()
    else:
        relay.off()
        print("Invalid Message")
    print("3")

print("4.1")
# Initialization of MQTT client
client = mqtt.Client()
print("4.2")
client.on_message = on_message
print("4.3")
client.connect(broker, port, keepalive)
print("4.4")
client.loop_start()
print("4.5")

# Initialization of DHT device
dhtDevice = adafruit_dht.DHT11(board.D4)
print("5")

# Main loop
try:
    while True:
        # humidity, temperature = Adafruit_DHT.read_retry(11, 4)  #sensor, gpio
        temperature = dhtDevice.temperature
        humidity = dhtDevice.humidity
        humidity = round(humidity, 2)
        temperature = round(temperature, 2)
        print("6")
        print('Temp={0:0.1f}*C  Humidity={1:0.1f}%'.format(temperature, humidity))
        # Sending humidity and temperature data to Broker
        client.publish('sensor/temp',temperature, 0)
        client.publish('sensor/hum',humidity, 0)
        client.subscribe("automation/bulb1", 0)
        time.sleep(2)
        print("7")
except KeyboardInterrupt:
    pass

# Cleanup
client.loop_stop()
client.disconnect()
print("8")

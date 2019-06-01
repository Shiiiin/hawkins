from time import sleep, strftime, time
import threading, zipfile, csv, os
# ina219
from ina219 import INA219
from ina219 import DeviceRangeError
# twilio message
# from twilio.rest import Client
from config import *  # config.py module
# pubnub
from pubnub.callbacks import SubscribeCallback
from pubnub.enums import PNStatusCategory
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub

from send_log import send_log_files_to_admin

# pubnub configuration
currentChannel = "current"
voltageChannel = "voltage"
powerChannel = "power"
sensorsList = ["ina219"]
data = {}

pnconfig = PNConfiguration()

pnconfig.subscribe_key = SUB_KEY
pnconfig.publish_key = PUB_KEY

pubnub = PubNub(pnconfig)

# ina219 configuration
SHUNT_OHMS = 0.1
MAX_EXPECTED_AMPS = 0.2
MAX_BYTE_SIZE = 32768  # limit byte size for csv file
file_no = 1
# data_dir = "/home/pi/Desktop/raspberrypi-practice/data"
data_dir = '~/Desktop/PanelData/data'
path = "~/Desktop/PanelData/data/log-{}.csv".format(file_no)
VOLTAGE = 0
CURRENT = 0
POWER = 0
status = True
first = False

I1 = 0
I2 = 0 
ErrorRate = 0 
P = 0
Charge = 0

ina = INA219(SHUNT_OHMS, MAX_EXPECTED_AMPS)
ina.configure(ina.RANGE_16V)

# ina219 functions
def read_ina219():
    global VOLTAGE, CURRENT, POWER
    try:
        VOLTAGE = ina.voltage()
        CURRENT = ina.current()
        POWER = ina.power()

    except DeviceRangeError as e:
        print(type(e), "::", e, "-", "Current overflow")

    except KeyboardInterrupt:
        print("\nCtrl-C pressed. Program exiting...")

def set_file_no():
    global file_no, path
    if not os.path.exists(data_dir):
        os.mkdir(data_dir)
    if os.path.exists(path):
        for root, dirs, files in os.walk(data_dir):
            for name in files:
                extension = os.path.join(root, name)[-5:]
                if "csv" in extension:
                    num = os.path.join(root, name)[-5:-4]
                    if int(num) > file_no:
                        file_no = int(num)
    if file_no is not 1:
        path = "/home/pi/Desktop/raspberrypi-practice/data/log-{}.csv".format(
            file_no)

def get_path():
    global file_no, path, first
    if os.path.exists(path):
        first = False
        if os.path.getsize(path) > MAX_BYTE_SIZE:
            file_no += 1
            path = "/home/pi/Desktop/raspberrypi-practice/data/log-{}.csv".format(
                file_no)
    else:
        first = True
    return path

def write_data():
    global first
    data = [
    {'TIME': '{}'.format(strftime("%Y-%m-%d %H:%M:%S")), 'POWER': POWER, 'VOLTAGE': VOLTAGE, 'CURRENT': CURRENT}
    ]
    
    field_names = ['TIME', 'POWER', 'VOLTAGE', 'CURRENT']
    # create new file and open it in append mode with the name log
    with open(get_path(), "a") as log:
        if first:
            csvfile = csv.DictWriter(log, fieldnames=field_names)
            csvfile.writeheader()
        #csvfile.writerow(data)
        log.write("{0}, {1}, {2}, {3}\n".format(
            strftime("%Y-%m-%d %H:%M:%S"), POWER, VOLTAGE, CURRENT))
        #print("{0}, {1}, {2}, {3}\n".format(
        #    strftime("%Y-%m-%d %H:%M:%S"), VOLTAGE, CURRENT, POWER))
    log.close()

def compress_files():
    global data_dir
    zip_path = data_dir + '/log.zip'

    data_zip = zipfile.ZipFile(zip_path, 'w')

    for folder, files in os.walk(data_dir):

        for file in files:
            if file.endswith('.csv'):
                data_zip.write(os.path.join(folder, file), os.path.relpath(os.path.join(folder, file), data_dir), compress_type=zipfile.ZIP_DEFLATED)

    data_zip.close()

def ReadAndComputeData():
    global I1, I2, ErrorRate, P, Charge
    P = 10
    I1 = 1
    I2 = 5
    ErrorRate = 10
    Charge = 50



def Compute():
    global file_no, status, path
    set_file_no()
    print("Starting to send data...")
    while status:
        # read_ina219()
        ReadAndComputeData()
        write_data()
        publish(currentChannel, {"eon": {"current": CURRENT}})
        publish(voltageChannel, {"eon": {"voltage": VOLTAGE}})
        publish(powerChannel, {"eon": {"power": POWER}})
        
        if file_no is 10 and os.path.getsize(path) > MAX_BYTE_SIZE-100:
           compress_files()
           send_log_files_to_admin()
           os.system('rm -r data/')
           set_file_no()
            
        sleep(1)

# # twilio function
# def send_message():
#     account_sid = ACCOUNT_SID  # Put your Twilio account SID here
#     auth_token = AUTH_TOKEN  # Put your auth token here
#     client = Client(account_sid, auth_token)
#     message = client.api.account.messages.create(
#         to=TO,  # Put your cellphone number here
#         from_=FROM,  # Put your Twilio number here
#         body="This is a text send from Raspberry Pi.")

# pubnub functions
def publish(channel, msg):
        pubnub.publish().channel(channel).message(msg).pn_async(my_publish_callback)

def my_publish_callback(envelope, status):
    # Check whether request successfully completed or not
    if not status.is_error():
        pass  # Message successfully published to specified channel.
    else:
        pass  # Handle message publish error. Check 'category' property to find out possible issue
        # because of which request did fail.
        # Request can be resent using: [status retry];

class MySubscribeCallback(SubscribeCallback):
    def presence(self, pubnub, presence):
        pass  # handle incoming presence data

    def status(self, pubnub, status):
        if status.category == PNStatusCategory.PNUnexpectedDisconnectCategory:
            pass  # This event happens when radio / connectivity is lost

        elif status.category == PNStatusCategory.PNConnectedCategory:
            # Connect event. You can do stuff like publish, and know you'll get it.
            # Or just use the connected event to confirm you are subscribed for
            # UI / internal notifications, etc
            #publish(currentChannel, "Device Connected! (current)")
            #publish(voltageChannel, "Device Connected! (voltage)")
            #publish(powerChannel, "Device Connected! (power)")
            print("Device Connected!")
        elif status.category == PNStatusCategory.PNReconnectedCategory:
            pass
            # Happens as part of our regular operation. This event happens when
            # radio / connectivity is lost, then regained.
        elif status.category == PNStatusCategory.PNDecryptionErrorCategory:
            pass
            # Handle message decryption error. Probably client configured to
            # encrypt messages and on live data feed it received plain text.

    def message(self, pubnub, message):
        try:
            #print(message.message, ": ", type(message.message))
            msg = message.message
            print("received json:", msg)
            key = list(msg.keys())
            if (key[0]) == "event":
                self.handleEvent(msg)   # {"event": {"sensor_name": True } }
        except Exception as e:
            print("received:", message.message)
            print(e)
            pass
        pass  # Handle new message stored in message.message

    def handleEvent(self, msg):
        global data
        eventData = msg["event"]
        key = list(eventData.keys())
        if key[0] in sensorsList:
            if eventData[key[0]] is True:
                data["ina219"] = True
            elif eventData[key[0]] is False:
                data["ina219"] = False

# main
pubnub.add_listener(MySubscribeCallback())
pubnub.subscribe().channels(currentChannel).execute()
pubnub.subscribe().channels(voltageChannel).execute()
pubnub.subscribe().channels(powerChannel).execute()

sleep(5)
ina219Thread = threading.Thread(target=Compute)
ina219Thread.start()

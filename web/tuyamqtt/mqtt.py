
import time
import paho.mqtt.client as mqtt
import logging
from threading import Thread

loglevel = logging.DEBUG
logger = logging.getLogger(__name__)
logging.basicConfig(
    format='%(asctime)s %(levelname)-8s [%(name)s] %(message)s', level=loglevel)


def connack_string(state):

    states = [
        'Connection successful',
        'Connection refused - incorrect protocol version',
        'Connection refused - invalid client identifier',
        'Connection refused - server unavailable',
        'Connection refused - bad username or password',
        'Connection refused - not authorised'
    ]
    return states[state]


class MQTT(Thread):

    def __init__(self):
        super().__init__()
        self.client = mqtt.Client()
        self.connected = False
        self.models_loaded = False
        #TODO: watch kill signal and close clean


    def load_models(self):

        try:
            from .models import Setting, Device, Dps, Dpstype
            self.Setting = Setting
            self.Device = Device
            self.Dps = Dps
            self.Dpstype = Dpstype
            self.models_loaded = True
            return True
        except Exception as ex:
            # print(ex)
            pass
        return False


    def run(self):
        
        while not self.models_loaded:
            self.load_models()

        while self.models_loaded:           
            
            if not self.connected:
                self.mqtt_connect()
                self.client.loop_start()
            #TODO: on_start publish devices once retain
            #TODO: watch for changes in Devices/Dps and publish
                #does django fire events for this?
            #TODO: watch for changes in Setting and reconnect
            #TODO: watch connection MQTT and reconnect

            # for u in self.Device.objects.all():
            # rec = self.Setting.objects.get(name="mqtt_host").value
            # print(list(self.Setting.objects.filter(name__startswith='mqtt_host').values('value')), rec)
            time.sleep(1)


    def mqtt_connect(self):

        try:
            self.client.enable_logger()
            # TODO: check if all values are there
            self.client.username_pw_set(self.Setting.objects.get(name="mqtt_user").value, self.Setting.objects.get(name="mqtt_pass").value)
            self.client.connect(self.Setting.objects.get(name="mqtt_host").value, int(self.Setting.objects.get(name="mqtt_port").value), 60)
            self.client.on_connect = self.on_connect
            self.client.loop_start()
            self.client.on_message = self.on_message

        except Exception as ex:
            logger.warning('(%s) Failed to connect to MQTT Broker %s', '', ex)
            self.connected = False


    #TODO what are the types of these func params
    def on_connect(self, client, userdata, flags, rc):

        logger.info("MQTT Connection state: %s " % (connack_string(rc)))
        self.connected = True
        self.publish_devices()
        # listen to homeassistant auto discovery, why?
        # self.client.subscribe("homeassistant/#")


    #TODO what are the types of these func params
    def on_message(self, client, userdata, message):

        logger.debug("topic %s retained %s message received %s", message.topic,
                     message.retain, str(message.payload.decode("utf-8")))
        pass


    def publish_device(self, device:dict):

        print(device)
        #TODO publish tuyamqtt config retain
        #TODO publish homeassistant config retain
        # client.publish(f"{mqtt_topic}/availability" , value, retain=True)


    def publish_devices(self):

        for device in self.Device.objects.all():
            self.publish_device(dict(device))
       
        pass

#TODO: prevent multiple starts 
# class SingleMQTT:

#    __instance = None

#    @staticmethod 
#    def getInstance():
#       """ Static access method. """
#       if SingleMQTT.__instance == None:
#          SingleMQTT()
#       return SingleMQTT.__instance

#    def __init__(self):
#       """ Virtually private constructor. """
#       if SingleMQTT.__instance != None:
#          raise Exception("This class is a singleton!")
#       else:
#          SingleMQTT.__instance = self

# s = SingleMQTT()
# print (s)

print("runs two times, why?")
x = MQTT()
x.start()


"""
def hass_discovery(self, entity):

        if entity['ip'] != '192.168.1.25':
            return

        for item in entity['attributes']['dps'].items():
            self.hass_disc_item(item)


    def hass_disc_item(self, item):
        ""
        08:56:40 MQT: kitchen_left_lighting/tele/LWT = Online (retained)
        08:56:40 MQT: kitchen_left_lighting/cmnd/POWER = 
        08:56:40 MQT: kitchen_left_lighting/tele/INFO1 = {"Module":"Sonoff Basic","Version":"8.1.0.2(1e06976-tasmota)","FallbackTopic":"cmnd/kitchen_left_lighting_fb/","GroupTopic":"sonoffs/cmnd/"}
        08:56:40 MQT: kitchen_left_lighting/tele/INFO2 = {"WebServerMode":"Admin","Hostname":"kitchen_left_lighting-7456","IPAddress":"192.168.1.34"}
        08:56:40 MQT: kitchen_left_lighting/tele/INFO3 = {"RestartReason":"Software/System restart"}
        08:56:40 MQT: kitchen_left_lighting/stat/RESULT = {"POWER":"OFF"}
        08:56:40 MQT: kitchen_left_lighting/stat/POWER = OFF
        08:56:41 MQT: homeassistant/light/ABBD20_LI_1/config =  (retained)
        08:56:41 MQT: homeassistant/switch/ABBD20_RL_1/config = {"name":"Kitchen Left Lighting","cmd_t":"~cmnd/POWER","stat_t":"~tele/STATE","val_tpl":"{{value_json.POWER}}","pl_off":"OFF","pl_on":"ON","avty_t":"~tele/LWT","pl_avail":"Online","pl_not_avail":"Offline","uniq_id":"ABBD20_RL_1","device":{"identifiers":["ABBD20"],"connections":[["mac","DC:4F:22:AB:BD:20"]]},"~":"kitchen_left_lighting/"} (retained)
        08:56:41 MQT: homeassistant/light/ABBD20_LI_2/config =  (retained)
        08:56:41 MQT: homeassistant/switch/ABBD20_RL_2/config =  (retained)
        08:56:41 MQT: homeassistant/light/ABBD20_LI_3/config =  (retained)
        08:56:41 MQT: homeassistant/switch/ABBD20_RL_3/config =  (retained)
        08:56:41 MQT: homeassistant/light/ABBD20_LI_4/config =  (retained)
        08:56:41 MQT: homeassistant/switch/ABBD20_RL_4/config =  (retained)
        08:56:41 MQT: homeassistant/light/ABBD20_LI_5/config =  (retained)
        08:56:41 MQT: homeassistant/switch/ABBD20_RL_5/config =  (retained)
        08:56:41 MQT: homeassistant/light/ABBD20_LI_6/config =  (retained)
        08:56:41 MQT: homeassistant/switch/ABBD20_RL_6/config =  (retained)
        08:56:41 MQT: homeassistant/light/ABBD20_LI_7/config =  (retained)
        08:56:41 MQT: homeassistant/switch/ABBD20_RL_7/config =  (retained)
        08:56:41 MQT: homeassistant/light/ABBD20_LI_8/config =  (retained)
        08:56:41 MQT: homeassistant/switch/ABBD20_RL_8/config =  (retained)
        08:56:41 MQT: homeassistant/binary_sensor/ABBD20_BTN_1/config = {"name":"Kitchen Left Lighting Button1","stat_t":"~stat/BUTTON1","avty_t":"~tele/LWT","pl_avail":"Online","pl_not_avail":"Offline","uniq_id":"ABBD20_BTN_1","device":{"identifiers":["ABBD20"],"connections":[["mac","DC:4F:22:AB:BD:20"]]},"~":"kitchen_left_lighting/","value_template":"{{value_json.STATE}}","pl_on":"TOGGLE","off_delay":1} (retained)
        08:56:41 MQT: homeassistant/binary_sensor/ABBD20_BTN_2/config =  (retained)
        08:56:41 MQT: homeassistant/binary_sensor/ABBD20_BTN_3/config =  (retained)
        08:56:41 MQT: homeassistant/binary_sensor/ABBD20_BTN_4/config =  (retained)
        08:56:41 MQT: homeassistant/binary_sensor/ABBD20_SW_1/config =  (retained)
        08:56:41 MQT: homeassistant/binary_sensor/ABBD20_SW_2/config =  (retained)
        08:56:41 MQT: homeassistant/binary_sensor/ABBD20_SW_3/config =  (retained)
        08:56:41 MQT: homeassistant/binary_sensor/ABBD20_SW_4/config =  (retained)
        08:56:41 MQT: homeassistant/binary_sensor/ABBD20_SW_5/config =  (retained)
        08:56:41 MQT: homeassistant/binary_sensor/ABBD20_SW_6/config =  (retained)
        08:56:41 MQT: homeassistant/binary_sensor/ABBD20_SW_7/config =  (retained)
        08:56:41 MQT: homeassistant/binary_sensor/ABBD20_SW_8/config =  (retained)
        08:56:41 MQT: homeassistant/sensor/ABBD20_status/config = {"name":"Kitchen Left Lighting status","stat_t":"~HASS_STATE","avty_t":"~LWT","frc_upd":true,"pl_avail":"Online","pl_not_avail":"Offline","json_attributes_topic":"~HASS_STATE","unit_of_meas":" ","val_tpl":"{{value_json['RSSI']}}","ic":"mdi:information-outline","uniq_id":"ABBD20_status","device":{"identifiers":["ABBD20"],"connections":[["mac","DC:4F:22:AB:BD:20"]],"name":"Kitchen Left Lighting","model":"Sonoff Basic","sw_version":"8.1.0.2(1e06976-tasmota)","manufacturer":"Tasmota"},"~":"kitchen_left_lighting/tele/"} (retained)
        08:56:44 MQT: kitchen_left_lighting/tele/STATE = {"Time":"2020-05-22T08:56:44","Uptime":"0T00:00:12","UptimeSec":1
        ""

        print(item)
        device_dps = '%s_%s' % (self.entity['deviceid'], item[0])
        ""
        we have no knowledge of what the dps values actualy do at this point
        need an interface so enduser can configure
        ""
        hass_topic = 'homeassistant/%s/%s/config' % ('unknown', device_dps)

       
        payload = {
            "name": "name here",
            "cmd_t": "~command",
            "stat_t": "~state",
            "val_tpl":"{{value_json.POWER}}",
            "pl_off": self.config['General']['payload_off'],
            "pl_on": self.config['General']['payload_off'],
            "avty_t":"~availability",
            "pl_avail": self.config['General']['availability_online'],
            "pl_not_avail": self.config['General']['availability_offline'],
            "uniq_id": device_dps,
            "device":{
                "identifiers":[self.entity['deviceid']]
            },
            "~": self.mqtt_topic
        }
        print(hass_topic)
        print(payload)
"""

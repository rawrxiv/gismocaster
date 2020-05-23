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
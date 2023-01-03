from distutils.sysconfig import EXEC_PREFIX
import os
from os import environ
import stat
import threading
import time
from typing import Optional
from typing_extensions import assert_type

import flet
from flet import (
    Column,
    Container,
    ElevatedButton,
    IconButton,
    Page,
    Row,
    Text,
    Image,
    UserControl,
    border_radius,
    colors,
    Stack,
    TextField,
    AnimatedSwitcher,
    icons,
    alignment
)
import paho.mqtt.client as pmqtt
import glob
import pathlib
# import asyncio


from fletbell.const import(
    #  MQTT_CLIENT_ID
     SCREEN_HEIGHT
    ,SCREEN_WIDTH
    ,MQTT_IDENTIFIERS
    ,HOUSE_TOPICS
    ,MQTT_END
)
from fletbell.pages.controlpage import ControlPage
from fletbell.pages.mainpage import MainPage
from fletbell.utiils import cfg_loader
# from fletbell.mqtthandler import MqttHandler
from fletbell.core import (
    MqttConfig,
    DoorModel,
    GateModel,
    House,
    MqttTopics
)
from fletbell.widgets.buttons import DoorButton, GarageButton, HouseButton




class App:
    page:Page

    def __init__(self, assets_dir:str, cfg_dir:str=None, dev_mode=False):
        self.assets_dir = assets_dir
        
        ## Import cfg and set up core components
        cfg=cfg_loader(cfg_dir)
        print(cfg)
        self.mqtt = MqttConfig(**cfg['mqtt'])
        # self.doors = [DoorModel(**door, id=id, state_t=f"{MQTT_IDENTIFIERS.DOOR}/{id}/{MQTT_END.STATE}") for id, door in cfg['doors'].items()]
        self.doors = [DoorModel(**door, id=id, state_t=f"{MQTT_IDENTIFIERS.DOOR}/{id}/{MQTT_END.STATE}", button=DoorButton(door['pretty'])) for id, door in cfg['doors'].items()]
        self.gates = [GateModel(**gate, id=id, command_t=f"{MQTT_IDENTIFIERS.GATE}/{id}/{MQTT_END.COMMAND}", state_t=f"{MQTT_IDENTIFIERS.GATE}/{id}/{MQTT_END.STATE}", button=GarageButton(g_up=self.g_up, g_down=self.g_down, g_stop=self.g_stop)) for id, gate in cfg['gates'].items()]
        self.house=House(button=HouseButton(house_state=self.house_state))
        self.bell=MqttTopics(command_t=f"{MQTT_IDENTIFIERS.BELL}/toggle/{MQTT_END.COMMAND}")
        # if lockmaster_url is None:
        #    lockmaster_url=environ.get('LOCKMASTER_URL','lockmaster')
        # self._mqttc = mqtt.Client(self.mqtt.client_id)


        ## Build graphics
        self.main_page = MainPage(app=self, assets_dir=self.assets_dir, cycle_time=10)
        self.control_page = ControlPage(app=self, doors=self.doors, gates=self.gates, house=self.house)
        self.control_page.visible=False

        self.st= Stack([
            self.main_page,
            self.control_page 
        ])



        # self._mqttc = mqtt.Client(MQTT_CLIENT_ID, userdata = parameters)
        self._mqttc = pmqtt.Client(self.mqtt.client_id)
        self._mqttc.on_message = self.mqtt_on_message
        self._mqttc.on_connect = self.mqtt_on_connect
        self._mqttc.on_publish = self.mqtt_on_publish
        self._mqttc.on_subscribe = self.mqtt_on_subscribe
        # self._mqttc.on_disconnect = self.mqtt_on_disconnect
        try:
            self.mqttc_connect_to_broker()
        except Exception as e:
            print(e)
    
        print("done")

        print("INIT FISISHED")
        

    def app(self, page:Page):
        self.page=page
        self.page.horizontal_alignment = "center"
        self.page.title = "piBell"
        self.page.add(self.st)

        self.main_page.start()


    # def login(self):
    def house_state(self, *args):
        pass

    def g_up(self, *args):
        pass

    def g_down(self, *args):
        pass

    def g_stop(self, *args):
        pass


    def try_login(self, *args):
        """Dummy login"""
        print("TRY LOGIN")
        self.main_page.visible=False
        self.control_page.visible=True
        self.page.update()

        return True

    def goto_lightcontrol(self, *args):
        print(args)

    def goto_main(self, *args):
        """Dummy login"""
        print("TRY LOGIN")
        self.main_page.visible=True
        self.control_page.visible=False
        self.page.update()

        return True


    def deploy(self):
        flet.app(target=self.app, assets_dir=self.assets_dir)


        


    def mqtt_on_connect(self, mqttc, obj, flags, rc):
        print("rc: "+str(rc))
        print(f"flag: {flags}")
        self.mqttc_subscribe()
        self.mqttc_run()
        


    def mqtt_on_message(self, mqttc, obj, msg):
        print(msg.topic+" "+str(msg.qos)+" "+str(msg.payload))
        topic = msg.topic
        payload = msg.payload.decode("utf-8") 

        t_list = topic.split('/')
        if t_list[0] == MQTT_IDENTIFIERS.DOOR:
            if t_list[2] == MQTT_END.STATE:
                self.set_door_state(t_list[1], payload)

        elif t_list[0] == MQTT_IDENTIFIERS.GATE:
            if t_list[2] == MQTT_END.STATE:
                self.set_gate_state(t_list[1], payload)

        elif t_list[0] == MQTT_IDENTIFIERS.HOUSE:
            if t_list[2] == MQTT_END.COMMAND:
                if t_list[1] == HOUSE_TOPICS.PARTYMODE:
                    self.set_partymode(payload)
                elif t_list[1] == HOUSE_TOPICS.STATE:
                    self.set_house_state(payload)



        # door = self.doors_config.get_by_state_topic(topic)
        # if door is not None:
        #     print(f"state received")
        #     if payload == DOORLOCK_STATE.LOCKED:
        #         door.state="LOCKED"
        #         self.screens['Control']["object"].update_door_states(door.door_id,True)
                
        #     elif payload == DOORLOCK_STATE.UNLOCKED:
        #         door.state="UNLOCKED"
        #         self.screens['Control']["object"].update_door_states(door.door_id, False)


    def set_partymode(self, mode):
        pass


    def set_house_state(self, state):
        pass



    def set_door_state(self, id, state):
        pass



    def set_gate_state(self, id, state):
        pass


    def mqtt_on_publish(self, mqttc, obj, mid):
        print("mid: "+str(mid))

    def mqtt_on_subscribe(self, mqttc, obj, mid, granted_qos):
        print("Subscribed: "+str(mid)+" "+str(granted_qos))

    def mqtt_on_log(self, mqttc, obj, level, string):
        print(string)

    def tls_set(self):
        #TODO: sett ssl and cert for encrypt
        pass

    def mqttc_connect_to_broker(self):
        print(f"connecting to broker {self.mqtt.broker_url} as {self.mqtt.client_id}")
        # broker_parsed = urllib.parse.urlparse(MQTT_BROKER)
        try:
            self._mqttc.username_pw_set(self.mqtt.username, password=self.mqtt.password)
            self._mqttc.connect(self.mqtt.broker_url, port=self.mqtt.broker_port, keepalive=60)
        except Exception as e:
            print(e)
            self._mqttc = None


    def mqttc_subscribe(self):
        for door in self.doors:
            self._mqttc.subscribe(door.state_t, qos=self.mqtt.qos)
        for garage in self.garages:
            self._mqttc.subscribe(garage.state_t, qos=self.mqtt.qos)
        self._mqttc.subscribe(self.house.partymode.state_t, qos=self.mqtt.qos)
        self._mqttc.subscribe(self.house.state.state_t, qos=self.mqtt.qos)




    def mqttc_run(self):
        if self._mqttc is not None:
            self._mqttc.loop_start()



    # def ring_bell(self):
    #     print('ringing that bell')
    #     print(f'self.mode_config.state: {self.mode_config.state}')
    #     self._mqttc.publish(self.bell_config.command_topic, payload=BELL_COMMAND_PAYLOAD.DO)
    #     if self.mode_config.state == MODE_COMMAND_PAYLOAD.NORMAL:
    #         pass
    #     elif self.mode_config.state == MODE_COMMAND_PAYLOAD.HALLOWEEN:
    #        self.change_screen('Scary')




    def toggle_state(self, *args):
        print(f"Toggle state: {args}")
  
        
    # def garage_open(self, *args):
    #     self.garage_command(GARAGE_COMMAND_PAYLOAD.OPEN)

    # def garage_close(self, *args):
    #     self.garage_command(GARAGE_COMMAND_PAYLOAD.CLOSE)

    # def garage_stop(self, *args):
    #     self.garage_command(GARAGE_COMMAND_PAYLOAD.STOP)

    # def garage_command(self, command):
    #     self._mqttc.publish(self.garage_config.command_topic, payload=command)

    # def next_screen(self):
    #     self.change_screen(self.gui.next())

    # def prev_screen(self):
    #     self.change_screen(self.gui.previous())

    # def change_screen(self, screen_name):
    #     if screen_name == 'Control':
    #         self.start_screen_timer()
    #     self.gui.current = screen_name
from http.client import LOCKED
from pydantic import BaseModel
from pydantic import BaseModel
from typing import Callable, Optional, List, Dict
from os import environ



from fletbell.const import MQTT_IDENTIFIERS, HOUSE_TOPICS, MQTT_END
from fletbell.widgets.buttons import DoorButton, GarageButton, HouseButton

class MqttTopics(BaseModel):
    command_t: Optional[str]
    state_t: Optional[str]

class MqttConfig(BaseModel):
    client_id: str=environ.get('MQTT_CLIENT_ID','mqtt')
    broker_port: int=int(environ.get('MQTT_PORT',1883))
    broker_url: str =environ.get('MQTT_BROKER','mqtt')
    username: str=environ.get('MQTT_USERNAME','mqtt')
    password: str =environ.get('MQTT_PASSWORD','mqtt')
    qos: int =environ.get('MQTT_QOS',0)
    ssl: bool =environ.get('MQTT_SSL',False)

class APIConfig(BaseModel):
    url: str



class DoorModel(MqttTopics):
    id: str
    pretty: str
    locked: bool = False
    button: Optional[DoorButton]

    class Config():
        arbitrary_types_allowed=True

    # def make_gui(self):
    #     self.button=DoorButton(self.pretty)

        

class GateModel(MqttTopics):
    pretty: str
    closed: bool = True
    moving: bool = False
    button: Optional[GarageButton]

    class Config():
        arbitrary_types_allowed=True

    # def make_gui(self):
    #     self.button=DoorButton(self.pretty)



class Memory(BaseModel):
    doors: List[DoorModel]
    gates: List[GateModel]

# class Bell(MqttTopics):

    # def __init__(self, **kwargs):
    #     super().__init__(**kwargs)

class PartyMode(MqttTopics):
    current: str = "Unknown"


class HouseState(MqttTopics):
    current: str = "Unknown"


     

class House(BaseModel):
    partymode:PartyMode=PartyMode(command_t=f"{MQTT_IDENTIFIERS.HOUSE}/{HOUSE_TOPICS.PARTYMODE}/{MQTT_END.COMMAND}", state_t=f"{MQTT_IDENTIFIERS.HOUSE}/{HOUSE_TOPICS.PARTYMODE}/{MQTT_END.STATE}")
    state: HouseState=HouseState(command_t=f"{MQTT_IDENTIFIERS.HOUSE}/{HOUSE_TOPICS.STATE}/{MQTT_END.COMMAND}", state_t=f"{MQTT_IDENTIFIERS.HOUSE}/{HOUSE_TOPICS.STATE}/{MQTT_END.STATE}")
    button: Optional[HouseButton]
    class Config():
        arbitrary_types_allowed=True

# class Config():
#     mqtt: MqttConfig
#     lockmaster_url: str 
#     doors: List[DoorModel]
#     gates: List[GateModel]
#     house:House
#     bell:MqttTopics


#     def __init__(self, mqtt, doors, gates, lockmaster_url=None):
#         self.mqtt = MqttConfig(**mqtt)
#         self.doors = [DoorModel(**door, id=id, state_t=f"{MQTT_IDENTIFIERS.DOOR}/{id}/{MQTT_END.STATE}") for id, door in doors.items()]
#         self.gates = [GateModel(**gate, id=id, command_t=f"{MQTT_IDENTIFIERS.GATE}/{id}/{MQTT_END.COMMAND}", state_t=f"{MQTT_IDENTIFIERS.GATE}/{id}/{MQTT_END.STATE}") for id, gate in gates.items()]
#         self.house=House()
#         self.bell=MqttTopics(command_t=f"{MQTT_IDENTIFIERS.BELL}/toggle/{MQTT_END.COMMAND}")
#         if lockmaster_url is None:
#            lockmaster_url=environ.get('LOCKMASTER_URL','lockmaster')
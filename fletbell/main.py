import os
import threading
import time

import flet
from flet import (
    Column,
    Container,
    ElevatedButton,
    Page,
    Row,
    Text,
    Image,
    UserControl,
    border_radius,
    colors,
    Stack,
    TextField,
)
import paho.mqtt.client as mqtt

from fletbell.const import(
     SCREEN_TIMER
    ,LOGOUT_TIMER
    ,BELL_COMMAND_PAYLOAD
    ,GARAGE_COMMAND_PAYLOAD
    ,MODE_COMMAND_PAYLOAD
    ,MQTT_BROKER
    ,MQTT_CLIENT_ID
)
from fletbell.calculator import CalculatorApp




class ImgCarousell(UserControl):
    images = ["familie/1.png",
            "familie/2.png",
            "familie/3.png",]
            
    def build(self):
        print("building")
        self.current_img = 0
        self.img = Image(
                    src=self.images[self.current_img],
                    width=300,
                    height=300,
                    fit="contain",
                )
        # application's root control (i.e. "view") containing all other controls
        return Container(
                on_click=self.onclick,
                content=self.img)
                
    def onclick(self, e):
        print(e)
        
        self.current_img+=1
        if self.current_img>len(self.images)-1:
            self.current_img=0
        
        self.img = Image(
                    src=self.images[self.current_img],
                    width=300,
                    height=300,
                    fit="contain",
                )
        txt_number=str(self.current_img)
        print(f"cycle {self.current_img}")
        print(f"cycle {self.images[self.current_img]}")
        print(f"cycle {self.img}")
        self.update()

    def update(self):
        super().update()



class Test():
    
    page:Page

    def main(self, page:Page):
        self.page=page
        self.page.horizontal_alignment = "center"
        print("MAIN")
        _mqttc = mqtt.Client(MQTT_CLIENT_ID)
        
        self.page.title = "Calc App"
        self.page.update()
        txt_number = TextField(value="0", text_align="right", width=100)
        calcpage = CalculatorApp()
        carousell = ImgCarousell()

        self.page.add(txt_number)
        self.page.add(calcpage)
        self.page.add(carousell)




        # create application instance
        # add application's root control to the page


    # def cycle(current_img):
    # while True:


    # x=threading.Thread(target=cycle, args=(current_img))
    # x.start()

    def run(self):
        flet.app(target=self.main, assets_dir="/assets")


# class BellApp():

#     def __init__(self):
#         self.main()

#     def main(self, page:Page=Page):

#         _mqttc = mqtt.Client(MQTT_CLIENT_ID)

#         page.title = "Calc App"
#         # create application instance
#         calcpage = CalculatorApp()

#         # add application's root control to the page
#         page.add(calcpage)

#     def run(self):
#         flet.app(target=self.main)
import os
import stat
import threading
import time
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
import paho.mqtt.client as mqtt
import glob
import pathlib


from fletbell.const import(
     SCREEN_HEIGHT
    ,SCREEN_WIDTH
)
from fletbell.pages.pinpad import PinPad




class ImgCarousell(UserControl):

    @staticmethod
    def _find_family_files(assets_dir):
        print(assets_dir)
        if not assets_dir.startswith("/"):
            x = assets_dir.split("/")
            family_path=pathlib.Path().parent.resolve()
            print(family_path)
            for p in x:
                if p == "..":
                    family_path = family_path.parent
                else:
                    family_path = family_path / p
                print(family_path)
        else:
            family_path =pathlib.Path(assets_dir)
        family_path= family_path/"family"
        
        return [f"family/{os.path.basename(x)}" for x in list(family_path.glob("*.png"))+ list(family_path.glob("*.jpg"))]


    def __init__(self, app, parent, assets_dir, cycle_time=60):
        super().__init__()
        self.family_files=self._find_family_files(assets_dir)
        self.app = app
        self.parent = parent
        self.current_img = 0
        self.cycle_time = cycle_time
        i = Image(
            src=self.family_files[self.current_img],
            width=300,
            height=300,
            fit="contain",
        )
        self.sw = AnimatedSwitcher(
                i,
                transition="scale",
                duration=0,
                reverse_duration=0,
                # switch_in_curve="linear",
                # switch_out_curve="linear",
            )

    def build(self):
        print("building")

        # application's root control (i.e. "view") containing all other controls
      
        return Container(
                # on_click=self.cycle,
                on_long_press=self.parent.show_login,
                content=self.sw)


            
    def start(self):
        t = threading.Thread(self.cycle_t())


         
    def cycle(self, *e):
        print(e)
    
        self.current_img+=1
        if self.current_img>len(self.family_files)-1:
            self.current_img=0
        
        self.sw.content = Image(
                    src=self.family_files[self.current_img],
                    width=SCREEN_HEIGHT,
                    height=SCREEN_HEIGHT,
                    fit="contain",
                )
        self.update()


    def cycle_t(self):
        while True:
            self.cycle()
            time.sleep(self.cycle_time)


    # def update(self):
    #     super().update()



class Bell(UserControl):


    def __init__(self, app, parent):
        super().__init__()
        self.app = app
        self.parent = parent

    def build(self):
        return  Container(
                    alignment=alignment.center,
                    bgcolor=colors.AMBER,
                    width=SCREEN_WIDTH-SCREEN_HEIGHT,
                    height=SCREEN_HEIGHT,
                    content=IconButton(
                        icon=icons.DOORBELL,
                        icon_color="blue400",
                        icon_size=100,
                        tooltip="Pause record",
                        on_click=self.app.try_login
                    )
                )

        
class MainPage(UserControl):
    def __init__(self, app, assets_dir, cycle_time=60):
        super().__init__()
        self.app = app
        self.carousell = ImgCarousell(app=app, parent=self, assets_dir=assets_dir, cycle_time=10)
        self.bell = Bell(app=app, parent=self)
        self.pinpad = PinPad(app=app, parent=self)
        self.pinpad.visible=False
        self.st = Stack(
        [
            self.carousell,
            self.pinpad 
        ],)
        self.row = Row(spacing=0, controls=[self.st, self.bell])

    def build(self):
        return  Container(
            width=SCREEN_WIDTH,
            height=SCREEN_HEIGHT,
            content=self.row)

    def start(self):
        self.carousell.start()


    def show_login(self, *args):
        print("Show Login")
        self.bell.visible = False
        self.pinpad.visible=True
        self.update()
        # super().update()

    def hide_login(self, *args):
        print("Show Login")
        self.bell.visible = True
        self.pinpad.visible=False
        self.update()
        # super().update()




    



    # def main_to_login(self, *args):
    #     print("goto login")
    #     self.page.controls.remove(self.main_page)
    #     self.page.update()
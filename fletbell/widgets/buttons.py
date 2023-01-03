from typing import Callable
from flet import (
    ElevatedButton,
    FloatingActionButton,
    IconButton,
    colors,
    icons,
    UserControl,
    Row,
    Column,
)



class DoorButton(FloatingActionButton):
    def __init__(self, text, **kwargs):
        super().__init__(**kwargs)
        # self.on_click=self.parent.key_press
        self.icon=icons.LOCK_OPEN_ROUNDED
        self.icon_color="blue400"
        self.icon_size=20
        self.tooltip="Toggle lock"
        self.locked=False
        self.text=text

    def update(self):
        if self.locked == True:
            self.icon=icons.LOCK_OUTLINE_ROUNDED
        else:
            self.icon=icons.LOCK_OPEN_ROUNDED



class GarageButton(UserControl):
    def __init__(self, g_up:Callable, g_down:Callable, g_stop:Callable, **kwargs):
        super().__init__(**kwargs)
        # self.on_click=self.parent.key_press
        self.icon=icons.LOCK_OPEN_ROUNDED
        self.icon_color="blue400"
        self.icon_size=20
        self.tooltip="Toggle gate"
        self.uo=False
        self.moving=False
        self.g_up = g_up
        self.g_down = g_down
        self.g_stop = g_stop

    
    def build(self):
        return Row(controls=[IconButton(
                            icon=icons.ARROW_CIRCLE_UP_OUTLINED,
                            bgcolor=colors.WHITE,
                            on_click=self.g_up
                            # color=colors.WHITE,
                            # expand=1,
                        ),
                        IconButton(
                            icon=icons.STOP_CIRCLE_OUTLINED,
                            bgcolor=colors.WHITE,
                            on_click=self.g_stop
                            # color=colors.WHITE,
                            # expand=1,
                        ),
                        IconButton(
                            icon=icons.ARROW_CIRCLE_DOWN_OUTLINED,
                            bgcolor=colors.WHITE,
                            on_click=self.g_down
                            # color=colors.WHITE,
                            # expand=1,
                        )
                        ],alignment="start")




class HouseButton(UserControl):
    def __init__(self, house_state:Callable, **kwargs):
        super().__init__(**kwargs)
        # self.on_click=self.parent.key_press
        self.icon=icons.LOCK_OPEN_ROUNDED
        self.icon_color="blue400"
        self.icon_size=20
        self.tooltip="Set house state"
        self.house_state = house_state

    

    
    def build(self):
        return Column(controls=[FloatingActionButton(
                            icon=icons.OTHER_HOUSES_OUTLINED,
                            text="Forlat hus",
                            bgcolor=colors.WHITE,
                            on_click=self.house_state
                            # color=colors.WHITE,
                            # expand=1,
                        ),
                        FloatingActionButton(
                            icon=icons.HOUSE_ROUNDED,
                            text="Kom hjem",
                            bgcolor=colors.WHITE,
                            on_click=self.house_state
                            # color=colors.WHITE,
                            # expand=1,
                        ),
                        FloatingActionButton(
                            icon=icons.AIRPLANEMODE_ACTIVE,
                            text="Dra på ferie",
                            bgcolor=colors.WHITE,
                            on_click=self.house_state
                            # color=colors.WHITE,
                            # expand=1,
                        )
                        ],alignment="start")

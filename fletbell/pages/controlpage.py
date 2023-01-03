from gc import garbage
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
    alignment,
    Icon,
)
import paho.mqtt.client as mqtt
import glob
import pathlib


from fletbell.const import(
     SCREEN_HEIGHT
    ,SCREEN_WIDTH
)

from fletbell.widgets.buttons import HouseButton


# class DoorControl(UserControl):
#     def __init__(self, doors, gates):
#         super().__init__()
#         self.doors=doors
#         self.gates=gates


#     def build(self):
#         return Column(
#             alignment="start",
#             controls=[
#                 Row(controls=[IconButton(
#                             icon=icons.EXIT_TO_APP,
#                             bgcolor=colors.WHITE24,
#                             on_click=self.exit
#                             # color=colors.WHITE,
#                             # expand=1,
#                         ),
#                         IconButton(
#                             icon=icons.EXIT_TO_APP,
#                             bgcolor=colors.WHITE24,
#                             on_click=self.exit
#                             # color=colors.WHITE,
#                             # expand=1,
#                         )],alignment="start"),

#                 Row(
#                     controls=[
#                         IconButton(
#                             icon=icons.KEYBOARD_BACKSPACE,
#                             bgcolor=colors.WHITE24,
#                             # color=colors.WHITE,
#                             expand=1,
#                             on_click=self.exit
#                         ),
#                         IconButton(
#                             icon=icons.LOGIN,
#                             bgcolor=colors.WHITE24,
#                             # color=colors.WHITE,
#                             expand=1,
#                             on_click=self.exit
#                         ),
#                     ]
#                 ),]
#         )   
        
class ControlPage(UserControl):
    def __init__(self, app, doors, gates, house):
        super().__init__()
        self.app = app
        self.doors=doors
        self.gates=gates
        self.house=house
        # for door in self.doors:
        #     door.make_gui()

        # self.doors_row=Row(controls=[door.button for door in self.doors],alignment="start"),

    def exit(self, e):
        print(self)
        self.app.goto_main()

    def build(self):
        # application's root control (i.e. "view") containing all other controls
        return Container(
            width=SCREEN_WIDTH,
            height=SCREEN_HEIGHT,
            bgcolor=colors.WHITE24,
            opacity=1,
            # border_radius=border_radius.all(20),
            padding=0,
            # alignment=alignment.START,
            content=Column(
                    controls=[
                        Container(
                            width=SCREEN_WIDTH,
                            height=20,
                            bgcolor=colors.WHITE24,
                            opacity=1,
                            # border_radius=border_radius.all(20),
                            padding=0,
                            # alignment=alignment.START,
                            content=Row(       
                                controls=[IconButton(
                                        icon=icons.EXIT_TO_APP,
                                        bgcolor=colors.WHITE24,
                                        on_click=self.exit
                                        # color=colors.WHITE,
                                        # expand=1,
                                    ),
                                    IconButton(
                                        icon=icons.LIGHT_OUTLINED,
                                        bgcolor=colors.WHITE24,
                                        on_click=self.app.goto_lightcontrol
                                        # color=colors.WHITE,
                                        # expand=1,
                                    )],alignment="start"),),
                        Row(controls=[
                            Container(
                                width=SCREEN_HEIGHT,
                                height=SCREEN_HEIGHT-20,
                                bgcolor=colors.WHITE24,
                                opacity=1,
                                # border_radius=border_radius.all(20),
                                padding=0,
                                # alignment=alignment.START,
                                content=Column(
                                    controls=[
                                        Row(controls=[  Icon(name=icons.DOOR_FRONT_DOOR_OUTLINED, color=colors.PINK, size=200),
                                                        Column(
                                                        controls=[door.button for door in self.doors]
                                                            )],
                                            ),
                                        Row(controls=[  Icon(name=icons.GARAGE_OUTLINED, color=colors.PINK, size=200),
                                                        Column(controls=[gate.button for gate in self.gates]),
                                                    ],
                                            ),]
                                    ),),
                                self.house.button,
                                ])
                    ]
                )
        )

from turtle import onclick
import flet
from flet import (
    Column,
    Container,
    ElevatedButton,
    Page,
    Row,
    Text,
    UserControl,
    border_radius,
    colors,
    IconButton,
    icons,
)
from typing import List
from functools import partial

from fletbell.const import(
     SCREEN_HEIGHT
    ,SCREEN_WIDTH
    ,PIN_SIZE
)

def blank_key(): return ["_" for x in range(PIN_SIZE)]

class PinButton(ElevatedButton):
    def __init__(self, parent, key):
        super().__init__()
        self.parent=parent
        self.key=key
        self.text=f"{key}"
        self.bgcolor=colors.WHITE24
        self.color=colors.WHITE
        self.expand=1
        self.on_click=self.parent.key_press


class PinPad(UserControl):
    key:List = blank_key()
    key_text:List

    def __init__(self, app, parent):
        super().__init__()
        self.app=app
        self.parent=parent
        self.idx=0
        self.generate_key_text()


        self.c = Container(
            width=SCREEN_HEIGHT,
            height=SCREEN_HEIGHT,
            bgcolor=colors.TRANSPARENT,
            opacity=1,
            border_radius=border_radius.all(20),
            padding=20,
            content=Column(
                controls=[
                    Row(controls=[IconButton(
                                icon=icons.EXIT_TO_APP,
                                bgcolor=colors.WHITE24,
                                on_click=self.hide_login
                                # color=colors.WHITE,
                                # expand=1,
                            )],alignment="start"),
                    Row(controls=self.key_text, alignment="center"),
                    Row(
                        controls=[
                            PinButton(
                                parent=self,
                                key=7
                            ),
                            PinButton(
                                parent=self,
                                key=8
                            ),
                            PinButton(
                                parent=self,
                                key=9
                            ),
                        ]
                    ),
                    Row(
                        controls=[
                            PinButton(
                                parent=self,
                                key=4
                            ),
                            PinButton(
                                parent=self,
                                key=5
                            ),
                            PinButton(
                                parent=self,
                                key=6
                            ),
                        ]
                    ),
                    Row(
                        controls=[
                            PinButton(
                                parent=self,
                                key=1
                            ),
                            PinButton(
                                parent=self,
                                key=2
                            ),
                            PinButton(
                                parent=self,
                                key=3
                            ),
                        ]
                    ),
                    Row(
                        controls=[
                            IconButton(
                                icon=icons.KEYBOARD_BACKSPACE,
                                bgcolor=colors.WHITE24,
                                # color=colors.WHITE,
                                expand=1,
                                on_click=self.backspace
                            ),
                            PinButton(
                                parent=self,
                                key=0
                            ),
                            IconButton(
                                icon=icons.LOGIN,
                                bgcolor=colors.WHITE24,
                                # color=colors.WHITE,
                                expand=1,
                                on_click=self.try_login
                            ),
                        ]
                    ),
                ]
            ),
        )


    def clean_key(self):
        self.key = blank_key()
        self.idx = 0
        print(self.key)
        self.update_key_row()

    # @staticmethod
    def generate_key_text(self):
        self.key_text = [Text(value=x, color=colors.WHITE, size=50) for x in self.key]

    def update_key_row(self):
        self.generate_key_text()
        self.update()
        print(self.key)
        print(self.key_text)

    def key_press(self, e):
        if self.idx < PIN_SIZE:
            self.key[self.idx]=e.control.key
            self.update_key_row()
            self.idx=min(self.idx+1,PIN_SIZE)
    
    def update(self):
        # self.controls[0].content.controls[1].controls = self.key_text
        self.c.content.controls[1].controls = self.key_text
        super().update()


    def backspace(self, e):
        if self.idx == PIN_SIZE:
            self.idx=PIN_SIZE-1
        if self.idx >= 0:
            self.key[self.idx]="_"
            self.idx=max(self.idx-1,0)
            self.update_key_row()
            self.update()

    def hide_login(self, e):
        print("HIDE LOGIN")
        self.clean_key()
        self.parent.hide_login()

    def try_login(self, e):
        print("HIDE LOGIN")
        success = self.app.try_login()
        if success:
            self.clean_key()
            self.parent.hide_login()

    def build(self):
        # application's root control (i.e. "view") containing all other controls
        return self.c
        # Container(
        #     width=SCREEN_HEIGHT,
        #     height=SCREEN_HEIGHT,
        #     bgcolor=colors.TRANSPARENT,
        #     opacity=1,
        #     border_radius=border_radius.all(20),
        #     padding=20,
        #     content=Column(
        #         controls=[
        #             Row(controls=[IconButton(
        #                         icon=icons.EXIT_TO_APP,
        #                         bgcolor=colors.WHITE24,
        #                         on_click=self.hide_login
        #                         # color=colors.WHITE,
        #                         # expand=1,
        #                     )],alignment="start"),
        #             Row(controls=self.key_text, alignment="center"),
        #             Row(
        #                 controls=[
        #                     PinButton(
        #                         parent=self,
        #                         key=7
        #                     ),
        #                     PinButton(
        #                         parent=self,
        #                         key=8
        #                     ),
        #                     PinButton(
        #                         parent=self,
        #                         key=9
        #                     ),
        #                 ]
        #             ),
        #             Row(
        #                 controls=[
        #                     PinButton(
        #                         parent=self,
        #                         key=4
        #                     ),
        #                     PinButton(
        #                         parent=self,
        #                         key=5
        #                     ),
        #                     PinButton(
        #                         parent=self,
        #                         key=6
        #                     ),
        #                 ]
        #             ),
        #             Row(
        #                 controls=[
        #                     PinButton(
        #                         parent=self,
        #                         key=1
        #                     ),
        #                     PinButton(
        #                         parent=self,
        #                         key=2
        #                     ),
        #                     PinButton(
        #                         parent=self,
        #                         key=3
        #                     ),
        #                 ]
        #             ),
        #             Row(
        #                 controls=[
        #                     IconButton(
        #                         icon=icons.KEYBOARD_BACKSPACE,
        #                         bgcolor=colors.WHITE24,
        #                         # color=colors.WHITE,
        #                         expand=1,
        #                         on_click=self.backspace
        #                     ),
        #                     PinButton(
        #                         parent=self,
        #                         key=0
        #                     ),
        #                     IconButton(
        #                         icon=icons.LOGIN,
        #                         bgcolor=colors.WHITE24,
        #                         # color=colors.WHITE,
        #                         expand=1,
        #                         on_click=self.try_login
        #                     ),
        #                 ]
        #             ),
        #         ]
        #     ),
        # )
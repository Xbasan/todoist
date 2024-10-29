import requests

from kivy.uix.widget import Widget

from kivymd.uix.button import MDButton, MDButtonText
from kivymd.uix.dialog import (
    MDDialog,
    MDDialogIcon,
    MDDialogHeadlineText,
    MDDialogSupportingText,
    MDDialogButtonContainer,
    MDDialogContentContainer,
)

from kivymd.uix.divider import MDDivider

class Dialog(MDDialog):
    def __init__(self, message ="", icon="alert-circle-outline", **kw):
        super().__init__(**kw)

        dialog_icon =  MDDialogIcon(
            icon=icon
        )

        title_dialog = MDDialogHeadlineText(
            text = f""" { message } """
        )

        dialog_container = MDDialogContentContainer(
            MDDivider(),
        )

        dialog_btn = MDDialogButtonContainer(
            Widget(),
            MDButton(
                MDButtonText(text="OK"),
                on_release=self.close_dialog,
                
            ),
            spacing="8dp"
        )

        self.add_widget(dialog_icon)
        self.add_widget(title_dialog)
        self.add_widget(dialog_container)
        self.add_widget(dialog_btn)

    def close_dialog(self, *args):
        self.dismiss()


class Dialog_unfolded_sheet(MDDialog):
    def __init__(self, date={}, **kw):
        super().__init__(** kw)

        self.__tiele = date["title"]
        self.__text = date["text"]
        self.__id = date["id"]
        self.__date = date["date"]

        dealog_icon = MDDialogIcon(
            icon="bowling"
        )

        title_list = MDDialogHeadlineText(
            text = self.__tiele
        )

        dialog_container = MDDialogContentContainer(
            MDDivider(),
            MDDialogSupportingText( text = str(self.__date)),
            MDDialogSupportingText( text = self.__text ),
            MDDivider(),
            orientation="vertical",
        )

        btn = MDDialogButtonContainer(
            MDButton(
                MDButtonText( text= "Выполнепо"),
                on_release=self.drop
            ),
            MDButton(
                MDButtonText( text= "Закрыть"),
                on_release=self.close,
            ),
            spacing = "20dp",
        )

        self.add_widget(dealog_icon)
        self.add_widget(title_list)
        self.add_widget(dialog_container)
        self.add_widget(btn)
        

    def close(self, *args):
        self.dismiss()

    def drop(self, *args):
        res  = requests.post("http://192.168.1.10:5000/api?del", json={"id":f"{ self.__id }"})

        if res.ok:
            Dialog("Задача успешна закрыта", "charity")


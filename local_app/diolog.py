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

from Data_b import delete_list

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
        self.__time = date["time"]

        title_list = MDDialogHeadlineText(
            text = self.__tiele
        )

        dialog_container = MDDialogContentContainer(
            MDDialogSupportingText( text = f"Дата { str(self.__date) }, время { str(self.__time) }"),
            MDDialogSupportingText( text = self.__text ),
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

        self.add_widget(title_list)
        self.add_widget(dialog_container)
        self.add_widget(btn)        

    def close(self, *args):
        self.dismiss()

    def drop(self, *args):
        delete_list(self.__id)
        self.dismiss()



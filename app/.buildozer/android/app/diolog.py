from kivy.uix.widget import Widget

from kivymd.uix.button import MDButton, MDButtonText
from kivymd.uix.dialog import (
    MDDialog,
    MDDialogIcon,
    MDDialogHeadlineText,
    MDDialogSupportingText,
    MDDialogButtonContainer,
    MDDialogContentContainer
)

from kivymd.uix.divider import MDDivider

class Dialog(MDDialog):
    def __init__(self, message ="", icon="alert-circle-outline", **kw):
        super().__init__(** kw)

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

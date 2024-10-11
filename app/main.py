import requests

from kivy.properties import StringProperty
from kivy.lang import Builder
# from kivy.uix.slider import Slider

from kivymd.app import MDApp

from kivymd.uix.floatlayout import FloatLayout
from kivymd.uix.button import (
    MDButton, 
    MDButtonIcon)
from kivymd.uix.list import (
    MDList,
    MDListItem,
    MDListItemHeadlineText,
    MDListItemSupportingText
)
from kivymd.uix.textfield import (
    MDTextField,
    MDTextFieldHintText,
    MDTextFieldMaxLengthText
)
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.navigationbar import (
    MDNavigationBar,
    MDNavigationItem,
    MDNavigationItemIcon,
    MDNavigationItemLabel
)
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.label import MDLabel
from kivymd.uix.screen import MDScreen

from diolog import Dialog


class ListItem(MDListItem):
    def __init__(self, res_json, e, **kw):
        super().__init__(**kw)

        tit = f"""{str(e+1)} | {res_json["title"]}"""
        
        title = MDListItemHeadlineText(
                                       text=tit
                                   )
        text = MDListItemSupportingText(
                                      text=res_json["text"]
                                  )

        btn_del = MDButton(
            MDButtonIcon(
                icon="close-circle-outline"
            ),
            on_press=lambda instance: self.del_(id=res_json["id"], instance=instance)
        )

        self.add_widget(title)
        self.add_widget(text)
        self.add_widget(btn_del)
        self.md_bg_color=self.theme_cls.backgroundColor

        
    def del_(self, id, instance=""):
        res = requests.post("http://192.168.1.10:5000/api?del", json={"id":f"{id}"})
            


class MainLists(MDList):
    def __init__(self, **kw):
        super().__init__(**kw)

        self.id = "Lists"
                
        res = requests.post("http://192.168.1.10:5000/api?list")

        if res.ok:
            for e, li in enumerate(res.json()):
                list_item = ListItem(e=e, res_json=li)

                self.add_widget(list_item)


class ScrollView(MDScrollView):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.size_hint=(1, 1)

        self.width = 100
        self.height = 100

        message = "Нет доступа к серверу" 

        try:
            self.add_widget(MainLists())
    
        except Exception:
            Dialog(message=message).open()

         
class BaseScreen(MDScreen):
    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)

        btn_update = MDButton(
            MDButtonIcon(
                icon="update"
            ),
            pos_hint={"center_x":.9, "center_y":.9},
            on_press=self.update
        )

        # self.add_widget(ScrollView(MainLists()))
        self.add_widget(btn_update)

        self.update()

    def update(self, instance=""):        
        self.add_widget(ScrollView())        


    def remove_element(self, id):
        for child in self.children:
            if child.id == id:
                self.remove_widget(child)
                break                   


class CreateListScreen(MDScreen):
    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)

        self.input_title = MDTextField(
            MDTextFieldHintText(
                text="Enter title"
            ),
            MDTextFieldMaxLengthText(
                max_text_length=90
            ),
             pos_hint = {"center_x":.5, "center_y":.9},
        )

        self.input_text = MDTextField(
            MDTextFieldHintText(
                text="Enter text"
            ),
            MDTextFieldMaxLengthText(
                max_text_length=255
            ),
            pos_hint={"center_x":.5, "center_y":.7}
        )

        btn_creat_list = MDButton(
            MDButtonIcon(
                icon="pencil-circle"
            ),
            pos_hint={"center_x":.9, "center_y":.4},
            on_press=self.creatу_btn
        )
        
        self.add_widget(self.input_title)
        self.add_widget(self.input_text)
        self.add_widget(btn_creat_list)

    def creatу_btn(self, instance=""):
        title = self.input_title.text
        text = self.input_text.text

        self.input_title.text = ""
        self.input_text.text = ""

        try:
            res = requests.post("http://192.168.1.10:5000/api?insert", json={"title":title, "text":text})
            if res.json()["status"] == "true":
                message = """ Все по кайфу """
                icon = "check-underline"
                Dialog(message=message,icon=icon).open()
        except Exception:
            message =  """ Сори проблемы с подключением """
            Dialog(message=message).open()            

            
class BaseMDNavigationItem(MDNavigationItem):
    icon = StringProperty()
    text = StringProperty()

    def __init__(self, *args, **kw):
        super().__init__(self, *args, **kw)
        self.add_widget(MDNavigationItemIcon(icon=self.icon))
        self.add_widget(MDNavigationItemLabel(text=self.text))

class To_do_listApp(MDApp):
    def on_switch_tabs(
        self,
        bar: MDNavigationBar,
        item: MDNavigationItem,
        item_icon: str,
        item_text: str,
    ):
        self.root.get_ids().screen_manager.current = item_text
        

    def build(self):
        self.theme_cls.theme_style = "Dark"
        
        return MDBoxLayout(
            MDScreenManager(
                BaseScreen(
                    name="List",
                ),
                CreateListScreen(
                    name="New EL",
                ),
                id="screen_manager"
            ),
            MDNavigationBar(
                BaseMDNavigationItem(
                    icon="clipboard-list-outline",
                    text="List",
                    active=True,
                ),
                BaseMDNavigationItem(
                    icon="playlist-edit",
                    text="New EL",
                ),
                on_switch_tabs=self.on_switch_tabs,
            ),
            orientation="vertical",
            md_bg_color=self.theme_cls.backgroundColor,
        )


To_do_listApp().run()


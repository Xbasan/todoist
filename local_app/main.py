import datetime

from kivy.properties import StringProperty
from kivy.clock import Clock
# from kivy.uix.slider import Slider

from kivymd.app import MDApp

from kivymd.uix.button import (
    MDButton, 
    MDButtonIcon,
    MDButtonText
)
from kivymd.uix.list import (
    MDList,
    MDListItem,
    MDListItemTertiaryText,
    MDListItemHeadlineText,
    MDListItemSupportingText
)
from kivymd.uix.textfield import (
    MDTextField,
    MDTextFieldHintText,
    MDTextFieldHelperText,
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
from kivymd.uix.pickers import (
    MDModalDatePicker,
    MDModalInputDatePicker    
)
from kivymd.uix.pickers import MDTimePickerDialVertical


from diolog import (
    Dialog,
    Dialog_unfolded_sheet
)

from Data_b import (
    list_json,
    select_list,
    inser_list
)


class ListItem(MDListItem):
    def __init__(self, res_json, e, **kw):
        super().__init__(**kw)

        title = MDListItemHeadlineText(text=f"""{ str(e+1) } | { res_json["title"] }""")        
        text = MDListItemSupportingText(text=res_json["text"])
        date = MDListItemTertiaryText(text=str(res_json["date"]))
        btn_del = MDButton(
            MDButtonIcon(icon="close-circle-outline"),
            MDButtonText(text="details"),
            on_press=lambda instance: self._del(date=res_json, instance=instance)
        )

        self.add_widget(title)
        self.add_widget(text)
        self.add_widget(date)
        self.add_widget(btn_del)
        self.md_bg_color=self.theme_cls.backgroundColor
        
    def _del(self, date, instance=""):
        Dialog_unfolded_sheet(date=date).open()
            


class MainLists(MDList):
    def __init__(self, **kw):
        super().__init__(**kw)

        self.id = "Lists"

        res = list_json(select_list())
        
        for e, li in enumerate(res):    
            list_item = ListItem(e=e, res_json=li)
            self.add_widget(list_item)
            
        self.add_widget(MDListItem())

        
class ScrollView(MDScrollView):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.size_hint=(1, 1)

        self.id = "Scroll_lists"
        self.padding = "10dp"
        self.width = 100
        self.height = 100
        
        self.pos_hint = {"center_x":.5, "center_y":.4} 

        self.add_widget(MainLists())


class BaseScreen(MDScreen):
    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        
        btn_update = MDButton(
            MDButtonIcon(
                icon="update"
            ),
            pos_hint={"center_x":.9, "center_y":.93},
            on_press=self.update
        )
        
        self.add_widget(btn_update)

        self.update()

    def update(self, instance=""):
        try:
            self.remove_element("Scroll_lists")
        except Exception:
            pass        
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
            MDTextFieldHintText( text="Enter title" ),
            MDTextFieldMaxLengthText( max_text_length=90 ),
            # pos_hint = { "center_x":.5, "center_y":.9 },
        )        
        
        self.input_text = MDTextField(
            MDTextFieldHelperText(text="Enter text"),
            MDTextFieldMaxLengthText( max_text_length=255 ),
            mode = "outlined",
            multiline = True,
            # pos_hint = { "center_x":.5, "center_y":.7 }
        )
        
        box_inpyt = MDBoxLayout()
        box_inpyt.orientation = "vertical"
        box_inpyt.pos_hint = {"center_x":.5, "center_y":1.15 }
        box_inpyt.padding = "10dp"
        box_inpyt.spacing = "50dp"
        box_inpyt.add_widget(self.input_title)
        box_inpyt.add_widget(self.input_text)
        

        # Отвечает за выбор date
        
        self.date = MDButtonText(text="Выбранная дата\n" + str(datetime.datetime.now().strftime("%Y-%m-%d")))
        btn_date=MDButton(
            self.date,
            MDButtonIcon(icon="calendar-range"),
            on_press=self._show_date_picker
        )

        self.time_text = MDButtonText(text=f"""Выбранная време\n { datetime.datetime.now().strftime("%I:%M %p")}""")
        btn_time = MDButton(
            self.time_text,
            MDButtonIcon(icon="clock-time-seven-outline"),
            on_press=self._show_time_picker
        )

        box_date_time = MDBoxLayout()
        box_date_time.pos_hint = {"center_x":.5, "center_y":1}        
        
        box_date_time.add_widget(btn_date)
        box_date_time.add_widget(btn_time)
        
        btn_creat_list = MDButton(
            MDButtonIcon(icon="pencil-circle"),
            pos_hint={"center_x":.9, "center_y":.4},
            on_press=self.creatу_btn
        )

# Добавление элиментов на экран
        
        self.add_widget(box_inpyt)
        self.add_widget(box_date_time)
        self.add_widget(btn_creat_list)

    def creatу_btn(self, instance=""):
        
        """Вызывает методы необходимые для добавления новай записи в БД"""
        
        title = self.input_title.text
        text = self.input_text.text
        date = self.date.text.split("\n")[1]
        time = self.time_text.text

        if text in "" and title in "":
            message = """ Вы не нечего не вели """
            Dialog(message=message).open()
            return
            
        self.input_title.text = ""
        self.input_text.text = ""
        self.date.text = "Выбранная дата\n" + str( datetime.datetime.now().strftime("%Y-%m-%d") )        

        try:
            inser_list(title=title, text=text, date=date, time=time)            
            message = """ Все по кайфу """
            icon = "check-underline"
            Dialog(message=message,icon=icon).open()
            
        except Exception:
            message =  """ Сори """
            print(Exception.__text_signature__)
            Dialog(message=message).open()

# функцые отвичаюшие за выбор даты

    def show_modal_input_date_picker(self, *args):
        def on_edit(*args):
            date_dialog.dismiss()
            Clock.schedule_once(self._show_date_picker, 0.2)

        date_dialog = MDModalInputDatePicker()
        date_dialog.bind(on_edit=on_edit, on_ok=self.on_ok_date, on_cancel=self.on_cancel_date)
        date_dialog.open()

    def on_edit_date(self, instance_date_picker):
        instance_date_picker.dismiss()
        Clock.schedule_once(self.show_modal_input_date_picker, 0.2)
    
    def on_cancel_date(self, instance_date_picker):
        instance_date_picker.dismiss()

    def on_ok_date(self, instance_date_picker):
        instance_date_picker.dismiss()
        self.date.text ="Выбранная дата\n" +  str(instance_date_picker.get_date()[0])

    def _show_date_picker(self, *args):

        date_dialog = MDModalDatePicker()        
        date_dialog.pos_hint = {"center_x":.5, "center_y":.5}

        date_dialog.bind(on_ok=self.on_ok_date, on_cancel=self.on_cancel_date, on_edit=self.on_edit_date)
        
        date_dialog.open()      

# функцые отвичаюшие за выбор времени
    def on_cancel_time(self, time_picker_vertical):
        time_picker_vertical.dismiss()

    def on_ok_time(self, time_picker_vertical: MDTimePickerDialVertical):
        
        hour = str(time_picker_vertical.hour) if int(time_picker_vertical.hour) > 9 else "0"+str(time_picker_vertical.hour)
        minute = str(time_picker_vertical.minute) if int(time_picker_vertical.minute) > 9 else "0"+str(time_picker_vertical.minute)  
        ap_pm = str(time_picker_vertical.am_pm).upper() 
        
        self.time_text.text = f"Выбранная време\n { hour }:{ minute } { ap_pm }"
        time_picker_vertical.dismiss()
            
    def _show_time_picker(self, *args):
        time_picker = MDTimePickerDialVertical()
        time_picker.bind(on_ok=self.on_ok_time, on_cancel=self.on_cancel_time, )
        time_picker.open()         

            
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


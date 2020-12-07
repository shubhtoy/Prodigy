from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.app import MDApp
from kivymd.uix.picker import MDTimePicker, MDDatePicker

# from kivy.core.window import Window
from kivymd.uix.datatables import MDDataTable
from kivy.metrics import dp
import webbrowser
import mysql.connector as ms
from datetime import datetime
import datetime as dt

try:
    from android.permissions import request_permissions, Permission

    request_permissions(
        [
            Permission.INTERNET,
            Permission.READ_EXTERNAL_STORAGE,
            Permission.WRITE_EXTERNAL_STORAGE,
        ]
    )
except:
    pass
# Window.size = (300, 500)
task = ""
time_ = ""
user = ""
passwd_ = ""
date_ = ""


class Mainscreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def login(self):
        global user, passwd_
        self.ids.bar.start()
        user_ = self.ids.username
        pass_ = self.ids.passw
        user = user_.text
        passw = pass_.text
        if user == "":
            return
        # print(user,passw)
        try:
            # self.ids.bar.stop()
            self.db = ms.connect(
                host="logs.c7xtjtjv8ph3.ap-south-1.rds.amazonaws.com",
                port=3306,
                user="shubh",
                passwd="shubh2003",
                db="tasker",
            )
            self.db.autocommit = True
            self.cursor = self.db.cursor()
            self.cursor.execute(
                f'select passwd,email,insta,fb from users where name="{user}";'
            )
            a = self.cursor.fetchall()
        except:
            self.ids.bar.start()
            return
        # db.close()
        # print(len(a))
        for i in a:
            for k in i:
                if k == None:
                    k = ""
        if len(a) == 0:
            user_.focus = True
            user_.error = True
            user_.text = ""
            # print(type(a))
        elif passw != a[0][0]:
            user_.error = False
            pass_.focus = True
            pass_.error = True
            pass_.text = ""
        else:
            user_.error = False
            pass_.error = False
            self.ids.passwd_.text = a[0][0]

            self.ids.email.text = a[0][1]
            self.ids.insta.text = a[0][2]
            self.ids.fb.text = a[0][3]
            self.ids.fb.text = a[0][3]
            self.ids.bar.stop()
            self.ids.screen_manager.current = "scr 2"
            self.table()

    def show_time_picker(self):
        global user
        if user == "":
            pass
        time_dialog = MDTimePicker()
        time_dialog.bind(time=self.get_time)
        time_dialog.open()

    def get_time(self, instance, time):
        global time_
        """
        The method returns the set time.

        :type instance: <kivymd.uix.picker.MDTimePicker object>
        :type time: <class 'datetime.time'>
        """
        sel_time = time
        time_ = str(time)
        # date = datetime.datetime.strptime('2018-01-01', '%Y-%m-%d').date()
        curr_time = datetime.strptime(
            str(datetime.now().strftime("%H:%M:00")), "%H:%M:00"
        ).time()
        # print(sel_time,curr_time)
        if sel_time > curr_time:
            strd = str(dt.datetime.now().strftime("%Y:%m:%d"))
            self.show_date_picker(datetime.strptime(strd, "%Y:%m:%d").date())
        else:
            strd = str((dt.datetime.now() + dt.timedelta(days=1)).strftime("%Y:%m:%d"))
            # print(strd)
            self.show_date_picker(datetime.strptime(strd, "%Y:%m:%d").date())
        # return time

    def show_date_picker(self, min):
        min_date = min
        max_date = datetime.strptime("2050:12:12", "%Y:%m:%d").date()
        dats = str(min).split("-")
        # print(str(min))
        date_dialog = MDDatePicker(
            callback=self.get_date,
            min_date=min_date,
            max_date=max_date,
            year=int(dats[0]),
            month=int(dats[1]),
            day=int(dats[2]),
        )
        date_dialog.open()
        return

    def get_date(self, date):
        global date_
        """
        :type date: <class 'datetime.date'>
        """
        date_ = str(date)
        return

    def insert_task(self):
        global time_, date_, task, user
        if time_ == "" or date_ == "" or task == "" or user == "":
            print("eff")
        else:
            try:
                self.ids.bar2.stop()
                self.db.ping(reconnect=True, attempts=1)
                self.cursor.execute(
                    f"insert into task values('{user}','{task}','{date_}','{time_}')"
                )
                time_ = date_ = task = ""
                self.table()
                return
            except:
                self.ids.bar2.start()
                return

    def callback(self, instance):
        if instance.icon == "clock-check-outline":
            self.show_time_picker()
            return
        elif instance.icon == "note-outline":
            self.ids.screen_manager.current = "data entry"
            return
        elif instance.icon == "timetable":
            # print('hehehehe')
            self.show_table()
            return
        elif instance.icon == "send-outline":
            self.insert_task()
            return

    def grabtask(self):
        global task
        task_ = self.ids.task
        task = str(task_.text)
        # print(task)
        self.ids.screen_manager.current = "scr 2"
        return

    def table(self):
        # rw=()
        row_ = []
        global user
        try:
            self.ids.bar2.stop()
            self.db.ping(reconnect=True, attempts=1)
            self.cursor.execute(
                f"select task.date,task.time,task.task from task where name='{user}';"
            )
            r = self.cursor.fetchall()
        except:
            self.ids.bar2.start()
            return
            # db.close()
        if len(r) == 0:
            return
        for i in r:
            rw = ()
            for k in i:
                rw += (str(k),)
            row_.append(rw)
        # return
        row_ = row_[::-1]
        self.data_table = MDDataTable(
            size_hint=(0.9, 0.6),
            column_data=[
                ("Date", dp(20)),
                ("Time", dp(20)),
                ("Task", dp(30)),
            ],
            row_data=row_,
            use_pagination=True,
            pagination_menu_pos="center",
            sort=True,
        )
        # print(row_)
        return

    def show_table(self):
        try:
            self.data_table.open()
            return
        except:
            return

    def change_data(self):
        global user
        if user == "":
            return
        ema = self.ids.email
        f = self.ids.fb
        pas = self.ids.passwd_
        ins = self.ids.insta
        email = ema.text
        paswd_ = pas.text
        fb = f.text
        insta = ins.text
        try:
            self.ids.bar2.stop()
            self.db.ping(reconnect=True, attempts=1)
            self.cursor.execute(
                f'update users set email="{email}",insta="{insta}",fb="{fb}",passwd="{paswd_}" where name="{user}";'
            )
            return
        except:
            self.ids.bar2.start()
            # db.close()
            return


class ContentNavigationDrawer(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def register(self):
        webbrowser.open("https://abhivyakti-evolve.com/prodigy.html")
        return


class ProdigyApp(MDApp):
    screen_manager = ObjectProperty()
    nav_drawer = ObjectProperty()
    data = {
        "timetable": "Current Tasks",
        "clock-check-outline": "Set Time",
        "note-outline": "Set Task",
        "send-outline": "Send",
    }

    def build(self):
        self.theme_cls.primary_palette = "Yellow"
        # self.theme_cls.primary_hue = "900"
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.accent_palette = "Green"
        b = Mainscreen()
        return b


if __name__ == "__main__":
    a = ProdigyApp()
    a.run()
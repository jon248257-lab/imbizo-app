from kivy.uix.screenmanager import Screen
from kivy.app import App
from kivy.clock import Clock
from kivy.properties import ObjectProperty # ADDED THIS 1 LINE
import datetime, json, os

from modules.auth import Auth, load_users, delete_user
from modules.license import check_license, PRICES
from modules.notifications import get_settings
from modules.labels import Labels
from modules.learners import load as load_learners, add as add_learner
from modules.attendance import save_attendance
from modules.whatsapp import send_whatsapp_alert
from modules.sms import send_sms
from modules.reports import Reports
from modules.classes import load as load_classes, save as save_classes
from modules.backup import create_backup
from __main__ import show_popup

class LoginScreen(Screen):
    def login(self, user, pw):
        user_data = Auth.login(user, pw)
        if user_data:
            App.get_running_app().current_user = user_data
            role = user_data.get("role", "teacher")
            if role == "headteacher":
                self.manager.current = "headteacher"
            else:
                self.manager.current = "teacher"
            self.ids.login_msg.text = ""
        else:
            self.ids.login_msg.text = "Invalid Username or Password"

class FirstRunScreen(Screen):
    def create_admin(self, user, pw):
        if user and pw:
            Auth.create_admin(user, pw, role="headteacher")
            show_popup("Success", "Admin Created. Please Login")
            self.manager.current = "login"

class PaymentScreen(Screen):
    # THESE 2 LINES CONNECT TO KV IDS
    code_input = ObjectProperty(None)
    phone_input = ObjectProperty(None)

    def on_pre_enter(self):
        """When screen opens, show expiry info for HT"""
        app = App.get_running_app()
        if app.get_role() == "headteacher":
            active, days_left, msg = check_license()
            if active:
                self.ids.status_label.text = f"Current: {days_left} days left. Enter new code to stack."
            else:
                self.ids.status_label.text = "EXPIRED. Enter new code to renew."

class TeacherScreen(Screen):
    def on_pre_enter(self):
        from modules.notifications import update_bell_count
        count = update_bell_count()
        if 'bell_btn' in self.ids:
            self.ids.bell_btn.text = f"🔔 {count}"
            self.ids.bell_btn.background_color = (1, 0, 0, 1) if count > 0 else (0.5, 0.5, 0.5, 1)

    def logout(self):
        App.get_running_app().current_user = None
        self.manager.current = "login"

class HeadteacherScreen(Screen):
    def on_pre_enter(self):
        active, days_left, msg = check_license()
        if 'license_info' in self.ids:
            if active:
                self.ids.license_info.text = f"Active: {days_left} days"
                self.ids.license_info.color = (0, 0.7, 0, 1)
            else:
                self.ids.license_info.text = "EXPIRED"
                self.ids.license_info.color = (1, 0, 0, 1)
        self.manager.get_screen('headteacher').manager.app.load_submissions()

    def logout(self):
        App.get_running_app().current_user = None
        self.manager.current = "login"

class LearnerListScreen(Screen):
    def on_pre_enter(self):
        self.ids.rv.data = []
        cls = App.get_running_app().selected_class
        learners = [l for l in load_learners() if l['class'] == cls]
        self.ids.rv.data = [{'text': f"{l['name']} - {l['parent_phone']}"} for l in learners]

class AddLearnerScreen(Screen):
    def save(self, name, phone):
        cls = App.get_running_app().selected_class
        if name and phone:
            add_learner(name, phone, cls)
            show_popup("Saved", f"{name} added to {cls}")
            self.manager.current = "learners"

class TakeAttendanceScreen(Screen):
    records = []
    def on_pre_enter(self):
        self.records = []
        self.ids.box.clear_widgets()
        cls = App.get_running_app().selected_class
        learners = [l for l in load_learners() if l['class'] == cls]
        for l in learners:
            from kivy.uix.boxlayout import BoxLayout
            from kivy.uix.label import Label
            from kivy.uix.button import Button
            row = BoxLayout(size_hint_y=None, height=50)
            row.add_widget(Label(text=l['name'], color=(0.04, 0.15, 0.25, 1)))
            btn_p = Button(text="Present", background_color=(0.79, 0.63, 0.15, 1), color=(0.04, 0.15, 0.25, 1), on_release=lambda x, id=l['id'], name=l['name'], cls=cls: self.mark(id, name, cls, "Present"))
            btn_a = Button(text="Absent", background_color=(0.8, 0.1, 0.1, 1), color=(1,1,1,1), on_release=lambda x, id=l['id'], name=l['name'], cls=cls: self.mark(id, name, cls, "Absent"))
            row.add_widget(btn_p); row.add_widget(btn_a)
            self.ids.box.add_widget(row)

    def mark(self, id, name, cls, status):
        self.records.append({"id":id, "name":name, "class":cls, "status":status})

    def submit(self):
        date = str(datetime.date.today())
        if not os.path.exists("submissions"): os.makedirs("submissions")
        teacher = App.get_running_app().current_user["username"]
        filename = f"submissions/{teacher}_{App.get_running_app().selected_class}_Attendance_{date}.json"
        submission = {
            "teacher_name": teacher,
            "class": App.get_running_app().selected_class,
            "type": "Attendance",
            "date": date,
            "status": "Pending",
            "data": self.records,
            "notified": True
        }
        with open(filename, "w") as f: json.dump(submission, f)
        show_popup("Submitted", f"Attendance sent to Headteacher for Approval")
        self.manager.current = "teacher"

class ReportScreen(Screen):
    def export(self):
        data = load_learners()
        Reports.export_to_pdf(data, "DR Learners Report", "data/reports/dr_learners_report.pdf")
        show_popup("Exported", "Files saved in data/reports/")

class ManageTeachersScreen(Screen):
    def on_pre_enter(self):
        self.load_teachers()
        self.load_classes()

    def load_teachers(self):
        users = load_users()
        teachers = [u for u in users if u["role"] == "teacher"]
        self.ids.teacher_rv.data = [{'text': f"{t['username']} - {t['role']}"} for t in teachers]

    def load_classes(self):
        self.ids.class_rv.data = [{'text': c} for c in load_classes()]

    def add_teacher(self, username, password):
        if not username or not password: show_popup("Error", "Enter Username and Password"); return
        success, msg = Auth.add_user(username, password, role="teacher")
        show_popup("Result", msg)
        if success: self.load_teachers(); self.ids.new_teacher_user.text = ""; self.ids.new_teacher_pass.text = ""

    def delete_teacher(self, username):
        delete_user(username)
        show_popup("Deleted", f"{username} deleted")
        self.load_teachers()

    def add_class(self, name):
        classes = load_classes()
        if name and name not in classes:
            classes.append(name); save_classes(classes)
            show_popup("Added", f"Class {name} added"); self.load_classes()
        else: show_popup("Error", "Class already exists or empty")

class BackupScreen(Screen):
    def backup(self):
        path = create_backup()
        show_popup("Backup Done", f"Saved to {path}")

class SMSSettingsScreen(Screen):
    def test_sms(self, phone):
        if send_sms(phone, "DR Test SMS: Digital Registration App"): show_popup("Sent", "Test SMS Sent")
        else: show_popup("Error", "SMS Failed. Check permissions")

class LabelsScreen(Screen):
    def on_pre_enter(self):
        labels = Labels.load()
        self.ids.lbl_learners.text = labels['learners']
        self.ids.lbl_attendance.text = labels['attendance']
        self.ids.lbl_class.text = labels['class']
        self.ids.lbl_report.text = labels['report']

    def save_labels(self):
        labels = {
            "learners": self.ids.lbl_learners.text.upper(), "learner": "Learner",
            "attendance": self.ids.lbl_attendance.text.upper(), "class": self.ids.lbl_class.text,
            "classes": self.ids.lbl_class.text.upper() + "S", "report": self.ids.lbl_report.text.upper(),
            "backup": "BACKUP & RESTORE", "sms": "SMS SETTINGS", "license": "LICENSE / PAYMENT"
        }
        Labels.save(labels)
        show_popup("Saved", "App will restart to apply changes")
        App.get_running_app().stop()

class SettingsScreen(Screen):
    def on_pre_enter(self):
        settings = get_settings()
        self.ids.sound_switch.active = settings["sound"]
        self.ids.vib_switch.active = settings["vibration"]

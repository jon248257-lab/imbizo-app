from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.clock import Clock
import datetime, os, json
import sys # ADDED FOR ANDROID EXIT

# Import all modules
from modules.kv import KV
from modules.auth import Auth
from modules.license import check_license, create_full_license, get_renewal_alert, PRICES # UPDATED license.py
from modules.notifications import check_teacher_notifications, update_bell_count, save_setting, get_settings
from modules.labels import Labels
from modules.learners import *
from modules.attendance import *
from modules.whatsapp import send_whatsapp_alert
from modules.sms import send_sms
from modules.reports import Reports
from modules.classes import *
from modules.backup import create_backup

# Import all screens - ADDED PaymentScreen for activation
from modules.screens import (
    LoginScreen, FirstRunScreen, PaymentScreen, # PaymentScreen = Activation Screen
    LearnerListScreen, AddLearnerScreen, TakeAttendanceScreen,
    ReportScreen, ManageTeachersScreen, BackupScreen,
    SMSSettingsScreen, LabelsScreen, SettingsScreen,
    TeacherScreen, HeadteacherScreen
)

current_review_file = ""

def show_popup(title, message):
    popup = Popup(title=title, content=Label(text=message), size_hint=(0.8, 0.4))
    popup.open()

class DRApp(App):
    current_user = None
    selected_class = None
    selected_role = "teacher" # Default
    selected_plan = "month" # Default

    def build(self):
        self.title = "DR - Digital Registration"
        self.icon = "icon.png"
        self.labels = Labels.load()

        sm = Builder.load_string(KV) # Load KV once

        # 1. CHECK FIRST RUN
        if Auth.first_run():
            sm.current = "firstrun"
            return sm

        # 2. CHECK LICENSE BEFORE ANYTHING ELSE - THIS IS THE LOCK
        active, days_left, msg = check_license()
        if not active:
            sm.current = "payment" # Force to activation screen
            show_popup("Subscription Required", msg) # Show why
            return sm

        # 3. IF LICENSE OK, ROUTE TO DASHBOARD
        role = self.get_role()
        if role == "headteacher":
            sm.current = "headteacher"
        else:
            sm.current = "teacher"
        return sm

    def on_start(self):
        Clock.schedule_once(self.check_subscription, 0.5)
        Clock.schedule_once(self.check_notifications, 1.0)

    def get_role(self):
        if not os.path.exists("data/license.kr"): return "teacher"
        with open("data/license.kr") as f: data = json.load(f)
        return data.get("role", "teacher")

    def check_subscription(self, dt):
        active, days_left, msg = check_license()
        role = self.get_role()

        # Show alert if 7, 4, 1 days left
        alert = get_renewal_alert(days_left)
        if alert: show_popup("Subscription Reminder", alert)

        # Update HT dashboard label
        if role == "headteacher" and hasattr(self.root, 'ids') and 'license_info' in self.root.ids:
            label = self.root.ids.license_info
            if active:
                plan_price = PRICES[role][self.selected_plan]
                label.text = f"Active: {days_left} days | {plan_price}UGX"
                label.color = (0, 0.7, 0, 1)
            else:
                label.text = f"EXPIRED. Tap to renew"
                label.color = (1, 0, 0, 1)
                self.root.current = "payment"

        # HARD LOCK - If expired anytime, kick to payment
        if not active:
            self.root.current = "payment"

    def check_notifications(self, dt):
        if self.get_role() == "teacher":
            count = check_teacher_notifications()
            if hasattr(self.root, 'ids') and 'bell_btn' in self.root.ids:
                self.root.ids.bell_btn.text = f"🔔 {count}"
                self.root.ids.bell_btn.background_color = (1, 0, 0, 1) if count > 0 else (0.5, 0.5, 0.5, 1)

    # ===== LICENSE / PAYMENT - UPDATED FOR 1 DEVICE LOCK =====
    def activate_license(self, code, phone):
        if not code or not phone:
            self.root.ids.status_label.text = "Enter Code and Phone"
            return
        # create_full_license now checks device lock + expiry + secret
        success, msg = create_full_license(code, phone, self.selected_role, self.selected_plan)
        if success:
            self.root.ids.status_label.text = f"Activated! {msg}"
            Clock.schedule_once(lambda dt: self.restart_app(), 1.5)
        else:
            self.root.ids.status_label.text = msg # e.g. "CODE ALREADY IN USE"

    def restart_app(self):
        # ANDROID FIX: Can't restart app. Just exit so user re-opens it
        sys.exit(0)

    # ===== HEADTEACHER FUNCTIONS =====
    def load_submissions(self):
        rv_data = []
        folder = "submissions"
        if not os.path.exists(folder): os.makedirs(folder)
        for f in os.listdir(folder):
            with open(f"{folder}/{f}") as file: data = json.load(file)
            rv_data.append({
                "teacher": data["teacher_name"],
                "class_name": data["class"],
                "sub_type": data["type"],
                "status": data["status"]
            })
        self.root.ids.submissions_list.data = rv_data

    def open_review_popup(self, teacher, class_name, sub_type):
        global current_review_file
        files = [f for f in os.listdir("submissions") if teacher in f and class_name in f and sub_type in f]
        if not files: return
        current_review_file = f"submissions/{sorted(files)[-1]}"

        with open(current_review_file) as f: data = json.load(f)

        content = BoxLayout(orientation="vertical", padding=10, spacing=10)
        content.add_widget(Label(text=f"Reviewing {class_name} {sub_type} from {teacher}"))
        content.add_widget(Label(text=str(data["data"])))
        comment_input = TextInput(hint_text="Add comment if rejecting", size_hint_y=None, height=60)
        content.add_widget(comment_input)

        btns = BoxLayout()
        btns.add_widget(Button(text="REJECT", background_color=(1,0,0,1), on_press=lambda x: self.reject_submission(comment_input.text)))
        btns.add_widget(Button(text="APPROVE", background_color=(0,0.6,0,1), on_press=lambda x: self.approve_submission()))
        content.add_widget(btns)

        self.popup = Popup(title="Review Submission", content=content, size_hint=(0.9, 0.6))
        self.popup.open()

    def approve_submission(self):
        global current_review_file
        with open(current_review_file, "r+") as f:
            data = json.load(f)
            data["status"] = "Approved"
            data["approved_by"] = "Headteacher"
            data["approved_date"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
            data["notified"] = False
            f.seek(0); f.truncate(); json.dump(data, f)
        self.popup.dismiss()
        self.load_submissions()

    def reject_submission(self, comment):
        global current_review_file
        with open(current_review_file, "r+") as f:
            data = json.load(f)
            data["status"] = "Rejected"
            data["comment"] = comment
            data["notified"] = False
            f.seek(0); f.truncate(); json.dump(data, f)
        self.popup.dismiss()
        self.load_submissions()

    def export_all_data(self):
        path = Reports.export_term_report()
        show_popup("Export Complete", f"Term Report saved to:\n{path}")

    # ===== TEACHER / SETTINGS FUNCTIONS =====
    def open_notification_history(self):
        if not os.path.exists("teacher_notifications.json"): return
        with open("teacher_notifications.json") as f: history = json.load(f)
        layout = BoxLayout(orientation="vertical")
        for n in history:
            color = "ff0000" if n["type"]=="Rejected" else "00aa00"
            txt = f"[color={color}][b]{n['type']}[/b][/color] {n['class']} {n['sub_type']}\n{n['message']}\n{n['date']}\n"
            layout.add_widget(Label(text=txt, markup=True, size_hint_y=None, height=60))
            n["read"] = True
        with open("teacher_notifications.json", "w") as f: json.dump(history, f)
        self.root.ids.bell_btn.text = "🔔 0"
        self.root.ids.bell_btn.background_color = (0.5, 0.5, 0.5, 1)
        popup = Popup(title="Notification History", content=layout, size_hint=(0.9, 0.7))
        popup.open()

    def save_setting(self, key, value):
        save_setting(key, value)

    def test_alert(self):
        from modules.notifications import play_alert
        play_alert()

if __name__ == "__main__":
    DRApp().run()

#:import dp kivy.metrics.dp

ScreenManager:
    FirstRunScreen:
    LoginScreen:
    PaymentScreen:
    TeacherScreen:
    HeadteacherScreen:
    LearnerListScreen:
    AddLearnerScreen:
    TakeAttendanceScreen:
    ReportScreen:
    ManageTeachersScreen:
    BackupScreen:
    SMSSettingsScreen:
    LabelsScreen:
    SettingsScreen:

<FirstRunScreen>:
    name: "firstrun"
    BoxLayout:
        orientation: "vertical"
        padding: dp(40)
        spacing: dp(20)
        Label:
            text: "CREATE ADMIN ACCOUNT"
            font_size: "24sp"
            bold: True
            color: 0.04, 0.15, 0.25, 1
        TextInput:
            id: admin_user
            hint_text: "Admin Username"
            size_hint_y: None
            height: dp(50)
        TextInput:
            id: admin_pass
            hint_text: "Admin Password"
            password: True
            size_hint_y: None
            height: dp(50)
        Button:
            text: "CREATE ADMIN"
            background_color: 0.79, 0.63, 0.15, 1
            color: 0.04, 0.15, 0.25, 1
            size_hint_y: None
            height: dp(60)
            on_release: root.create_admin(admin_user.text, admin_pass.text)

<LoginScreen>:
    name: "login"
    BoxLayout:
        orientation: "vertical"
        padding: dp(40)
        spacing: dp(20)
        Label:
            text: "DR - DIGITAL REGISTRATION"
            font_size: "24sp"
            bold: True
            color: 0.04, 0.15, 0.25, 1
        TextInput:
            id: username
            hint_text: "Username"
            size_hint_y: None
            height: dp(50)
        TextInput:
            id: password
            hint_text: "Password"
            password: True
            size_hint_y: None
            height: dp(50)
        Label:
            id: login_msg
            color: 1,0,0,1
            size_hint_y: None
            height: dp(30)
        Button:
            text: "LOGIN"
            background_color: 0.04, 0.15, 0.25, 1
            color: 1,1,1,1
            size_hint_y: None
            height: dp(60)
            on_release: root.login(username.text, password.text)

<PaymentScreen>:
    name: "payment"
    BoxLayout:
        orientation: "vertical"
        padding: dp(20)
        spacing: dp(10)
        Label:
            text: "ACTIVATE APP"
            font_size: "24sp"
            bold: True
            color: 0.04, 0.15, 0.25, 1
            size_hint_y: None
            height: dp(50)
        Label:
            id: status_label
            text: "Enter Code and Admin Phone"
            color: 1,0,0,1
        BoxLayout:
            size_hint_y: None
            height: dp(50)
            Button:
                text: "Teacher"
                background_color: (0.79, 0.63, 0.15, 1) if app.selected_role == "teacher" else (0.5,0.5,0.5,1)
                on_release: app.selected_role = "teacher"
            Button:
                text: "Headteacher"
                background_color: (0.79, 0.63, 0.15, 1) if app.selected_role == "headteacher" else (0.5,0.5,0.5,1)
                on_release: app.selected_role = "headteacher"
        BoxLayout:
            size_hint_y: None
            height: dp(50)
            Button:
                text: "Month"
                background_color: (0.79, 0.63, 0.15, 1) if app.selected_plan == "month" else (0.5,0.5,0.5,1)
                on_release: app.selected_plan = "month"
            Button:
                text: "Term"
                background_color: (0.79, 0.63, 0.15, 1) if app.selected_plan == "term" else (0.5,0.5,0.5,1)
                on_release: app.selected_plan = "term"
        Label:
            text: f"Price: {PRICES[app.selected_role][app.selected_plan]} UGX"
            color: 0.04, 0.15, 0.25, 1
        TextInput:
            id: activation_code
            hint_text: "Enter Activation Code"
            size_hint_y: None
            height: dp(50)
        TextInput:
            id: admin_phone
            hint_text: "Admin WhatsApp Phone 2567..."
            size_hint_y: None
            height: dp(50)
        Button:
            text: "ACTIVATE"
            background_color: 0, 0.6, 0, 1
            color: 1,1,1,1
            size_hint_y: None
            height: dp(60)
            on_release: app.activate_license(activation_code.text, admin_phone.text)

<TeacherScreen>:
    name: "teacher"
    BoxLayout:
        orientation: "vertical"
        padding: dp(10)
        spacing: dp(10)
        BoxLayout:
            size_hint_y: None
            height: dp(50)
            Label:
                id: welcome_label
                text: "TEACHER DASHBOARD"
                bold: True
                color: 0.04, 0.15, 0.25, 1
            Button:
                id: bell_btn
                text: "🔔 0"
                size_hint_x: None
                width: dp(80)
                background_color: 0.5, 0.5, 0.5, 1
                on_release: app.open_notification_history()
        Button:
            text: app.labels['attendance']
            size_hint_y: None
            height: dp(60)
            background_color: 0.79, 0.63, 0.15, 1
            color: 0.04, 0.15, 0.25, 1
            on_release: app.root.current = "attendance"
        Button:
            text: app.labels['learners']
            size_hint_y: None
            height: dp(60)
            background_color: 0.04, 0.15, 0.25, 1
            color: 1,1,1,1
            on_release: app.root.current = "learners"
        Button:
            text: "Settings"
            size_hint_y: None
            height: dp(60)
            background_color: 0.5, 0.5, 0.5, 1
            color: 1,1,1,1
            on_release: app.root.current = "settings"
        Button:
            text: "LOGOUT"
            size_hint_y: None
            height: dp(60)
            background_color: 0.8, 0.1, 0.1, 1
            color: 1,1,1,1
            on_release: root.logout()

<HeadteacherScreen>:
    name: "headteacher"
    BoxLayout:
        orientation: "vertical"
        padding: dp(10)
        spacing: dp(10)
        BoxLayout:
            size_hint_y: None
            height: dp(50)
            Label:
                text: "HEADTEACHER DASHBOARD"
                bold: True
                color: 0.04, 0.15, 0.25, 1
            Label:
                id: license_info
                text: "Checking..."
                size_hint_x: None
                width: dp(200)
        TabbedPanel:
            do_default_tab: False
            size_hint_y: 0.9
            TabbedPanelItem:
                text: "Submissions"
                BoxLayout:
                    orientation: "vertical"
                    Button:
                        text: "REFRESH"
                        size_hint_y: None
                        height: dp(40)
                        on_release: app.load_submissions()
                    RecycleView:
                        id: submissions_list
                        viewclass: "SubmissionItem"
                        RecycleBoxLayout:
                            default_size: None, dp(50)
                            default_size_hint: 1, None
                            size_hint_y: None
                            height: self.minimum_height
                            orientation: "vertical"
            TabbedPanelItem:
                text: "Manage"
                ManageTeachersScreen:
            TabbedPanelItem:
                text: "Reports"
                BoxLayout:
                    orientation: "vertical"
                    Button:
                        text: "EXPORT TERM REPORT"
                        background_color: 0.79, 0.63, 0.15, 1
                        color: 0.04, 0.15, 0.25, 1
                        size_hint_y: None
                        height: dp(60)
                        on_release: app.export_all_data()
        Button:
            text: "LOGOUT"
            size_hint_y: None
            height: dp(60)
            background_color: 0.8, 0.1, 0.1, 1
            color: 1,1,1,1
            on_release: root.logout()

<SubmissionItem@BoxLayout>:
    teacher: ""
    class_name: ""
    sub_type: ""
    status: ""
    orientation: "horizontal"
    size_hint_y: None
    height: dp(50)
    padding: dp(5)
    Label:
        text: f"{root.teacher} - {root.class_name} - {root.sub_type}"
    Label:
        text: root.status
        color: (0,0.6,0,1) if root.status=="Approved" else (1,0,0,1) if root.status=="Rejected" else (0.8,0.5,0,1)
    Button:
        text: "REVIEW"
        size_hint_x: None
        width: dp(80)
        on_release: app.open_review_popup(root.teacher, root.class_name, root.sub_type)

<SettingsScreen>:
    name: "settings"
    BoxLayout:
        orientation: "vertical"
        padding: dp(20)
        spacing: dp(20)
        Label:
            text: "SETTINGS"
            font_size: "20sp"
            bold: True
            color: 0.04, 0.15, 0.25, 1
            size_hint_y: None
            height: dp(50)
        BoxLayout:
            Label:
                text: "Sound"
            Switch:
                id: sound_switch
                active: True
                on_active: app.save_setting("sound", self.active)
        BoxLayout:
            Label:
                text: "Vibration"
            Switch:
                id: vib_switch
                active: True
                on_active: app.save_setting("vibration", self.active)
        Button:
            text: "TEST ALERT"
            size_hint_y: None
            height: dp(50)
            on_release: app.test_alert()
        Button:
            text: "< Back"
            background_color: 0.04, 0.15, 0.25, 1
            color: 1,1,1,1
            size_hint_y: None
            height: dp(60)
            on_release: app.root.current = "teacher"

<ManageTeachersScreen>:
    # This class is embedded inside HeadteacherScreen Tab
    # So no name here
    BoxLayout:
        orientation: "vertical"
        padding: dp(10)
        spacing: dp(10)
        Label:
            text: "MANAGE TEACHERS & CLASSES"
            font_size: "20sp"
            bold: True
            color: 0.04, 0.15, 0.25, 1
            size_hint_y: None
            height: dp(50)
        TabbedPanel:
            do_default_tab: False
            size_hint_y: 0.9
            TabbedPanelItem:
                text: "Teachers"
                BoxLayout:
                    orientation: "vertical"
                    padding: dp(10)
                    spacing: dp(10)
                    BoxLayout:
                        size_hint_y: None
                        height: dp(50)
                        TextInput:
                            id: new_teacher_user
                            hint_text: "New Teacher Username"
                        TextInput:
                            id: new_teacher_pass
                            hint_text: "Password"
                            password: True
                        Button:
                            text: "ADD"
                            size_hint_x: None
                            width: dp(80)
                            background_color: 0.79, 0.63, 0.15, 1
                            on_release: root.add_teacher(new_teacher_user.text, new_teacher_pass.text)
                    RecycleView:
                        id: teacher_rv
                        viewclass: "TeacherItem"
                        RecycleBoxLayout:
                            default_size: None, dp(50)
                            default_size_hint: 1, None
                            size_hint_y: None
                            height: self.minimum_height
                            orientation: "vertical"
            TabbedPanelItem:
                text: "Classes"
                BoxLayout:
                    orientation: "vertical"
                    padding: dp(10)
                    spacing: dp(10)
                    BoxLayout:
                        size_hint_y: None
                        height: dp(50)
                        TextInput:
                            id: new_class
                            hint_text: "New Class Name e.g P4"
                        Button:
                            text: "ADD"
                            size_hint_x: None
                            width: dp(80)
                            background_color: 0.79, 0.63, 0.15, 1
                            on_release: root.add_class(new_class.text)
                    RecycleView:
                        id: class_rv
                        viewclass: "Label"
                        RecycleBoxLayout:
                            default_size: None, dp(50)
                            default_size_hint: 1, None
                            size_hint_y: None
                            height: self.minimum_height
                            orientation: "vertical"
                                                      
<LearnerListScreen>:
    name: "learners"
    BoxLayout:
        orientation: "vertical"
        Label:
            text: f"{app.selected_class} Learners"
        RecycleView:
            id: rv
            viewclass: "Label"
            RecycleBoxLayout:
                default_size: None, dp(40)
                default_size_hint: 1, None
                size_hint_y: None
                height: self.minimum_height
                orientation: "vertical"
        Button:
            text: "+ Add Learner"
            on_release: app.root.current = "add_learner"
        Button:
            text: "< Back"
            on_release: app.root.current = "teacher"

<AddLearnerScreen>:
    name: "add_learner"
    BoxLayout:
        orientation: "vertical"
        padding: dp(20)
        Label:
            text: "Add Learner"
        TextInput:
            id: learner_name
            hint_text: "Learner Name"
        TextInput:
            id: parent_phone
            hint_text: "Parent Phone"
        Button:
            text: "SAVE"
            on_release: root.save(learner_name.text, parent_phone.text)
        Button:
            text: "< Cancel"
            on_release: app.root.current = "learners"

<TakeAttendanceScreen>:
    name: "attendance"
    BoxLayout:
        orientation: "vertical"
        Label:
            text: f"Attendance for {app.selected_class}"
        ScrollView:
            BoxLayout:
                id: box
                orientation: "vertical"
                size_hint_y: None
                height: self.minimum_height
        Button:
            text: "SUBMIT TO HEADTEACHER"
            on_release: root.submit()
        Button:
            text: "< Back"
            on_release: app.root.current = "teacher"

<ReportScreen>:
    name: "report"
    BoxLayout:
        orientation: "vertical"
        padding: dp(20)
        Label:
            text: "Reports"
        Button:
            text: "EXPORT LEARNERS PDF"
            on_release: root.export()
        Button:
            text: "< Back"
            on_release: app.root.current = "teacher"

<BackupScreen>:
    name: "backup"
    BoxLayout:
        orientation: "vertical"
        padding: dp(20)
        Label:
            text: "Backup"
        Button:
            text: "CREATE BACKUP"
            on_release: root.backup()
        Button:
            text: "< Back"
            on_release: app.root.current = "teacher"

<SMSSettingsScreen>:
    name: "sms"
    BoxLayout:
        orientation: "vertical"
        padding: dp(20)
        Label:
            text: "SMS Settings"
        TextInput:
            id: test_phone
            hint_text: "Test Phone"
        Button:
            text: "SEND TEST SMS"
            on_release: root.test_sms(test_phone.text)
        Button:
            text: "< Back"
            on_release: app.root.current = "teacher"

<LabelsScreen>:
    name: "labels"
    BoxLayout:
        orientation: "vertical"
        padding: dp(20)
        Label:
            text: "Rename Labels"
        TextInput:
            id: lbl_learners
            hint_text: "Learners"
        TextInput:
            id: lbl_attendance
            hint_text: "Attendance"
        Button:
            text: "SAVE"
            on_release: root.save_labels()
        Button:
            text: "< Back"
            on_release: app.root.current = "teacher"
<TeacherItem@BoxLayout>:
    text: ""
    orientation: "horizontal"
    size_hint_y: None
    height: dp(50)
    padding: dp(5)
    Label:
        text: root.text
    Button:
        text: "DELETE"
        size_hint_x: None
        width: dp(80)
        background_color: 0.8, 0.1, 0.1, 1
        on_release: root.parent.delete_teacher(root.text.split(" - ")[0])
<PaymentScreen>:
    code_input: code
    phone_input: phone
    name: "payment" # MUST match what main.py calls
    
    ScrollView:
        BoxLayout:
            orientation: "vertical"
            padding: 20
            spacing: 15
            size_hint_y: None
            height: self.minimum_height

            Label:
                text: "DR - SUBSCRIPTION REQUIRED"
                font_size: 24
                bold: True
                color: 1,0,0,1
                size_hint_y: None
                height: 50

            Label:
                id: status_label
                text: "Enter Activation Code from CEO"
                font_size: 16
                size_hint_y: None
                height: 30
                text_size: self.width, None
                halign: "center"

            TextInput:
                id: code
                hint_text: "Enter Code: DR-XXXX-XXXX-XXXX"
                multiline: False
                font_size: 18
                size_hint_y: None
                height: 50

            TextInput:
                id: phone
                hint_text: "Admin Phone: 2567xxxxxxxx"
                multiline: False
                input_filter: "int"
                font_size: 18
                size_hint_y: None
                height: 50

            Label:
                text: "Select Plan"
                font_size: 16
                bold: True
                size_hint_y: None
                height: 30

            BoxLayout:
                size_hint_y: None
                height: 50
                spacing: 10
                Button:
                    text: f"Month: {app.PRICES['teacher']['month']} UGX"
                    background_color: 0.2,0.5,0.8,1
                    on_press: 
                        app.selected_plan = "month"
                        app.selected_role = "teacher"
                Button:
                    text: f"Term: {app.PRICES['teacher']['term']} UGX"
                    background_color: 0.2,0.5,0.8,1
                    on_press: 
                        app.selected_plan = "term"
                        app.selected_role = "teacher"

            BoxLayout:
                size_hint_y: None
                height: 50
                spacing: 10
                Button:
                    text: f"Month HT: {app.PRICES['headteacher']['month']} UGX"
                    background_color: 0.8,0.2,0.5,1
                    on_press: 
                        app.selected_plan = "month"
                        app.selected_role = "headteacher"
                Button:
                    text: f"Term HT: {app.PRICES['headteacher']['term']} UGX"
                    background_color: 0.8,0.2,0.5,1
                    on_press: 
                        app.selected_plan = "term"
                        app.selected_role = "headteacher"

            Button:
                text: "ACTIVATE"
                font_size: 20
                bold: True
                background_color: 0,0.6,0,1
                size_hint_y: None
                height: 60
                on_press: app.activate_license(code.text.strip(), phone.text.strip())

            Label:
                text: "WhatsApp CEO to buy code"
                font_size: 12
                color: 0.5,0.5,0.5,1
                size_hint_y: None
                height: 20

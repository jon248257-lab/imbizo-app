import json
import os
import pandas as pd
from datetime import datetime

LEARNERS_FILE = "data/learners.json"
EXCEL_FILE = "data/learners.xlsx"

FIELDS = [
    "learner_id", "first_name", "last_name", "gender", "dob", "class_stream",
    "parent_name", "parent_phone", "parent_whatsapp", "address", "admission_no",
    "photo_path", "health_info", "previous_school", "date_admitted",
    "guardian_name", "guardian_phone"
]

class Learners:
    @staticmethod
    def load_learners():
        if not os.path.exists(LEARNERS_FILE):
            return []
        try:
            with open(LEARNERS_FILE, "r") as f:
                return json.load(f)
        except:
            return []

    @staticmethod
    def save_learners(data):
        os.makedirs("data", exist_ok=True)
        with open(LEARNERS_FILE, "w") as f:
            json.dump(data, f, indent=4)
        # Also export to Excel for backup
        df = pd.DataFrame(data)
        df.to_excel(EXCEL_FILE, index=False)

    @staticmethod
    def add_learner(learner_data):
        data = Learners.load_learners()
        # Auto generate ID
        new_id = f"L{len(data)+1:04d}"
        learner_data["learner_id"] = new_id
        learner_data["date_admitted"] = datetime.now().strftime("%Y-%m-%d")
        data.append(learner_data)
        Learners.save_learners(data)
        return new_id

    @staticmethod
    def get_learner(learner_id):
        data = Learners.load_learners()
        for learner in data:
            if learner["learner_id"] == learner_id:
                return learner
        return None

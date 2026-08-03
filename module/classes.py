import pandas as pd
import os
from datetime import datetime, timedelta
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

ATT_DIR = "data/attendance"
REPORT_DIR = "data/reports"

class Reports:
    @staticmethod
    def get_daily_report(date_str, class_stream):
        file = f"{ATT_DIR}/{date_str}_{class_stream}.json"
        if not os.path.exists(file):
            return []
        df = pd.read_json(file)
        return df.to_dict('records')

    @staticmethod
    def get_monthly_report(month, year, class_stream):
        all_data = []
        learners = set()
        start = datetime(year, month, 1)
        end = (start + timedelta(days=32)).replace(day=1)

        d = start
        while d < end:
            file = f"{ATT_DIR}/{d.strftime('%Y-%m-%d')}_{class_stream}.json"
            if os.path.exists(file):
                df = pd.read_json(file)
                all_data.append(df)
                learners.update(df['learner_id'].tolist())
            d += timedelta(days=1)

        if not all_data:
            return pd.DataFrame()

        full_df = pd.concat(all_data)
        summary = full_df.groupby('learner_id')['status'].value_counts().unstack(fill_value=0)
        summary['Total'] = summary.sum(axis=1)
        summary['% Present'] = (summary.get('P', 0) / summary['Total'] * 100).round(1)
        return summary.reset_index()

    @staticmethod
    def export_to_pdf(data, title, filename):
        os.makedirs(REPORT_DIR, exist_ok=True)
        c = canvas.Canvas(f"{REPORT_DIR}/{filename}", pagesize=A4)
        c.setFont("Helvetica-Bold", 16)
        c.drawString(50, 800, title)
        y = 770
        c.setFont("Helvetica", 10)
        for row in data:
            c.drawString(50, y, str(row))
            y -= 20
            if y < 50:
                c.showPage()
                y = 800
        c.save()
        return f"{REPORT_DIR}/{filename}"

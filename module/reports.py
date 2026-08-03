import pandas as pd
import os, json
from datetime import datetime, timedelta
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors

ATT_DIR = "data/attendance"
REPORT_DIR = "data/reports"
SUBMISSION_DIR = "submissions" # NEW

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

    # ===== NEW: EXPORT ONLY APPROVED SUBMISSIONS =====
    @staticmethod
    def export_term_report():
        """Headteacher exports all APPROVED submissions for the term"""
        if not os.path.exists(SUBMISSION_DIR):
            return "No submissions folder found"

        all_records = []
        for f in os.listdir(SUBMISSION_DIR):
            with open(f"{SUBMISSION_DIR}/{f}", "r") as file:
                data = json.load(file)
            
            # ONLY EXPORT APPROVED
            if data.get("status") == "Approved":
                for record in data["data"]: # record = {"id":, "name":, "status":}
                    record["class"] = data["class"]
                    record["date"] = data["date"]
                    record["teacher"] = data["teacher_name"]
                    record["type"] = data["type"]
                    all_records.append(record)

        if not all_records:
            return "No Approved submissions found for this term"

        df = pd.DataFrame(all_records)
        
        # 1. EXPORT TO EXCEL
        os.makedirs(REPORT_DIR, exist_ok=True)
        excel_path = f"{REPORT_DIR}/Term_Report_{datetime.now().strftime('%Y-%m-%d')}.xlsx"
        df.to_excel(excel_path, index=False)

        # 2. EXPORT TO PDF
        pdf_path = f"{REPORT_DIR}/Term_Report_{datetime.now().strftime('%Y-%m-%d')}.pdf"
        Reports.export_to_pdf(df.values.tolist(), f"DR TERM REPORT - {datetime.now().strftime('%B %Y')}", pdf_path)
        
        return f"Exported: {excel_path} and {pdf_path}"

    @staticmethod
    def export_to_pdf(data, title, filename):
        os.makedirs(REPORT_DIR, exist_ok=True)
        c = canvas.Canvas(filename, pagesize=A4)
        width, height = A4
        
        # HEADER
        c.setFont("Helvetica-Bold", 16)
        c.drawCentredString(width/2, 800, title)
        c.setFont("Helvetica", 9)
        c.drawCentredString(width/2, 785, f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        
        # TABLE
        table_data = [["Teacher", "Class", "Learner", "Status", "Date"]] + data
        t = Table(table_data, colWidths=[80, 60, 120, 60, 80])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#04182F")), # Navy
            ('TEXTCOLOR',(0,0),(-1,0), colors.whitesmoke),
            ('ALIGN',(0,0),(-1,-1),'CENTER'),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            ('GRID', (0,0), (-1,-1), 1, colors.black),
            ('FONTSIZE', (0,0), (-1,-1), 8)
        ]))
        
        t.wrapOn(c, width, height)
        t.drawOn(c, 30, 650)
        
        c.save()
        return filename

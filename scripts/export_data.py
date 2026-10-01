"""
Export flat, dashboard-ready CSVs from the `hr` MySQL database.

Run this once (or whenever the source database changes) to refresh the
CSVs that app.py reads. Keeping the dashboard on CSVs instead of a live
DB connection keeps the repo simple to run for anyone who clones it.

Usage:
    1. Copy .env.example to .env and fill in your MySQL credentials.
    2. python scripts/export_data.py
"""

import os
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()

DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_NAME = os.getenv("DB_NAME", "hr")

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "data")


def get_engine():
    url = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    return create_engine(url)


QUERIES = {
    "timesheets_full": """
        SELECT
            t.timesheet_id,
            t.employee_id,
            CONCAT(e.first_name, ' ', e.last_name) AS employee_name,
            d.department_name,
            t.role_level,
            t.hourly_rate,
            t.reported_date,
            t.approval_method,
            t.secondment_id,
            s.status AS secondment_status
        FROM timesheets t
        JOIN employees e   ON t.employee_id = e.employee_id
        JOIN secondments s ON t.secondment_id = s.secondment_id
        JOIN departments d ON s.department_id = d.department_id
    """,
    "feedback_full": """
        SELECT
            f.feedback_id,
            f.timesheet_id,
            CONCAT(e.first_name, ' ', e.last_name) AS employee_name,
            d.department_name,
            f.channel,
            f.rating,
            f.submitted_date,
            f.resolved
        FROM feedback f
        JOIN timesheets t   ON f.timesheet_id = t.timesheet_id
        JOIN employees e    ON t.employee_id = e.employee_id
        JOIN secondments s  ON t.secondment_id = s.secondment_id
        JOIN departments d  ON s.department_id = d.department_id
    """,
    "secondments_full": """
        SELECT
            s.secondment_id,
            d.department_name,
            s.status,
            s.start_date,
            s.extension_days
        FROM secondments s
        JOIN departments d ON s.department_id = d.department_id
    """,
    "mentor_load": """
        SELECT
            CONCAT(m.first_name, ' ', m.last_name) AS mentor,
            COUNT(*) AS secondments_mentored
        FROM secondment_mentors sm
        JOIN mentors m ON sm.mentor_id = m.mentor_id
        GROUP BY sm.mentor_id
        ORDER BY secondments_mentored DESC
    """,
}


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    engine = get_engine()

    for name, sql in QUERIES.items():
        df = pd.read_sql(sql, engine)
        out_path = os.path.join(OUTPUT_DIR, f"{name}.csv")
        df.to_csv(out_path, index=False)
        print(f"Wrote {len(df):>5} rows -> {out_path}")


if __name__ == "__main__":
    main()

# HR secondment analysis

A data modeling course project: ER modeling, SQL analysis, and an interactive
dashboard built on a MySQL `hr` database tracking employee secondments
(temporary assignments between offices), timesheets, mentors, and feedback.

## Project structure

```
hr-secondment-analysis/
├── sql/
│   ├── hr1_komplett_databearbetning.sql   # full data cleaning, run on a fresh copy of the original
│   └── hr_business_analysis.sql   # 16 business-focused SQL queries
├── scripts/
│   └── export_data.py             # exports flat CSVs from MySQL for the dashboard
├── data/                          # CSVs consumed by app.py (generated, not hand-edited)
├── app.py                         # Streamlit dashboard
├── requirements.txt
└── .env.example                   # copy to .env with your MySQL credentials
```

## Data model

The database has 11 tables centered on **secondments** — temporary employee
assignments to another office. Key relationships:

- `employees` — the people
- `departments` — org units, linked to secondments
- `secondments` — an assignment: which path, which department, dates/status
- `secondment_paths` — from-office/to-office routes with distance
- `offices` — office locations
- `mentors` / `secondment_mentors` — many-to-many, mentors assigned to secondments
- `timesheets` — hours/rate logged per employee per secondment
- `rate_adjustments` — corrections tied to a timesheet
- `feedback` — rating and resolution status tied to a timesheet
- `profiler` — extended 1:1 profile data per employee

**Known modeling note:** `employees` has no direct foreign key to
`secondments` — the only path is `employees → timesheets → secondments`.
There's also no "hours worked" column, so cost figures in this analysis are a
rate-volume proxy (sum/avg of `hourly_rate` per timesheet row), not true
labor cost.

## Setup

```bash
pip install -r requirements.txt
cp .env.example .env   # fill in your MySQL credentials
python scripts/export_data.py   # regenerate CSVs from the live database
streamlit run app.py
```

The `data/` folder already contains CSVs generated from the sample dataset,
so `streamlit run app.py` works out of the box without a live database
connection — re-run `export_data.py` only if the source data changes.

## SQL analysis

`sql/hr_business_analysis.sql` covers four areas: cost/rate, workload,
mentor load, and feedback trends. Some notable findings:

- Rate volume is close between Systemutveckling and Dataanalys departments,
  with Infrastruktur lower.
- Senior-level timesheets average roughly double the hourly rate of Konsult level.
- Mentor load is fairly even: each of the 12 mentors is assigned to 33-55 secondments (Lina Falk 55, Iris Sand 53).
- Feedback rating doesn't differ much between resolved and unresolved cases
  (3.62 vs 3.68 avg), which is worth digging into further.

## Dashboard

`app.py` is a single-page Streamlit dashboard with department and date
filters, showing:

1. KPI row (employees, secondments, timesheets, avg rate)
2. Rate sum by department / avg rate by role level
3. Secondment status breakdown / avg feedback rating by channel
4. Feedback rating trend over time
5. Top 10 employees by timesheet count

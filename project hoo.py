"""
╔══════════════════════════════════════════════════════════╗
║        MEDICORE — Hospital Management System             ║
║  Modules used: pandas, numpy, scipy, datetime,           ║
║                calendar, math                            ║
║  No OOP · No tkinter · No SQL · No JSON · No OS         ║
╚══════════════════════════════════════════════════════════╝
"""

import pandas as pd
import numpy as np
import math
import calendar
from datetime import datetime, date, timedelta
from scipy import stats

# ─────────────────────────────────────────────────────────
#  DATA STORAGE  (pandas DataFrames, saved as CSV)
# ─────────────────────────────────────────────────────────

PATIENT_FILE     = "patients.csv"
DOCTOR_FILE      = "doctors.csv"
APPOINTMENT_FILE = "appointments.csv"
BILL_FILE        = "bills.csv"

PATIENT_COLS     = ["pid","name","age","gender","blood","phone","address","admitted","ward"]
DOCTOR_COLS      = ["did","name","dept","phone","fee","experience","rating"]
APPOINTMENT_COLS = ["aid","pid","did","date","time","reason","status"]
BILL_COLS        = ["bid","pid","aid","consult_fee","medicine_fee","room_fee","tests_fee","discount","total","status","date"]

def load(file, cols):
    try:
        df = pd.read_csv(file, dtype=str)
        for c in cols:
            if c not in df.columns:
                df[c] = ""
        return df[cols]
    except FileNotFoundError:
        return pd.DataFrame(columns=cols)

def save(df, file):
    df.to_csv(file, index=False)

def next_id(df, col, prefix):
    if df.empty:
        return f"{prefix}001"
    nums = df[col].str.extract(r'(\d+)')[0].dropna().astype(int)
    return f"{prefix}{(nums.max()+1):03d}" if not nums.empty else f"{prefix}001"

# ─────────────────────────────────────────────────────────
#  DISPLAY HELPERS
# ─────────────────────────────────────────────────────────

W = 74  # terminal width

def line(ch="─"):
    print(ch * W)

def header(title, icon="🏥"):
    print()
    line("═")
    print(f"║  {icon}  {title.upper():<{W-7}}║")
    line("═")

def box(text):
    print(f"  ┌{'─'*(W-4)}┐")
    for t in text if isinstance(text, list) else [text]:
        print(f"  │  {t:<{W-7}}│")
    print(f"  └{'─'*(W-4)}┘")

def success(msg): print(f"\n  ✅  {msg}")
def error(msg):   print(f"\n  ❌  {msg}")
def warn(msg):    print(f"\n  ⚠️   {msg}")
def info(msg):    print(f"\n  ℹ️   {msg}")

def pause():
    input("\n  Press Enter to continue...")

def ask(prompt, default=""):
    val = input(f"  {prompt}: ").strip()
    return val if val else default

def ask_int(prompt, lo=0, hi=9999):
    while True:
        try:
            v = int(ask(prompt))
            if lo <= v <= hi:
                return v
            warn(f"Enter a number between {lo} and {hi}")
        except ValueError:
            warn("Please enter a valid number.")

def ask_float(prompt):
    while True:
        try:
            return float(ask(prompt))
        except ValueError:
            warn("Please enter a valid number.")

def pick(prompt, options):
    print(f"\n  {prompt}")
    for i, o in enumerate(options, 1):
        print(f"    [{i}] {o}")
    while True:
        try:
            c = int(ask("Choice"))
            if 1 <= c <= len(options):
                return options[c-1]
        except ValueError:
            pass
        warn("Invalid choice.")

def print_table(df, max_rows=20):
    if df.empty:
        warn("No records found.")
        return
    show = df.head(max_rows).copy()
    # Replace NaN with ""
    show = show.fillna("")
    cols = list(show.columns)
    # Calculate column widths
    widths = [max(len(str(c)), show[c].astype(str).str.len().max()) for c in cols]
    widths = [min(w, 20) for w in widths]
    row_fmt = "  │ " + " │ ".join(f"{{:<{w}}}" for w in widths) + " │"
    sep     = "  ├─" + "─┼─".join("─"*w for w in widths) + "─┤"
    top     = "  ┌─" + "─┬─".join("─"*w for w in widths) + "─┐"
    bot     = "  └─" + "─┴─".join("─"*w for w in widths) + "─┘"
    print(top)
    print(row_fmt.format(*[str(c)[:w] for c, w in zip(cols, widths)]))
    print(sep)
    for _, row in show.iterrows():
        print(row_fmt.format(*[str(row[c])[:w] for c, w in zip(cols, widths)]))
    print(bot)
    if len(df) > max_rows:
        info(f"Showing {max_rows} of {len(df)} records.")

# ─────────────────────────────────────────────────────────
#  PATIENT MODULE
# ─────────────────────────────────────────────────────────

def add_patient():
    header("Register New Patient", "👤")
    patients = load(PATIENT_FILE, PATIENT_COLS)
    pid  = next_id(patients, "pid", "P")
    name = ask("Full Name")
    if not name:
        error("Name cannot be empty."); return
    age  = ask_int("Age", 0, 130)
    gender = pick("Gender", ["Male","Female","Other"])
    blood  = pick("Blood Group", ["A+","A-","B+","B-","AB+","AB-","O+","O-","Unknown"])
    phone  = ask("Phone Number")
    addr   = ask("Address")
    ward   = pick("Ward", ["General","ICU","Pediatrics","Maternity","Surgery","Cardiac","Orthopedic","Neurology","OPD"])
    admitted = datetime.now().strftime("%Y-%m-%d")

    # Age group analysis using numpy
    age_group = (
        "Infant (0-2)"     if age <= 2 else
        "Child (3-12)"     if age <= 12 else
        "Teen (13-19)"     if age <= 19 else
        "Adult (20-59)"    if age <= 59 else
        "Senior (60+)"
    )
    # BMI placeholder hint using math
    bmi_hint = round(math.log(age + 1) * 5, 1) if age > 0 else 0

    new_row = pd.DataFrame([[pid,name,age,gender,blood,phone,addr,admitted,ward]], columns=PATIENT_COLS)
    patients = pd.concat([patients, new_row], ignore_index=True)
    save(patients, PATIENT_FILE)

    box([
        f"Patient Registered Successfully!",
        f"ID       : {pid}",
        f"Name     : {name}",
        f"Age      : {age}  ({age_group})",
        f"Blood    : {blood}",
        f"Ward     : {ward}",
        f"Admitted : {admitted}",
    ])
    pause()

def view_patients():
    header("All Patients", "👥")
    patients = load(PATIENT_FILE, PATIENT_COLS)
    search = ask("Search by name/ID/phone (Enter to show all)")
    if search:
        mask = (
            patients["name"].str.contains(search, case=False, na=False) |
            patients["pid"].str.contains(search, case=False, na=False) |
            patients["phone"].str.contains(search, na=False)
        )
        patients = patients[mask]
    # Numeric analysis with numpy
    if not patients.empty:
        ages = pd.to_numeric(patients["age"], errors="coerce").dropna().values
        if len(ages) > 0:
            info(f"Count: {len(patients)} | Avg Age: {np.mean(ages):.1f} | "
                 f"Min: {int(np.min(ages))} | Max: {int(np.max(ages))} | "
                 f"Std Dev: {np.std(ages):.1f}")
    print_table(patients[["pid","name","age","gender","blood","phone","ward","admitted"]])
    pause()

def discharge_patient():
    header("Discharge Patient", "🚪")
    patients = load(PATIENT_FILE, PATIENT_COLS)
    if patients.empty:
        warn("No patients registered."); pause(); return
    pid = ask("Enter Patient ID to discharge")
    row = patients[patients["pid"] == pid]
    if row.empty:
        error(f"Patient {pid} not found."); pause(); return
    pat = row.iloc[0]

    # Calculate days admitted using datetime
    try:
        admitted_date = datetime.strptime(str(pat["admitted"]), "%Y-%m-%d").date()
        days = (date.today() - admitted_date).days
    except:
        days = 0

    box([
        f"Discharging: {pat['name']} ({pid})",
        f"Ward       : {pat['ward']}",
        f"Days Stay  : {days} day(s)",
    ])
    confirm = ask("Confirm discharge? (yes/no)")
    if confirm.lower() == "yes":
        patients = patients[patients["pid"] != pid]
        save(patients, PATIENT_FILE)
        success(f"Patient {pat['name']} discharged after {days} day(s).")
    else:
        info("Discharge cancelled.")
    pause()

def patient_stats():
    header("Patient Statistics", "📊")
    patients = load(PATIENT_FILE, PATIENT_COLS)
    if patients.empty:
        warn("No data."); pause(); return

    ages = pd.to_numeric(patients["age"], errors="coerce").dropna().values

    # scipy stats
    if len(ages) >= 2:
        skew    = round(float(stats.skew(ages)), 3)
        kurt    = round(float(stats.kurtosis(ages)), 3)
        mode_r  = stats.mode(ages, keepdims=True)
        age_mode = int(mode_r.mode[0])
        median  = float(np.median(ages))
        q1, q3  = float(np.percentile(ages, 25)), float(np.percentile(ages, 75))
        iqr     = round(q3 - q1, 1)
        print()
        box([
            "── Age Distribution (scipy + numpy) ──",
            f"  Count      : {len(ages)}",
            f"  Mean       : {np.mean(ages):.2f}",
            f"  Median     : {median:.1f}",
            f"  Mode       : {age_mode}",
            f"  Std Dev    : {np.std(ages):.2f}",
            f"  Variance   : {np.var(ages):.2f}",
            f"  Skewness   : {skew}  ({'right-skewed' if skew>0 else 'left-skewed' if skew<0 else 'symmetric'})",
            f"  Kurtosis   : {kurt}",
            f"  Q1 / Q3    : {q1:.1f} / {q3:.1f}",
            f"  IQR        : {iqr}",
            f"  Min / Max  : {int(np.min(ages))} / {int(np.max(ages))}",
        ])

    print()
    # Gender breakdown
    print("  Gender Distribution:")
    gender_counts = patients["gender"].value_counts()
    total = len(patients)
    for g, cnt in gender_counts.items():
        pct = cnt / total * 100
        bar = "█" * int(pct / 4)
        print(f"    {g:<10} {bar:<25} {cnt} ({pct:.1f}%)")

    print()
    # Blood group breakdown
    print("  Blood Group Distribution:")
    blood_counts = patients["blood"].value_counts()
    for b, cnt in blood_counts.items():
        bar = "█" * cnt
        print(f"    {b:<6} {bar:<20} {cnt}")

    print()
    # Ward occupancy
    print("  Ward Occupancy:")
    ward_counts = patients["ward"].value_counts()
    for w, cnt in ward_counts.items():
        bar = "█" * cnt
        print(f"    {w:<15} {bar:<20} {cnt}")

    pause()

# ─────────────────────────────────────────────────────────
#  DOCTOR MODULE
# ─────────────────────────────────────────────────────────

def add_doctor():
    header("Add New Doctor", "👨‍⚕️")
    doctors = load(DOCTOR_FILE, DOCTOR_COLS)
    did     = next_id(doctors, "did", "D")
    name    = ask("Full Name (Dr.)")
    if not name:
        error("Name required."); return
    dept    = pick("Department", [
        "General Medicine","Cardiology","Neurology","Pediatrics",
        "Orthopedics","Dermatology","ENT","Ophthalmology","Oncology","Psychiatry"])
    phone   = ask("Phone")
    fee     = ask_float("Consultation Fee (₹)")
    exp     = ask_int("Years of Experience", 0, 60)
    rating  = round(min(5.0, max(1.0, 3.0 + math.log(exp+1) * 0.4)), 1)

    new_row = pd.DataFrame([[did,name,dept,phone,fee,exp,rating]], columns=DOCTOR_COLS)
    doctors = pd.concat([doctors, new_row], ignore_index=True)
    save(doctors, DOCTOR_FILE)

    box([
        f"Doctor Added!",
        f"ID         : {did}",
        f"Name       : Dr. {name}",
        f"Department : {dept}",
        f"Fee        : ₹{fee:.2f}",
        f"Experience : {exp} year(s)",
        f"Rating     : {'★' * int(rating)}{'☆' * (5-int(rating))} ({rating}/5.0)",
    ])
    pause()

def view_doctors():
    header("Doctor Directory", "🩺")
    doctors = load(DOCTOR_FILE, DOCTOR_COLS)
    dept_filter = ask("Filter by department (Enter to show all)")
    if dept_filter:
        doctors = doctors[doctors["dept"].str.contains(dept_filter, case=False, na=False)]
    # numpy: average fee
    if not doctors.empty:
        fees = pd.to_numeric(doctors["fee"], errors="coerce").dropna().values
        if len(fees):
            info(f"Count: {len(doctors)} | Avg Fee: ₹{np.mean(fees):.2f} | "
                 f"Min: ₹{np.min(fees):.2f} | Max: ₹{np.max(fees):.2f}")
    print_table(doctors)
    pause()

def doctor_leaderboard():
    header("Top Doctors by Rating", "🏆")
    doctors = load(DOCTOR_FILE, DOCTOR_COLS)
    if doctors.empty:
        warn("No doctors."); pause(); return
    doctors["rating"] = pd.to_numeric(doctors["rating"], errors="coerce")
    doctors["fee"]    = pd.to_numeric(doctors["fee"], errors="coerce")
    top = doctors.sort_values("rating", ascending=False).head(10)
    print()
    for rank, (_, row) in enumerate(top.iterrows(), 1):
        stars = "★" * int(row["rating"]) + "☆" * (5 - int(row["rating"]))
        print(f"  #{rank:<3} {stars}  Dr. {str(row['name']):<20} {str(row['dept']):<22}  ₹{row['fee']:.0f}")
    pause()

# ─────────────────────────────────────────────────────────
#  APPOINTMENT MODULE
# ─────────────────────────────────────────────────────────

def book_appointment():
    header("Book Appointment", "📅")
    patients = load(PATIENT_FILE, PATIENT_COLS)
    doctors  = load(DOCTOR_FILE, DOCTOR_COLS)
    appts    = load(APPOINTMENT_FILE, APPOINTMENT_COLS)

    if patients.empty:
        error("No patients registered."); pause(); return
    if doctors.empty:
        error("No doctors available."); pause(); return

    # Show patients
    print("\n  Available Patients:")
    for _, p in patients[["pid","name","ward"]].iterrows():
        print(f"    {p['pid']} — {p['name']} ({p['ward']})")

    pid = ask("\n  Enter Patient ID")
    if patients[patients["pid"] == pid].empty:
        error("Patient not found."); pause(); return

    # Show doctors
    print("\n  Available Doctors:")
    for _, d in doctors[["did","name","dept","fee"]].iterrows():
        print(f"    {d['did']} — Dr. {d['name']} ({d['dept']}) ₹{d['fee']}")

    did = ask("\n  Enter Doctor ID")
    if doctors[doctors["did"] == did].empty:
        error("Doctor not found."); pause(); return

    # Date picker using calendar
    today = date.today()
    print(f"\n  {calendar.month_name[today.month]} {today.year}")
    cal_str = calendar.month(today.year, today.month)
    for line_txt in cal_str.splitlines():
        print(f"    {line_txt}")

    appt_date = ask(f"\n  Appointment date (YYYY-MM-DD, default today {today})", str(today))
    try:
        appt_date_parsed = datetime.strptime(appt_date, "%Y-%m-%d").date()
        day_name = calendar.day_name[appt_date_parsed.weekday()]
        info(f"Day: {day_name}")
    except ValueError:
        error("Invalid date format."); pause(); return

    # Time slots
    slot = pick("Time Slot", [
        "08:00","09:00","10:00","11:00","12:00",
        "14:00","15:00","16:00","17:00","18:00"])
    reason = ask("Reason for visit")

    # Conflict check using pandas
    conflict = appts[(appts["did"]==did) & (appts["date"]==appt_date) & (appts["time"]==slot) & (appts["status"]=="Scheduled")]
    if not conflict.empty:
        error(f"Dr. is already booked at {slot} on {appt_date}."); pause(); return

    aid = next_id(appts, "aid", "A")
    new_row = pd.DataFrame([[aid, pid, did, appt_date, slot, reason, "Scheduled"]], columns=APPOINTMENT_COLS)
    appts = pd.concat([appts, new_row], ignore_index=True)
    save(appts, APPOINTMENT_FILE)

    pat_name = patients[patients["pid"]==pid]["name"].values[0]
    doc_name = doctors[doctors["did"]==did]["name"].values[0]
    box([
        "Appointment Booked!",
        f"ID       : {aid}",
        f"Patient  : {pat_name} ({pid})",
        f"Doctor   : Dr. {doc_name} ({did})",
        f"Date     : {appt_date} ({day_name})",
        f"Time     : {slot}",
        f"Reason   : {reason}",
    ])
    pause()

def view_appointments():
    header("All Appointments", "📋")
    appts    = load(APPOINTMENT_FILE, APPOINTMENT_COLS)
    patients = load(PATIENT_FILE, PATIENT_COLS)
    doctors  = load(DOCTOR_FILE, DOCTOR_COLS)

    if appts.empty:
        warn("No appointments."); pause(); return

    # Merge for display
    merged = (appts
              .merge(patients[["pid","name"]].rename(columns={"name":"patient"}), on="pid", how="left")
              .merge(doctors[["did","name"]].rename(columns={"name":"doctor"}), on="did", how="left"))

    status_filter = pick("Filter by status", ["All","Scheduled","Completed","Cancelled"])
    if status_filter != "All":
        merged = merged[merged["status"] == status_filter]

    display = merged[["aid","patient","doctor","date","time","reason","status"]]
    info(f"Total: {len(display)}")
    print_table(display)
    pause()

def update_appointment():
    header("Update Appointment Status", "✏️")
    appts = load(APPOINTMENT_FILE, APPOINTMENT_COLS)
    if appts.empty:
        warn("No appointments."); pause(); return

    aid = ask("Enter Appointment ID")
    row = appts[appts["aid"] == aid]
    if row.empty:
        error("Appointment not found."); pause(); return

    cur = row.iloc[0]["status"]
    info(f"Current status: {cur}")
    new_status = pick("New Status", ["Scheduled","Completed","Cancelled"])
    appts.loc[appts["aid"] == aid, "status"] = new_status
    save(appts, APPOINTMENT_FILE)
    success(f"Appointment {aid} updated to '{new_status}'.")
    pause()

def monthly_calendar():
    header("Monthly Appointment Calendar", "🗓️")
    appts = load(APPOINTMENT_FILE, APPOINTMENT_COLS)

    today = date.today()
    yr  = ask_int(f"Year  (default {today.year})", 2000, 2100)
    mo  = ask_int(f"Month (1–12, default {today.month})", 1, 12)
    yr  = yr if yr != 0 else today.year
    mo  = mo if mo != 0 else today.month

    cal_str = calendar.month(yr, mo)
    print(f"\n  {'─'*30}")
    for ln in cal_str.splitlines():
        print(f"  {ln}")
    print(f"  {'─'*30}")

    month_appts = appts[appts["date"].str.startswith(f"{yr}-{mo:02d}", na=False)]
    if month_appts.empty:
        info("No appointments this month.")
    else:
        info(f"{len(month_appts)} appointment(s) in {calendar.month_name[mo]} {yr}")
        # Group by date using pandas
        by_day = month_appts.groupby("date").size().sort_index()
        print()
        for d, cnt in by_day.items():
            bar = "▓" * int(cnt)
            print(f"    {d}  {bar} {cnt}")
    pause()

# ─────────────────────────────────────────────────────────
#  BILLING MODULE
# ─────────────────────────────────────────────────────────

def generate_bill():
    header("Generate Bill", "💰")
    patients = load(PATIENT_FILE, PATIENT_COLS)
    appts    = load(APPOINTMENT_FILE, APPOINTMENT_COLS)
    bills    = load(BILL_FILE, BILL_COLS)

    if patients.empty:
        error("No patients."); pause(); return

    print("\n  Patients:")
    for _, p in patients[["pid","name"]].iterrows():
        print(f"    {p['pid']} — {p['name']}")
    pid = ask("\n  Patient ID")
    if patients[patients["pid"]==pid].empty:
        error("Patient not found."); pause(); return
    pat_name = patients[patients["pid"]==pid]["name"].values[0]

    aid = ask("Appointment ID (Enter to skip)")

    print(f"\n  Billing for: {pat_name}")
    line()
    consult = ask_float("Consultation fee (₹)")
    meds    = ask_float("Medicine charges (₹)")
    room    = ask_float("Room/ward charges (₹)")
    tests   = ask_float("Tests/diagnostics (₹)")
    disc    = ask_float("Discount (₹, 0 if none)")

    # numpy calculations
    charges  = np.array([consult, meds, room, tests])
    subtotal = float(np.sum(charges))
    gst_rate = 0.05
    gst      = round(subtotal * gst_rate, 2)
    total    = round(subtotal + gst - disc, 2)

    # math: ceiling for insurance purposes
    insurance_ceil = math.ceil(total / 100) * 100

    box([
        f"══ BILL SUMMARY — {pat_name} ({pid}) ══",
        f"  Consultation  : ₹{consult:>10.2f}",
        f"  Medicines     : ₹{meds:>10.2f}",
        f"  Room Charges  : ₹{room:>10.2f}",
        f"  Tests         : ₹{tests:>10.2f}",
        f"  {'─'*35}",
        f"  Subtotal      : ₹{subtotal:>10.2f}",
        f"  GST (5%)      : ₹{gst:>10.2f}",
        f"  Discount      : ₹{disc:>10.2f}",
        f"  {'─'*35}",
        f"  TOTAL DUE     : ₹{total:>10.2f}",
        f"  Ins. Ceiling  : ₹{insurance_ceil:>10.2f}",
    ])

    confirm = ask("Save this bill? (yes/no)")
    if confirm.lower() == "yes":
        bid = next_id(bills, "bid", "B")
        today = date.today().strftime("%Y-%m-%d")
        new_row = pd.DataFrame(
            [[bid, pid, aid, consult, meds, room, tests, disc, total, "Pending", today]],
            columns=BILL_COLS)
        bills = pd.concat([bills, new_row], ignore_index=True)
        save(bills, BILL_FILE)
        success(f"Bill {bid} saved. Total: ₹{total:.2f}")
    pause()

def view_bills():
    header("All Bills", "🧾")
    bills    = load(BILL_FILE, BILL_COLS)
    patients = load(PATIENT_FILE, PATIENT_COLS)
    if bills.empty:
        warn("No bills generated."); pause(); return

    merged = bills.merge(patients[["pid","name"]], on="pid", how="left")
    merged["total"] = pd.to_numeric(merged["total"], errors="coerce")

    # numpy stats
    totals = merged["total"].dropna().values
    if len(totals):
        info(f"Bills: {len(totals)} | Total Revenue: ₹{np.sum(totals):.2f} | "
             f"Avg: ₹{np.mean(totals):.2f} | Max: ₹{np.max(totals):.2f}")

    display = merged[["bid","name","total","status","date"]]
    print_table(display)

    # Pending vs paid summary
    pending = merged[merged["status"]=="Pending"]["total"].sum()
    paid    = merged[merged["status"]=="Paid"]["total"].sum()
    print(f"\n  Collected: ₹{paid:.2f}   |   Pending: ₹{pending:.2f}")
    pause()

def mark_bill_paid():
    header("Mark Bill as Paid", "✅")
    bills = load(BILL_FILE, BILL_COLS)
    if bills.empty:
        warn("No bills."); pause(); return

    bid = ask("Enter Bill ID")
    if bills[bills["bid"]==bid].empty:
        error("Bill not found."); pause(); return

    bills.loc[bills["bid"]==bid, "status"] = "Paid"
    save(bills, BILL_FILE)
    success(f"Bill {bid} marked as Paid.")
    pause()

# ─────────────────────────────────────────────────────────
#  ANALYTICS MODULE
# ─────────────────────────────────────────────────────────

def analytics_dashboard():
    header("Analytics Dashboard", "📈")
    patients = load(PATIENT_FILE, PATIENT_COLS)
    doctors  = load(DOCTOR_FILE, DOCTOR_COLS)
    appts    = load(APPOINTMENT_FILE, APPOINTMENT_COLS)
    bills    = load(BILL_FILE, BILL_COLS)

    print()
    # ── KPI Cards ──
    n_pat  = len(patients)
    n_doc  = len(doctors)
    n_appt = len(appts)
    n_bill = len(bills)

    kpis = [
        ("Patients",     n_pat,  "👥"),
        ("Doctors",      n_doc,  "👨‍⚕️"),
        ("Appointments", n_appt, "📅"),
        ("Bills",        n_bill, "💰"),
    ]
    print("  ┌──────────────────┬──────────────────┬──────────────────┬──────────────────┐")
    print("  │" + "│".join(f"  {icon} {label:<14}" for label,_,icon in kpis) + "│")
    print("  │" + "│".join(f"  {str(val):<16}" for _,val,_ in kpis) + "│")
    print("  └──────────────────┴──────────────────┴──────────────────┴──────────────────┘")

    # ── Financial Summary ──
    if not bills.empty:
        bills["total"]  = pd.to_numeric(bills["total"], errors="coerce").fillna(0)
        total_rev  = bills["total"].sum()
        paid_rev   = bills[bills["status"]=="Paid"]["total"].sum()
        pend_rev   = bills[bills["status"]=="Pending"]["total"].sum()
        avg_bill   = bills["total"].mean()
        # scipy: 95% confidence interval for average bill
        if len(bills) >= 2:
            ci = stats.t.interval(0.95, df=len(bills)-1,
                                  loc=float(np.mean(bills["total"].values)),
                                  scale=float(stats.sem(bills["total"].values)))
            ci_str = f"95% CI: ₹{ci[0]:.2f} – ₹{ci[1]:.2f}"
        else:
            ci_str = "Not enough data for CI"

        print()
        box([
            "── Financial Overview ──",
            f"  Total Revenue   : ₹{total_rev:>12.2f}",
            f"  Collected       : ₹{paid_rev:>12.2f}",
            f"  Pending         : ₹{pend_rev:>12.2f}",
            f"  Avg Bill        : ₹{avg_bill:>12.2f}",
            f"  {ci_str}",
        ])

    # ── Appointment Status Breakdown ──
    if not appts.empty:
        print()
        print("  Appointment Status:")
        status_counts = appts["status"].value_counts()
        total_a = len(appts)
        for s, cnt in status_counts.items():
            pct = cnt/total_a*100
            bar = "█" * int(pct/5)
            print(f"    {s:<12} {bar:<22} {cnt:>3} ({pct:.1f}%)")

    # ── Weekly appointment trend (last 4 weeks) ──
    if not appts.empty:
        appts["date"] = pd.to_datetime(appts["date"], errors="coerce")
        today_dt = pd.Timestamp(date.today())
        print()
        print("  Appointments — last 4 weeks:")
        for w in range(3, -1, -1):
            wstart = today_dt - timedelta(weeks=w+1)
            wend   = today_dt - timedelta(weeks=w)
            cnt    = ((appts["date"] >= wstart) & (appts["date"] < wend)).sum()
            bar    = "▓" * int(cnt)
            label  = wstart.strftime("%d %b")
            print(f"    {label}  {bar:<20} {cnt}")

    # ── Doctor dept distribution ──
    if not doctors.empty:
        print()
        print("  Doctors by Department:")
        dept_counts = doctors["dept"].value_counts()
        for dept, cnt in dept_counts.items():
            bar = "█" * cnt
            print(f"    {dept:<22} {bar:<15} {cnt}")

    pause()

# ─────────────────────────────────────────────────────────
#  UTILITIES
# ─────────────────────────────────────────────────────────

def bmi_calculator():
    header("BMI Calculator", "⚖️")
    weight = ask_float("Weight (kg)")
    height = ask_float("Height (cm)")
    h_m = height / 100
    bmi = round(weight / (h_m ** 2), 2)
    # math functions
    ideal_low  = round(18.5 * h_m ** 2, 1)
    ideal_high = round(24.9 * h_m ** 2, 1)
    category = (
        "Severely Underweight" if bmi < 16 else
        "Underweight"          if bmi < 18.5 else
        "Normal weight"        if bmi < 25 else
        "Overweight"           if bmi < 30 else
        "Obese Class I"        if bmi < 35 else
        "Obese Class II"       if bmi < 40 else
        "Obese Class III"
    )
    # scipy: z-score vs population mean (WHO avg ~22)
    pop_mean, pop_std = 22.0, 4.0
    z = round((bmi - pop_mean) / pop_std, 2)
    percentile = round(float(stats.norm.cdf(z) * 100), 1)

    box([
        f"BMI Result",
        f"  Weight     : {weight} kg",
        f"  Height     : {height} cm",
        f"  BMI        : {bmi}",
        f"  Category   : {category}",
        f"  Ideal Range: {ideal_low} – {ideal_high} kg",
        f"  Z-score    : {z}  (Percentile: {percentile}%)",
    ])
    pause()

def drug_dose_calculator():
    header("Paediatric Drug Dose (mg/kg)", "💊")
    weight = ask_float("Child weight (kg)")
    dose_per_kg = ask_float("Prescribed dose (mg/kg)")
    freq  = ask_int("Times per day", 1, 6)
    days  = ask_int("Duration (days)", 1, 90)

    single_dose = round(weight * dose_per_kg, 2)
    daily_dose  = round(single_dose * freq, 2)
    total_dose  = round(daily_dose * days, 2)

    # numpy linspace: dosing schedule
    times_arr = np.linspace(0, 24, freq, endpoint=False)
    schedule  = [f"{int(t):02d}:{int((t%1)*60):02d}" for t in times_arr]

    box([
        f"Dose Calculation",
        f"  Single dose  : {single_dose} mg",
        f"  Daily dose   : {daily_dose} mg  ({freq}× per day)",
        f"  Total course : {total_dose} mg  ({days} days)",
        f"  Schedule     : {', '.join(schedule)}",
    ])
    pause()

def age_calculator():
    header("Age & Date Calculator", "🎂")
    dob_str = ask("Date of birth (YYYY-MM-DD)")
    try:
        dob = datetime.strptime(dob_str, "%Y-%m-%d").date()
    except ValueError:
        error("Invalid date format."); pause(); return

    today_d = date.today()
    delta   = today_d - dob
    total_days = delta.days
    years  = total_days // 365
    months = (total_days % 365) // 30
    days   = total_days % 30

    # next birthday
    try:
        next_bday = dob.replace(year=today_d.year)
        if next_bday < today_d:
            next_bday = dob.replace(year=today_d.year + 1)
        days_to_bday = (next_bday - today_d).days
    except ValueError:
        days_to_bday = "N/A"

    # calendar: day of birth
    day_of_week = calendar.day_name[dob.weekday()]
    week_num    = dob.isocalendar()[1]

    box([
        f"Age Details",
        f"  Date of Birth   : {dob_str} ({day_of_week})",
        f"  Age             : {years} yr  {months} mo  {days} day(s)",
        f"  Total Days      : {total_days:,}",
        f"  Total Weeks     : {total_days // 7:,}",
        f"  Birth Week No.  : {week_num}",
        f"  Next Birthday   : {next_bday} (in {days_to_bday} day(s))",
    ])
    pause()

def export_report():
    header("Export Reports", "📤")
    print()
    print("  Choose data to export:")
    choice = pick("Export", ["Patients","Doctors","Appointments","Bills","All"])
    exports = {
        "Patients":     (PATIENT_FILE,     PATIENT_COLS,     "patients_report.csv"),
        "Doctors":      (DOCTOR_FILE,      DOCTOR_COLS,      "doctors_report.csv"),
        "Appointments": (APPOINTMENT_FILE, APPOINTMENT_COLS, "appointments_report.csv"),
        "Bills":        (BILL_FILE,        BILL_COLS,        "bills_report.csv"),
    }
    items = list(exports.items()) if choice == "All" else [(choice, exports[choice])]
    for name, (src, cols, out) in items:
        df = load(src, cols)
        if not df.empty:
            # pandas describe for numeric columns
            numeric_df = df.select_dtypes(include=[np.number])
            df.to_csv(out, index=False)
            success(f"{name} exported → {out}  ({len(df)} records)")
        else:
            warn(f"{name}: no data to export.")
    pause()

# ─────────────────────────────────────────────────────────
#  MENUS
# ─────────────────────────────────────────────────────────

def patient_menu():
    while True:
        header("Patient Management", "👥")
        options = [
            "Register New Patient",
            "View / Search Patients",
            "Discharge Patient",
            "Patient Statistics",
            "Back",
        ]
        for i, o in enumerate(options, 1):
            print(f"    [{i}] {o}")
        ch = ask("\n  Choice")
        if ch == "1": add_patient()
        elif ch == "2": view_patients()
        elif ch == "3": discharge_patient()
        elif ch == "4": patient_stats()
        elif ch == "5": break
        else: warn("Invalid option.")

def doctor_menu():
    while True:
        header("Doctor Management", "👨‍⚕️")
        options = [
            "Add New Doctor",
            "View Doctors",
            "Top Doctors Leaderboard",
            "Back",
        ]
        for i, o in enumerate(options, 1):
            print(f"    [{i}] {o}")
        ch = ask("\n  Choice")
        if ch == "1": add_doctor()
        elif ch == "2": view_doctors()
        elif ch == "3": doctor_leaderboard()
        elif ch == "4": break
        else: warn("Invalid option.")

def appointment_menu():
    while True:
        header("Appointments", "📅")
        options = [
            "Book Appointment",
            "View All Appointments",
            "Update Appointment Status",
            "Monthly Calendar View",
            "Back",
        ]
        for i, o in enumerate(options, 1):
            print(f"    [{i}] {o}")
        ch = ask("\n  Choice")
        if ch == "1": book_appointment()
        elif ch == "2": view_appointments()
        elif ch == "3": update_appointment()
        elif ch == "4": monthly_calendar()
        elif ch == "5": break
        else: warn("Invalid option.")

def billing_menu():
    while True:
        header("Billing", "💰")
        options = [
            "Generate Bill",
            "View All Bills",
            "Mark Bill as Paid",
            "Back",
        ]
        for i, o in enumerate(options, 1):
            print(f"    [{i}] {o}")
        ch = ask("\n  Choice")
        if ch == "1": generate_bill()
        elif ch == "2": view_bills()
        elif ch == "3": mark_bill_paid()
        elif ch == "4": break
        else: warn("Invalid option.")

def utilities_menu():
    while True:
        header("Utilities & Calculators", "🔧")
        options = [
            "BMI Calculator (+ scipy z-score)",
            "Paediatric Drug Dose Calculator",
            "Age & Date Calculator",
            "Export Reports to CSV",
            "Back",
        ]
        for i, o in enumerate(options, 1):
            print(f"    [{i}] {o}")
        ch = ask("\n  Choice")
        if ch == "1": bmi_calculator()
        elif ch == "2": drug_dose_calculator()
        elif ch == "3": age_calculator()
        elif ch == "4": export_report()
        elif ch == "5": break
        else: warn("Invalid option.")

def main_menu():
    while True:
        print()
        line("═")
        print("║" + "  🏥  MEDICORE HOSPITAL MANAGEMENT SYSTEM  ".center(W-2) + "║")
        print("║" + f"  {datetime.now().strftime('%A, %d %B %Y  |  %H:%M')}  ".center(W-2) + "║")
        line("═")
        menu = [
            ("1", "👥  Patient Management"),
            ("2", "👨‍⚕️  Doctor Management"),
            ("3", "📅  Appointments"),
            ("4", "💰  Billing"),
            ("5", "📈  Analytics Dashboard"),
            ("6", "🔧  Utilities & Calculators"),
            ("0", "🚪  Exit"),
        ]
        print()
        for key, label in menu:
            print(f"    [{key}]  {label}")
        print()
        line()
        ch = ask("  Select option")

        if   ch == "1": patient_menu()
        elif ch == "2": doctor_menu()
        elif ch == "3": appointment_menu()
        elif ch == "4": billing_menu()
        elif ch == "5": analytics_dashboard()
        elif ch == "6": utilities_menu()
        elif ch == "0":
            print()
            box("Thank you for using MediCore. Stay healthy! 🏥")
            print()
            break
        else:
            warn("Invalid option. Please try again.")


# ─────────────────────────────────────────────────────────
#  ENTRY POINT
# ─────────────────────────────────────────────────────────

if __name__ == "__main__":
    main_menu()
"""
Hospital Management System
Built with Python OOP + Tkinter
Modules: Patients, Doctors, Appointments, Billing
"""

import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime
import uuid


# ─────────────────────────────────────────────
# DATABASE LAYER
# ─────────────────────────────────────────────

class Database:
    """Singleton database connection manager."""
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.conn = sqlite3.connect("hospital.db", check_same_thread=False)
            cls._instance._create_tables()
        return cls._instance

    def _create_tables(self):
        c = self.conn.cursor()
        c.executescript("""
            CREATE TABLE IF NOT EXISTS patients (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                age INTEGER,
                gender TEXT,
                phone TEXT,
                blood_group TEXT,
                address TEXT,
                created_at TEXT
            );
            CREATE TABLE IF NOT EXISTS doctors (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                specialization TEXT,
                phone TEXT,
                fee REAL,
                available_days TEXT,
                created_at TEXT
            );
            CREATE TABLE IF NOT EXISTS appointments (
                id TEXT PRIMARY KEY,
                patient_id TEXT,
                doctor_id TEXT,
                date TEXT,
                time TEXT,
                reason TEXT,
                status TEXT DEFAULT 'Scheduled',
                created_at TEXT,
                FOREIGN KEY(patient_id) REFERENCES patients(id),
                FOREIGN KEY(doctor_id) REFERENCES doctors(id)
            );
            CREATE TABLE IF NOT EXISTS bills (
                id TEXT PRIMARY KEY,
                patient_id TEXT,
                appointment_id TEXT,
                amount REAL,
                description TEXT,
                status TEXT DEFAULT 'Pending',
                created_at TEXT,
                FOREIGN KEY(patient_id) REFERENCES patients(id)
            );
        """)
        self.conn.commit()

    def execute(self, query, params=()):
        c = self.conn.cursor()
        c.execute(query, params)
        self.conn.commit()
        return c

    def fetchall(self, query, params=()):
        return self.execute(query, params).fetchall()

    def fetchone(self, query, params=()):
        return self.execute(query, params).fetchone()


# ─────────────────────────────────────────────
# MODEL CLASSES
# ─────────────────────────────────────────────

class Person:
    """Base class for Patient and Doctor."""
    def __init__(self, name, phone):
        self.id = str(uuid.uuid4())[:8].upper()
        self.name = name
        self.phone = phone
        self.created_at = datetime.now().strftime("%Y-%m-%d %H:%M")


class Patient(Person):
    def __init__(self, name, age, gender, phone, blood_group, address):
        super().__init__(name, phone)
        self.age = age
        self.gender = gender
        self.blood_group = blood_group
        self.address = address

    def save(self):
        db = Database()
        db.execute(
            "INSERT INTO patients VALUES (?,?,?,?,?,?,?,?)",
            (self.id, self.name, self.age, self.gender,
             self.phone, self.blood_group, self.address, self.created_at)
        )

    @staticmethod
    def get_all():
        return Database().fetchall("SELECT * FROM patients ORDER BY created_at DESC")

    @staticmethod
    def search(query):
        q = f"%{query}%"
        return Database().fetchall(
            "SELECT * FROM patients WHERE name LIKE ? OR id LIKE ? OR phone LIKE ?", (q, q, q))

    @staticmethod
    def delete(patient_id):
        Database().execute("DELETE FROM patients WHERE id=?", (patient_id,))


class Doctor(Person):
    def __init__(self, name, specialization, phone, fee, available_days):
        super().__init__(name, phone)
        self.specialization = specialization
        self.fee = fee
        self.available_days = available_days

    def save(self):
        db = Database()
        db.execute(
            "INSERT INTO doctors VALUES (?,?,?,?,?,?,?)",
            (self.id, self.name, self.specialization,
             self.phone, self.fee, self.available_days, self.created_at)
        )

    @staticmethod
    def get_all():
        return Database().fetchall("SELECT * FROM doctors ORDER BY name")

    @staticmethod
    def delete(doctor_id):
        Database().execute("DELETE FROM doctors WHERE id=?", (doctor_id,))


class Appointment:
    def __init__(self, patient_id, doctor_id, date, time, reason):
        self.id = str(uuid.uuid4())[:8].upper()
        self.patient_id = patient_id
        self.doctor_id = doctor_id
        self.date = date
        self.time = time
        self.reason = reason
        self.status = "Scheduled"
        self.created_at = datetime.now().strftime("%Y-%m-%d %H:%M")

    def save(self):
        Database().execute(
            "INSERT INTO appointments VALUES (?,?,?,?,?,?,?,?)",
            (self.id, self.patient_id, self.doctor_id,
             self.date, self.time, self.reason, self.status, self.created_at)
        )

    @staticmethod
    def get_all():
        return Database().fetchall("""
            SELECT a.id, p.name, d.name, a.date, a.time, a.reason, a.status
            FROM appointments a
            JOIN patients p ON a.patient_id = p.id
            JOIN doctors d ON a.doctor_id = d.id
            ORDER BY a.date DESC, a.time DESC
        """)

    @staticmethod
    def update_status(appt_id, status):
        Database().execute("UPDATE appointments SET status=? WHERE id=?", (status, appt_id))


class Bill:
    def __init__(self, patient_id, appointment_id, amount, description):
        self.id = str(uuid.uuid4())[:8].upper()
        self.patient_id = patient_id
        self.appointment_id = appointment_id
        self.amount = amount
        self.description = description
        self.status = "Pending"
        self.created_at = datetime.now().strftime("%Y-%m-%d %H:%M")

    def save(self):
        Database().execute(
            "INSERT INTO bills VALUES (?,?,?,?,?,?,?)",
            (self.id, self.patient_id, self.appointment_id,
             self.amount, self.description, self.status, self.created_at)
        )

    @staticmethod
    def get_all():
        return Database().fetchall("""
            SELECT b.id, p.name, b.amount, b.description, b.status, b.created_at
            FROM bills b JOIN patients p ON b.patient_id = p.id
            ORDER BY b.created_at DESC
        """)

    @staticmethod
    def mark_paid(bill_id):
        Database().execute("UPDATE bills SET status='Paid' WHERE id=?", (bill_id,))


# ─────────────────────────────────────────────
# UI THEME & STYLES
# ─────────────────────────────────────────────

COLORS = {
    "bg":        "#F0F4F8",
    "sidebar":   "#1A2B4A",
    "sidebar_h": "#2C4170",
    "accent":    "#2563EB",
    "accent2":   "#059669",
    "danger":    "#DC2626",
    "white":     "#FFFFFF",
    "card":      "#FFFFFF",
    "text":      "#1E293B",
    "muted":     "#64748B",
    "border":    "#E2E8F0",
    "header_bg": "#1A2B4A",
}

FONTS = {
    "title":  ("Segoe UI", 22, "bold"),
    "head":   ("Segoe UI", 13, "bold"),
    "body":   ("Segoe UI", 11),
    "small":  ("Segoe UI", 10),
    "btn":    ("Segoe UI", 10, "bold"),
    "sidebar":("Segoe UI", 11),
}


# ─────────────────────────────────────────────
# REUSABLE UI COMPONENTS
# ─────────────────────────────────────────────

class StyledButton(tk.Button):
    def __init__(self, parent, text, command=None, color=None, **kwargs):
        bg = color or COLORS["accent"]
        super().__init__(
            parent, text=text, command=command,
            bg=bg, fg="white",
            font=FONTS["btn"],
            relief="flat", cursor="hand2",
            padx=14, pady=6,
            activebackground=COLORS["accent2"],
            activeforeground="white",
            **kwargs
        )
        self.bind("<Enter>", lambda e: self.config(bg=COLORS["sidebar_h"]))
        self.bind("<Leave>", lambda e: self.config(bg=bg))


class FormField:
    """Helper that creates a label + entry pair."""
    def __init__(self, parent, label, row, col=0, width=28, values=None):
        tk.Label(parent, text=label, font=FONTS["small"],
                 bg=COLORS["white"], fg=COLORS["muted"]).grid(
            row=row, column=col*2, padx=(10,4), pady=4, sticky="w")
        if values:
            self.var = tk.StringVar()
            self.widget = ttk.Combobox(parent, textvariable=self.var,
                                       values=values, width=width, state="readonly")
            if values:
                self.widget.set(values[0])
        else:
            self.widget = tk.Entry(parent, font=FONTS["body"],
                                   width=width, relief="solid",
                                   highlightthickness=1,
                                   highlightcolor=COLORS["accent"],
                                   bd=1)
        self.widget.grid(row=row, column=col*2+1, padx=(0,14), pady=4, sticky="ew")

    def get(self):
        if hasattr(self, 'var'):
            return self.var.get()
        return self.widget.get().strip()

    def clear(self):
        if hasattr(self, 'var'):
            self.var.set("")
        else:
            self.widget.delete(0, tk.END)


class DataTable(tk.Frame):
    """Reusable treeview table with scrollbar."""
    def __init__(self, parent, columns, headings, col_widths=None, **kwargs):
        super().__init__(parent, bg=COLORS["bg"], **kwargs)
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Hospital.Treeview",
                        background=COLORS["white"],
                        foreground=COLORS["text"],
                        rowheight=28,
                        fieldbackground=COLORS["white"],
                        font=FONTS["small"])
        style.configure("Hospital.Treeview.Heading",
                        background=COLORS["sidebar"],
                        foreground="white",
                        font=FONTS["btn"],
                        relief="flat")
        style.map("Hospital.Treeview",
                  background=[("selected", COLORS["accent"])],
                  foreground=[("selected", "white")])

        self.tree = ttk.Treeview(self, columns=columns, show="headings",
                                  style="Hospital.Treeview")
        for col, head in zip(columns, headings):
            self.tree.heading(col, text=head)
        if col_widths:
            for col, w in zip(columns, col_widths):
                self.tree.column(col, width=w, anchor="center")

        sb = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=sb.set)
        self.tree.pack(side="left", fill="both", expand=True)
        sb.pack(side="right", fill="y")

    def load(self, rows, tag_col=None, tag_map=None):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for r in rows:
            tag = ""
            if tag_col is not None and tag_map:
                val = r[tag_col]
                tag = tag_map.get(val, "")
            self.tree.insert("", "end", values=r, tags=(tag,))
        if tag_map:
            for tag, color in [("Paid", "#D1FAE5"), ("Scheduled", "#DBEAFE"),
                                ("Completed", "#D1FAE5"), ("Cancelled", "#FEE2E2"),
                                ("Pending", "#FEF3C7")]:
                self.tree.tag_configure(tag, background=color)

    def selected_values(self):
        sel = self.tree.selection()
        if sel:
            return self.tree.item(sel[0])["values"]
        return None


# ─────────────────────────────────────────────
# MODULE PANELS
# ─────────────────────────────────────────────

class PatientPanel(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=COLORS["bg"])
        self._build()

    def _build(self):
        # Header
        hdr = tk.Frame(self, bg=COLORS["header_bg"], pady=12)
        hdr.pack(fill="x")
        tk.Label(hdr, text="🏥  Patient Management", font=FONTS["title"],
                 bg=COLORS["header_bg"], fg="white").pack(side="left", padx=20)

        # Form card
        card = tk.Frame(self, bg=COLORS["white"], padx=10, pady=10,
                        highlightbackground=COLORS["border"], highlightthickness=1)
        card.pack(fill="x", padx=16, pady=(12, 6))
        tk.Label(card, text="Register New Patient", font=FONTS["head"],
                 bg=COLORS["white"], fg=COLORS["text"]).grid(
            row=0, column=0, columnspan=4, sticky="w", padx=10, pady=(4,8))

        self.f_name   = FormField(card, "Full Name",    1, 0)
        self.f_age    = FormField(card, "Age",          1, 1, width=14)
        self.f_gender = FormField(card, "Gender",       2, 0, values=["Male","Female","Other"])
        self.f_blood  = FormField(card, "Blood Group",  2, 1, width=14,
                                  values=["A+","A-","B+","B-","AB+","AB-","O+","O-"])
        self.f_phone  = FormField(card, "Phone",        3, 0)
        self.f_addr   = FormField(card, "Address",      3, 1)

        btn_row = tk.Frame(card, bg=COLORS["white"])
        btn_row.grid(row=4, column=0, columnspan=4, pady=8, sticky="w", padx=10)
        StyledButton(btn_row, "Add Patient", self._add).pack(side="left", padx=(0,8))
        StyledButton(btn_row, "Delete Selected", self._delete,
                     color=COLORS["danger"]).pack(side="left")

        # Search bar
        sf = tk.Frame(self, bg=COLORS["bg"])
        sf.pack(fill="x", padx=16, pady=(4,2))
        tk.Label(sf, text="Search:", font=FONTS["body"],
                 bg=COLORS["bg"], fg=COLORS["muted"]).pack(side="left")
        self.search_var = tk.StringVar()
        se = tk.Entry(sf, textvariable=self.search_var, font=FONTS["body"],
                      width=30, relief="solid", bd=1)
        se.pack(side="left", padx=6)
        self.search_var.trace("w", lambda *a: self._load())

        # Table
        cols = ("id","name","age","gender","phone","blood","address","joined")
        heads = ("ID","Name","Age","Gender","Phone","Blood","Address","Joined")
        widths = (70,150,50,70,100,60,160,120)
        self.table = DataTable(self, cols, heads, widths)
        self.table.pack(fill="both", expand=True, padx=16, pady=8)
        self._load()

    def _add(self):
        name  = self.f_name.get()
        age   = self.f_age.get()
        phone = self.f_phone.get()
        if not name or not age or not phone:
            messagebox.showwarning("Missing Fields", "Name, Age and Phone are required.")
            return
        try:
            age = int(age)
        except ValueError:
            messagebox.showerror("Invalid", "Age must be a number.")
            return
        p = Patient(name, age, self.f_gender.get(), phone,
                    self.f_blood.get(), self.f_addr.get())
        p.save()
        for f in [self.f_name, self.f_age, self.f_phone, self.f_addr]:
            f.clear()
        self._load()
        messagebox.showinfo("Success", f"Patient '{name}' registered (ID: {p.id})")

    def _delete(self):
        v = self.table.selected_values()
        if not v:
            messagebox.showwarning("Select", "Please select a patient to delete.")
            return
        if messagebox.askyesno("Confirm", f"Delete patient '{v[1]}'?"):
            Patient.delete(v[0])
            self._load()

    def _load(self):
        q = self.search_var.get() if hasattr(self, 'search_var') else ""
        rows = Patient.search(q) if q else Patient.get_all()
        self.table.load(rows)


class DoctorPanel(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=COLORS["bg"])
        self._build()

    def _build(self):
        hdr = tk.Frame(self, bg=COLORS["header_bg"], pady=12)
        hdr.pack(fill="x")
        tk.Label(hdr, text="👨‍⚕️  Doctor Management", font=FONTS["title"],
                 bg=COLORS["header_bg"], fg="white").pack(side="left", padx=20)

        card = tk.Frame(self, bg=COLORS["white"], padx=10, pady=10,
                        highlightbackground=COLORS["border"], highlightthickness=1)
        card.pack(fill="x", padx=16, pady=(12,6))
        tk.Label(card, text="Add New Doctor", font=FONTS["head"],
                 bg=COLORS["white"], fg=COLORS["text"]).grid(
            row=0, column=0, columnspan=4, sticky="w", padx=10, pady=(4,8))

        specs = ["General Medicine","Cardiology","Neurology","Pediatrics",
                 "Orthopedics","Dermatology","ENT","Ophthalmology","Oncology","Psychiatry"]
        self.f_name  = FormField(card, "Full Name",       1, 0)
        self.f_spec  = FormField(card, "Specialization",  1, 1, values=specs)
        self.f_phone = FormField(card, "Phone",           2, 0)
        self.f_fee   = FormField(card, "Consultation Fee",2, 1, width=14)
        self.f_days  = FormField(card, "Available Days",  3, 0)

        btn_row = tk.Frame(card, bg=COLORS["white"])
        btn_row.grid(row=4, column=0, columnspan=4, pady=8, sticky="w", padx=10)
        StyledButton(btn_row, "Add Doctor", self._add).pack(side="left", padx=(0,8))
        StyledButton(btn_row, "Delete Selected", self._delete,
                     color=COLORS["danger"]).pack(side="left")

        cols = ("id","name","spec","phone","fee","days","joined")
        heads = ("ID","Name","Specialization","Phone","Fee (₹)","Available Days","Joined")
        widths = (70,150,130,100,70,150,110)
        self.table = DataTable(self, cols, heads, widths)
        self.table.pack(fill="both", expand=True, padx=16, pady=8)
        self._load()

    def _add(self):
        name  = self.f_name.get()
        phone = self.f_phone.get()
        fee   = self.f_fee.get()
        if not name or not phone or not fee:
            messagebox.showwarning("Missing Fields", "Name, Phone and Fee are required.")
            return
        try:
            fee = float(fee)
        except ValueError:
            messagebox.showerror("Invalid", "Fee must be a number.")
            return
        d = Doctor(name, self.f_spec.get(), phone, fee, self.f_days.get())
        d.save()
        for f in [self.f_name, self.f_phone, self.f_fee, self.f_days]:
            f.clear()
        self._load()
        messagebox.showinfo("Success", f"Dr. '{name}' added (ID: {d.id})")

    def _delete(self):
        v = self.table.selected_values()
        if not v:
            messagebox.showwarning("Select", "Please select a doctor to delete.")
            return
        if messagebox.askyesno("Confirm", f"Delete Dr. '{v[1]}'?"):
            Doctor.delete(v[0])
            self._load()

    def _load(self):
        self.table.load(Doctor.get_all())


class AppointmentPanel(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=COLORS["bg"])
        self._build()

    def _build(self):
        hdr = tk.Frame(self, bg=COLORS["header_bg"], pady=12)
        hdr.pack(fill="x")
        tk.Label(hdr, text="📅  Appointments", font=FONTS["title"],
                 bg=COLORS["header_bg"], fg="white").pack(side="left", padx=20)

        card = tk.Frame(self, bg=COLORS["white"], padx=10, pady=10,
                        highlightbackground=COLORS["border"], highlightthickness=1)
        card.pack(fill="x", padx=16, pady=(12,6))
        tk.Label(card, text="Book Appointment", font=FONTS["head"],
                 bg=COLORS["white"], fg=COLORS["text"]).grid(
            row=0, column=0, columnspan=4, sticky="w", padx=10, pady=(4,8))

        # Patient ID dropdown
        self.f_pat = FormField(card, "Patient ID", 1, 0, values=self._get_patient_ids())
        self.f_doc = FormField(card, "Doctor ID",  1, 1, width=20, values=self._get_doctor_ids())
        self.f_date = FormField(card, "Date (YYYY-MM-DD)", 2, 0)
        self.f_time = FormField(card, "Time (HH:MM)", 2, 1, width=14)
        self.f_reason = FormField(card, "Reason", 3, 0)

        btn_row = tk.Frame(card, bg=COLORS["white"])
        btn_row.grid(row=4, column=0, columnspan=4, pady=8, sticky="w", padx=10)
        StyledButton(btn_row, "Book Appointment", self._book).pack(side="left", padx=(0,8))
        StyledButton(btn_row, "Mark Completed", self._complete,
                     color=COLORS["accent2"]).pack(side="left", padx=(0,8))
        StyledButton(btn_row, "Cancel Appointment", self._cancel,
                     color=COLORS["danger"]).pack(side="left")

        cols = ("id","patient","doctor","date","time","reason","status")
        heads = ("ID","Patient","Doctor","Date","Time","Reason","Status")
        widths = (70,130,130,90,60,150,90)
        self.table = DataTable(self, cols, heads, widths)
        self.table.pack(fill="both", expand=True, padx=16, pady=8)
        self._load()

    def _get_patient_ids(self):
        rows = Database().fetchall("SELECT id, name FROM patients")
        return [f"{r[0]} - {r[1]}" for r in rows] or ["No patients"]

    def _get_doctor_ids(self):
        rows = Database().fetchall("SELECT id, name FROM doctors")
        return [f"{r[0]} - {r[1]}" for r in rows] or ["No doctors"]

    def _book(self):
        pat_raw = self.f_pat.get()
        doc_raw = self.f_doc.get()
        date    = self.f_date.get()
        time    = self.f_time.get()
        reason  = self.f_reason.get()
        if not all([pat_raw, doc_raw, date, time]):
            messagebox.showwarning("Missing", "All fields except Reason are required.")
            return
        pid = pat_raw.split(" - ")[0]
        did = doc_raw.split(" - ")[0]
        a = Appointment(pid, did, date, time, reason)
        a.save()
        self.f_date.clear(); self.f_time.clear(); self.f_reason.clear()
        self._load()
        messagebox.showinfo("Booked", f"Appointment booked (ID: {a.id})")

    def _complete(self):
        v = self.table.selected_values()
        if not v:
            messagebox.showwarning("Select", "Select an appointment first.")
            return
        Appointment.update_status(v[0], "Completed")
        self._load()

    def _cancel(self):
        v = self.table.selected_values()
        if not v:
            messagebox.showwarning("Select", "Select an appointment first.")
            return
        if messagebox.askyesno("Confirm", "Cancel this appointment?"):
            Appointment.update_status(v[0], "Cancelled")
            self._load()

    def _load(self):
        rows = Appointment.get_all()
        tag_map = {"Scheduled":"Scheduled","Completed":"Completed","Cancelled":"Cancelled"}
        self.table.load(rows, tag_col=6, tag_map=tag_map)


class BillingPanel(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=COLORS["bg"])
        self._build()

    def _build(self):
        hdr = tk.Frame(self, bg=COLORS["header_bg"], pady=12)
        hdr.pack(fill="x")
        tk.Label(hdr, text="💰  Billing", font=FONTS["title"],
                 bg=COLORS["header_bg"], fg="white").pack(side="left", padx=20)

        card = tk.Frame(self, bg=COLORS["white"], padx=10, pady=10,
                        highlightbackground=COLORS["border"], highlightthickness=1)
        card.pack(fill="x", padx=16, pady=(12,6))
        tk.Label(card, text="Generate Bill", font=FONTS["head"],
                 bg=COLORS["white"], fg=COLORS["text"]).grid(
            row=0, column=0, columnspan=4, sticky="w", padx=10, pady=(4,8))

        self.f_pat  = FormField(card, "Patient", 1, 0, values=self._get_patients())
        self.f_amt  = FormField(card, "Amount (₹)", 1, 1, width=16)
        self.f_desc = FormField(card, "Description", 2, 0)

        btn_row = tk.Frame(card, bg=COLORS["white"])
        btn_row.grid(row=3, column=0, columnspan=4, pady=8, sticky="w", padx=10)
        StyledButton(btn_row, "Generate Bill", self._generate).pack(side="left", padx=(0,8))
        StyledButton(btn_row, "Mark as Paid", self._paid,
                     color=COLORS["accent2"]).pack(side="left")

        # Summary label
        self.summary_var = tk.StringVar(value="")
        tk.Label(self, textvariable=self.summary_var, font=FONTS["body"],
                 bg=COLORS["bg"], fg=COLORS["accent"]).pack(pady=(2,0))

        cols = ("id","patient","amount","description","status","date")
        heads = ("Bill ID","Patient","Amount (₹)","Description","Status","Date")
        widths = (70,150,80,200,80,130)
        self.table = DataTable(self, cols, heads, widths)
        self.table.pack(fill="both", expand=True, padx=16, pady=8)
        self._load()

    def _get_patients(self):
        rows = Database().fetchall("SELECT id, name FROM patients")
        return [f"{r[0]} - {r[1]}" for r in rows] or ["No patients"]

    def _generate(self):
        pat_raw = self.f_pat.get()
        amt     = self.f_amt.get()
        desc    = self.f_desc.get()
        if not pat_raw or not amt:
            messagebox.showwarning("Missing", "Patient and Amount are required.")
            return
        try:
            amt = float(amt)
        except ValueError:
            messagebox.showerror("Invalid", "Amount must be a number.")
            return
        pid = pat_raw.split(" - ")[0]
        b = Bill(pid, None, amt, desc)
        b.save()
        self.f_amt.clear(); self.f_desc.clear()
        self._load()
        messagebox.showinfo("Billed", f"Bill generated (ID: {b.id}) — ₹{amt:.2f}")

    def _paid(self):
        v = self.table.selected_values()
        if not v:
            messagebox.showwarning("Select", "Select a bill first.")
            return
        Bill.mark_paid(v[0])
        self._load()

    def _load(self):
        rows = Bill.get_all()
        self.table.load(rows, tag_col=4, tag_map={"Paid":"Paid","Pending":"Pending"})
        total = sum(r[2] for r in rows)
        paid  = sum(r[2] for r in rows if r[4] == "Paid")
        self.summary_var.set(f"Total Billed: ₹{total:.2f}   |   Collected: ₹{paid:.2f}   |   Pending: ₹{total-paid:.2f}")


class DashboardPanel(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=COLORS["bg"])
        self._build()

    def _build(self):
        hdr = tk.Frame(self, bg=COLORS["header_bg"], pady=14)
        hdr.pack(fill="x")
        tk.Label(hdr, text="🏥  MediCore Hospital Management System",
                 font=FONTS["title"], bg=COLORS["header_bg"], fg="white").pack(side="left", padx=20)
        now = datetime.now().strftime("%d %b %Y, %H:%M")
        tk.Label(hdr, text=now, font=FONTS["small"],
                 bg=COLORS["header_bg"], fg="#93C5FD").pack(side="right", padx=20)

        tk.Label(self, text="Dashboard Overview", font=FONTS["head"],
                 bg=COLORS["bg"], fg=COLORS["text"]).pack(anchor="w", padx=20, pady=(16,8))

        cards_frame = tk.Frame(self, bg=COLORS["bg"])
        cards_frame.pack(fill="x", padx=16)
        self._stat_card(cards_frame, "Total Patients", self._count("patients"), "#2563EB", 0)
        self._stat_card(cards_frame, "Total Doctors",  self._count("doctors"),  "#059669", 1)
        self._stat_card(cards_frame, "Appointments",   self._count("appointments"), "#D97706", 2)
        self._stat_card(cards_frame, "Pending Bills",  self._pending_bills(), "#DC2626", 3)

        # Recent patients
        tk.Label(self, text="Recent Patients", font=FONTS["head"],
                 bg=COLORS["bg"], fg=COLORS["text"]).pack(anchor="w", padx=20, pady=(18,6))
        cols = ("id","name","age","gender","phone","blood","address","joined")
        heads = ("ID","Name","Age","Gender","Phone","Blood","Address","Joined")
        widths = (70,150,50,70,100,60,160,120)
        self.table = DataTable(self, cols, heads, widths)
        self.table.pack(fill="both", expand=True, padx=16, pady=(0,12))
        rows = Database().fetchall("SELECT * FROM patients ORDER BY created_at DESC LIMIT 10")
        self.table.load(rows)

    def _stat_card(self, parent, label, value, color, col):
        card = tk.Frame(parent, bg=color, padx=20, pady=16, cursor="arrow")
        card.grid(row=0, column=col, padx=8, pady=4, sticky="ew")
        parent.columnconfigure(col, weight=1)
        tk.Label(card, text=str(value), font=("Segoe UI", 28, "bold"),
                 bg=color, fg="white").pack()
        tk.Label(card, text=label, font=FONTS["small"],
                 bg=color, fg="#E0F2FE").pack()

    def _count(self, table):
        r = Database().fetchone(f"SELECT COUNT(*) FROM {table}")
        return r[0] if r else 0

    def _pending_bills(self):
        r = Database().fetchone("SELECT COUNT(*) FROM bills WHERE status='Pending'")
        return r[0] if r else 0


# ─────────────────────────────────────────────
# MAIN APPLICATION
# ─────────────────────────────────────────────

class HospitalApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("MediCore — Hospital Management System")
        self.geometry("1100x720")
        self.minsize(900, 600)
        self.configure(bg=COLORS["bg"])
        Database()  # initialise DB
        self._build_layout()
        self._show("Dashboard")

    def _build_layout(self):
        # Sidebar
        self.sidebar = tk.Frame(self, bg=COLORS["sidebar"], width=200)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        # Logo
        tk.Label(self.sidebar, text="🏥", font=("Segoe UI", 28),
                 bg=COLORS["sidebar"], fg="white").pack(pady=(22,2))
        tk.Label(self.sidebar, text="MediCore", font=("Segoe UI", 14, "bold"),
                 bg=COLORS["sidebar"], fg="white").pack()
        tk.Label(self.sidebar, text="Hospital System", font=FONTS["small"],
                 bg=COLORS["sidebar"], fg="#93C5FD").pack(pady=(0,20))

        ttk.Separator(self.sidebar, orient="horizontal").pack(fill="x", padx=16, pady=4)

        # Nav buttons
        self.nav_buttons = {}
        nav_items = [
            ("Dashboard", "🏠"),
            ("Patients",  "👥"),
            ("Doctors",   "👨‍⚕️"),
            ("Appointments", "📅"),
            ("Billing",   "💰"),
        ]
        for name, icon in nav_items:
            btn = tk.Button(
                self.sidebar,
                text=f"  {icon}  {name}",
                font=FONTS["sidebar"],
                bg=COLORS["sidebar"], fg="white",
                activebackground=COLORS["sidebar_h"],
                activeforeground="white",
                relief="flat", anchor="w",
                cursor="hand2", padx=10, pady=10,
                command=lambda n=name: self._show(n)
            )
            btn.pack(fill="x", padx=8, pady=2)
            btn.bind("<Enter>", lambda e, b=btn: b.config(bg=COLORS["sidebar_h"]))
            btn.bind("<Leave>", lambda e, b=btn, n=name: b.config(
                bg=COLORS["accent"] if self._active == n else COLORS["sidebar"]))
            self.nav_buttons[name] = btn

        # Version
        tk.Label(self.sidebar, text="v1.0 · MediCore",
                 font=("Segoe UI", 8), bg=COLORS["sidebar"], fg="#475569").pack(
            side="bottom", pady=10)

        # Content area
        self.content = tk.Frame(self, bg=COLORS["bg"])
        self.content.pack(side="left", fill="both", expand=True)

        self._panels = {}
        self._active = ""

    def _show(self, name):
        self._active = name
        # Update sidebar highlight
        for n, btn in self.nav_buttons.items():
            btn.config(bg=COLORS["accent"] if n == name else COLORS["sidebar"])

        # Clear content
        for w in self.content.winfo_children():
            w.destroy()

        # Lazy-load panels
        panel_map = {
            "Dashboard":    DashboardPanel,
            "Patients":     PatientPanel,
            "Doctors":      DoctorPanel,
            "Appointments": AppointmentPanel,
            "Billing":      BillingPanel,
        }
        panel = panel_map[name](self.content)
        panel.pack(fill="both", expand=True)


# ─────────────────────────────────────────────
# ENTRY POINT
# ─────────────────────────────────────────────

if __name__ == "__main__":
    app = HospitalApp()
    app.mainloop()
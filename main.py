# Final Year Project: GUI for Machine Learning Curriculum Enhancement System
# Author: ChatGPT (OpenAI) | Collaborating with the user

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import sqlite3
from PIL import Image, ImageTk
import os
import random
import pandas as pd
from tkinter import filedialog, messagebox
import tempfile
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import joblib




# Load model and label encoder
model = joblib.load("admission_model.pkl")
label_encoder = joblib.load("label_encoder.pkl")

# Ensure consistent connection to the correct database
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "students.db")
conn = sqlite3.connect(db_path)






# --- Constants ---
SCREEN_WIDTH = 1400
SCREEN_HEIGHT = 1050
BG_COLOR = "#8080FF"  # Milk color
FONT_HEADER = ("Helvetica", 18, "bold")
FONT_NORMAL = ("Helvetica", 12)
DB_NAME = "students.db"
FONT_MEDIUM = ("Segoe UI", 16, "bold")
FONT_HEADER = ("Segoe UI", 24, "bold")   # For "Faculty of Applied Science" and "Admin Dashboard"
FONT_NORMAL = ("Segoe UI", 12)           # For regular labels and entries
BUTTON_FONT = ("Segoe UI", 14, "bold")
FONT_HEADER = ("Segoe UI", 24, "bold")     # Big titles
FONT_MEDIUM = ("Segoe UI", 16, "bold")     # Section headers like "Welcome..."
FONT_NORMAL = ("Segoe UI", 12)             # Labels/entries
BUTTON_FONT = ("Segoe UI", 14, "bold")


# ✅ Step 1: Load data
df = pd.read_csv("sample_student_data.csv")  # Make sure this file exists in the same folder

# ✅ Step 2: Convert O'Level grades to numeric
grade_map = {
    "A1": 8, "B2": 7, "B3": 6,
    "C4": 5, "C5": 4, "C6": 3,
    "D7": 2, "E8": 1, "F9": 0
}
subjects = ['English', 'Maths', 'Physics', 'Chemistry', 'Biology', 'Agric']
for subject in subjects:
    df[subject] = df[subject].map(grade_map)

# ✅ Step 3: Encode the Predicted Course column
le = LabelEncoder()
df['Preferred Course'] = df['Preferred Course'].astype(str)  # Ensure no NaNs
df['Preferred Course Encoded'] = le.fit_transform(df['Preferred Course'])


# ✅ Step 4: Define features (X) and target (y)
X = df[['UTME Score', 'Post-UTME Score', 'English', 'Maths', 'Physics', 'Chemistry', 'Biology', 'Agric']]
y = df['Preferred Course Encoded']

# ✅ Step 5: Train the model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X, y)

# ✅ Step 6: Save model and label encoder
joblib.dump(model, "admission_model.pkl")
joblib.dump(le, "label_encoder.pkl")

print("✅ Model trained and saved as 'admission_model.pkl' and 'label_encoder.pkl'")
# --- Database Setup ---
def initialize_db():
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()

    # Create students table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            reg_no TEXT PRIMARY KEY,
            surname TEXT,
            othernames TEXT,
            sex TEXT,
            dob TEXT,
            nationality TEXT,
            session TEXT,
            reg_date TEXT,
            year TEXT,
            photo_path TEXT
        )
    ''')

    # --- DROP old olevel_results table (Dev only) ---


    # Create olevel_results table with correct columns
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS olevel_results (
            reg_no TEXT PRIMARY KEY,
            subject1 TEXT, grade1 TEXT,
            subject2 TEXT, grade2 TEXT,
            subject3 TEXT, grade3 TEXT,
            subject4 TEXT, grade4 TEXT,
            subject5 TEXT, grade5 TEXT,
            subject6 TEXT, grade6 TEXT,
            subject7 TEXT, grade7 TEXT,
            subject8 TEXT, grade8 TEXT,
            subject9 TEXT, grade9 TEXT,
            FOREIGN KEY(reg_no) REFERENCES students(reg_no)
        )
    ''')

    conn.commit()
    conn.close()

# --- Login Screen ---
class LoginScreen:
    def __init__(self, root):
        self.root = root
        self.root.title("Admin Login")
        self.root.geometry(f"{SCREEN_WIDTH}x{SCREEN_HEIGHT}")
        self.root.configure(bg="#8080FF")  # Page background

        # ====== Title/Header ======
        title_frame = tk.Frame(self.root, bg="#0269FE", pady=10)
        title_frame.pack(fill="x", pady=30)
        title_label = tk.Label(
            title_frame,
            text="MACHINE LEARNING FOR CURRICULUM ENHANCEMENT\n(A Python-Based Analysis of Student Data For Improved Learning and Admission Outcomes)",
            font=("Helvetica", 18, "bold"),
            bg="#0269FE",
            fg="#F3DCC3",
            justify="center"
        )
        title_label.pack()

        # ====== Content Frame ======
        content_frame = tk.Frame(self.root, bg="#8080FF", padx=40, pady=20)
        content_frame.pack(fill="both", expand=True)

        # ====== Left: Login Frame ======
        login_frame = tk.Frame(content_frame, bg="#000040", bd=2, relief="groove", highlightbackground="#CDCBE3", highlightthickness=2)
        login_frame.place(relx=0.02, rely=0.05, relwidth=0.35, relheight=0.8)

        tk.Label(login_frame, text="ADMIN LOGIN", font=("Helvetica", 14, "bold"), bg="#000040", fg="#008C01").pack(pady=20)

        tk.Label(login_frame, text="Username", font=("Helvetica", 12), bg="#000040", fg="#008C01").pack(pady=(10, 0))
        self.username_entry = tk.Entry(login_frame, font=("Helvetica", 12))
        self.username_entry.pack(pady=5)

        tk.Label(login_frame, text="Password", font=("Helvetica", 12), bg="#000040", fg="#008C01").pack(pady=(10, 0))
        self.password_entry = tk.Entry(login_frame, show="*", font=("Helvetica", 12))
        self.password_entry.pack(pady=5)

        tk.Button(login_frame, text="Login", font=("Helvetica", 12), bg="#008C01", fg="white", command=self.login).pack(pady=20)

        # ====== Right: Developer Info Frame ======
        right_frame = tk.Frame(content_frame, bg="#8080FF")
        right_frame.place(relx=0.4, rely=0.05, relwidth=0.58, relheight=0.8)

        info = [
            ("Developed By: ", "EMMANUEL SUNDAY A.", "#C0C0FF", "#2121CB"),
            ("Matric No: ", "FTP/CSC/24/0094922", "#C0C0FF", "#E8485F"),
            ("Supervised By: ", "DR. RUFAI M. M.", "#C0C0FF", "#2323C7"),
            ("COMPUTER SCIENCE DEPARTMENT", "", "#000000", "#F9F9FA"),
            ("PROJECT 2025", "", "#400000", "#D6A6C8")
        ]

        for i, (label, value, bg, fg) in enumerate(info):
            container = tk.Frame(right_frame, bg=bg)
            container.pack(fill="x", pady=5, padx=20)
            text = label + value
            tk.Label(
                container,
                text=text,
                font=("Helvetica", 15, "bold"),
                bg=bg,
                fg=fg
            ).pack(anchor="w", padx=10, pady=4)

            if i in [1, 4]:  # breaklines after Matric No and Department
                tk.Frame(right_frame, bg="#4F4FE7", height=2).pack(fill="x", pady=6, padx=20)

    def login(self):
        user = self.username_entry.get()
        pwd = self.password_entry.get()
        if user == "admin" and pwd == "admin123":
            self.root.destroy()
            app = tk.Tk()
            MainApp(app)
            app.mainloop()
        else:
            messagebox.showerror("Login Failed", "Invalid credentials")

# --- Main Application ---
class MainApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Curriculum Enhancement System - Admin Portal")
        self.root.geometry(f"{SCREEN_WIDTH}x{SCREEN_HEIGHT}")
        self.root.configure(bg=BG_COLOR)

        # --- Menu Bar ---
        menubar = tk.Menu(root)

        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Student Registration", command=self.student_registration)
        filemenu.add_command(label="Registered Candidates", command=self.registered_candidates)
        filemenu.add_command(label="O'Level Subject Portal", command=self.olevel_subject_portal)
        filemenu.add_command(label="UTME/POST-UTME Scores Portal", command=self.open_utme_portal)
        filemenu.add_command(label="Prediction Portal", command=self.prediction_portal)
        filemenu.add_command(label="Candidate Courses Portal", command=self.view_candidate_courses)

        menubar.add_cascade(label="Shortcuts", menu=filemenu)


        root.config(menu=menubar)

        # --- Dashboard Heading ---
        heading_frame = tk.Frame(root, bg=BG_COLOR)
        heading_frame.pack(pady=60)

        tk.Label(
            heading_frame,
            text="FACULTY OF APPLIED SCIENCE",
            font=FONT_HEADER,
            bg=BG_COLOR,
            fg="#FFFFFF"
        ).pack()

        tk.Label(
            heading_frame,
            text="ADMIN DASHBOARD",
            font=FONT_HEADER,
            bg=BG_COLOR,
            fg="#FFFFFF"
        ).pack()

        tk.Label(
            root,
            text="Welcome, what will you like to do?",
            font=FONT_MEDIUM,
            bg=BG_COLOR,
            fg="#F3DCC3"
        ).pack(pady=20)

        # --- Buttons ---
        btn_frame = tk.Frame(root, bg=BG_COLOR)
        btn_frame.pack(pady=30)

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TButton",
                        font=BUTTON_FONT,
                        padding=(30, 20),
                        borderwidth=0,
                        background="#0269FE",
                        foreground="#FFFFFF")
        style.map("TButton",
                  background=[("active", "#0047A0")],
                  relief=[("pressed", "flat")])

        ttk.Button(btn_frame, text="Fresh Applicant Registration", command=self.student_registration)\
            .grid(row=0, column=0, padx=70, pady=30)

        ttk.Button(btn_frame, text="View Registered Candidates", command=self.registered_candidates)\
            .grid(row=0, column=1, padx=70, pady=30)

        ttk.Button(btn_frame, text="Course Prediction / Admission Portal", command=self.prediction_portal)\
            .grid(row=1, column=0, padx=70, pady=30)

        ttk.Button(btn_frame, text="Admitted Candidates Portal", command=self.admitted_candidates_portal) \
            .grid(row=1, column=1, padx=70, pady=30)

        # --- Styled Logout Button at Top-Right ---
        style.configure("Logout.TButton", font=("Helvetica", 9), padding=(5, 2),
                        background="#F3E5AB", foreground="#000000")
        style.map("Logout.TButton",
                  background=[("active", "#E0D3A4")])

        logout_btn = ttk.Button(self.root, text="🔒 Logout", command=self.logout, style="Logout.TButton")
        logout_btn.place(relx=0.98, rely=0.02, anchor="ne")  # Positioned top-right

    # Grade map
    grade_map = {
        "A1": 8, "B2": 7, "B3": 6,
        "C4": 5, "C5": 4, "C6": 3,
        "D7": 2, "E8": 1, "F9": 0
    }

    def full_student_registration(self):
        import sqlite3

        biodata = {label: entry.get().strip() for label, entry in self.reg_entries.items()}
        biodata["Photo"] = self.photo_path.get()

        if not biodata["Registration Number"]:
            messagebox.showerror("Missing Data", "Registration Number is required.")
            return

        try:
            conn = sqlite3.connect("students.db")
            cursor = conn.cursor()
            cursor.execute('''
                INSERT OR REPLACE INTO students (
                    reg_no, surname, othernames, sex, preferred_course,
                    dob, nationality, session, reg_date, year, photo_path
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                biodata['Registration Number'], biodata['Surname'], biodata['Other Names'], biodata['Sex'],
                biodata['Preferred Course of Study'], biodata['Date of Birth'], biodata['Nationality'],
                biodata['Session'], biodata['Date of Registration'], biodata['Year'], biodata['Photo']
            ))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Student bio data saved successfully.")
            self.clear_entries()
        except Exception as e:
            messagebox.showerror("Database Error", str(e))

    def predict_course(candidate_data):
        try:
            # Extract and transform grades and scores
            X_input = [[
                grade_map.get(candidate_data['English'], 0),
                grade_map.get(candidate_data['Maths'], 0),
                grade_map.get(candidate_data['Physics'], 0),
                grade_map.get(candidate_data['Chemistry'], 0),
                grade_map.get(candidate_data['Biology'], 0),
                grade_map.get(candidate_data['Agric'], 0),
                int(candidate_data['UTME']),
                float(candidate_data['Post_UTME'])
            ]]

            prediction = model.predict(X_input)[0]
            predicted_course = label_encoder.inverse_transform([prediction])[0]

            # Admission Rule Logic
            utme_score = int(candidate_data['UTME'])
            post_utme_score = float(candidate_data['Post_UTME'])
            if utme_score > 200 and post_utme_score > 60:
                admission_status = "Admitted"
            else:
                admission_status = "Not Admitted"

            return predicted_course, admission_status

        except Exception as e:
            print("Prediction error:", e)
            return None, "Not Admitted"

    def logout(self):
        self.root.destroy()
        root = tk.Tk()
        LoginScreen(root)
        root.mainloop()

    def admitted_candidates_portal(self):
        win = tk.Toplevel(self.root)
        win.title("Admitted Candidates Portal")
        win.geometry(f"{SCREEN_WIDTH}x{SCREEN_HEIGHT}")
        win.configure(bg=BG_COLOR)

        tk.Label(win, text="Admitted Candidates", font=FONT_HEADER, bg=BG_COLOR).pack(pady=20)

        # Treeview
        columns = ("sn", "reg_no", "name", "admitted_department")
        tree = ttk.Treeview(win, columns=columns, show="headings")
        tree.heading("sn", text="S/N")
        tree.heading("reg_no", text="Registration Number")
        tree.heading("name", text="Name")
        tree.heading("admitted_department", text="Admitted Department")
        tree.column("sn", width=50, anchor="center")

        tree.pack(pady=10, fill="both", expand=True)

        # Load data
        conn = sqlite3.connect("students.db")
        cursor = conn.cursor()
        cursor.execute("SELECT reg_no, name, admitted_department FROM predictions")
        data = cursor.fetchall()
        conn.close()

        for idx, row in enumerate(data, start=1):
            tree.insert("", "end", values=(idx, *row))

        # Filter
        filter_frame = tk.Frame(win, bg=BG_COLOR)
        filter_frame.pack(pady=10)

        tk.Label(filter_frame, text="Filter by Department:", font=FONT_NORMAL, bg=BG_COLOR).pack(side="left", padx=10)

        departments = [
            "Computer Science", "Physics", "Industrial Chemistry", "Microbiology",
            "Animal and Environmental Biology", "Biochemistry",
            "Plant Science and Biotechnology", "Applied Physics", "Mathematics and Statistics"
        ]
        selected_dept = tk.StringVar()
        dept_combo = ttk.Combobox(filter_frame, textvariable=selected_dept, values=departments, state="readonly")
        dept_combo.pack(side="left", padx=5)

        # Apply Filter Button (smaller size)
        style = ttk.Style()
        style.configure("Small.TButton", font=("Helvetica", 9), padding=(6, 4))

        def filter_data():
            tree.delete(*tree.get_children())
            conn = sqlite3.connect("students.db")
            cursor = conn.cursor()
            cursor.execute("SELECT reg_no, name, admitted_department FROM predictions WHERE admitted_department = ?",
                           (selected_dept.get(),))
            filtered = cursor.fetchall()
            conn.close()
            for idx, row in enumerate(filtered, start=1):
                tree.insert("", "end", values=(idx, *row))

        ttk.Button(filter_frame, text="Apply Filter", command=filter_data, style="Small.TButton") \
            .pack(side="left", pady=0, padx=10)

        # Action Buttons (Import / Export)
        def import_data():
            filename = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
            if filename:
                with open(filename, newline='') as f:
                    reader = csv.reader(f)
                    next(reader)  # skip header
                    conn = sqlite3.connect("students.db")
                    cursor = conn.cursor()
                    for row in reader:
                        cursor.execute(
                            "INSERT OR REPLACE INTO predictions (reg_no, name, admitted_department) VALUES (?, ?, ?)",
                            row)
                    conn.commit()
                    conn.close()
                    messagebox.showinfo("Import", "Data imported successfully!")
                    self.admitted_candidates_portal()  # Refresh

        def export_csv():
            filename = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
            if filename:
                with open(filename, mode='w', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow(["Registration Number", "Name", "Admitted Department"])
                    for item in tree.get_children():
                        values = tree.item(item)["values"][1:]  # skip S/N
                        writer.writerow(values)
                messagebox.showinfo("Export", "Data exported to CSV successfully!")

            # Define this once (e.g., at the top of your UI setup or just before creating the buttons)

        style = ttk.Style()
        style.configure("Small.TButton", font=("Helvetica", 9), padding=(6, 4))  # smaller font, less padding

        def export_pdf():
            filename = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
            if filename:
                from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
                from reportlab.lib.pagesizes import letter
                from reportlab.lib import colors

                pdf = SimpleDocTemplate(filename, pagesize=letter)
                data = [["Registration Number", "Name", "Admitted Department"]]
                for item in tree.get_children():
                    values = tree.item(item)["values"][1:]  # skip S/N
                    data.append(values)

                table = Table(data)
                table.setStyle(TableStyle([
                    ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                    ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                    ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
                    ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
                ]))
                pdf.build([table])
                messagebox.showinfo("Export", "Data exported to PDF successfully!")

        # Now define and place the action_frame properly
        action_frame = tk.Frame(win, bg=BG_COLOR)
        action_frame.pack(pady=10)

        ttk.Button(action_frame, text="Import CSV", command=import_data, style="Small.TButton") \
            .grid(row=0, column=0, padx=5)
        ttk.Button(action_frame, text="Export CSV", command=export_csv, style="Small.TButton") \
            .grid(row=0, column=1, padx=5)
        ttk.Button(action_frame, text="Export PDF", command=export_pdf, style="Small.TButton") \
            .grid(row=0, column=2, padx=5)
        ttk.Button(action_frame, text="Exit", command=win.destroy, style="Small.TButton") \
            .grid(row=0, column=3, padx=5)

    def save_changes(self):
        selected = self.tree.focus()
        if not selected or not hasattr(self, 'editing_cells'):
            return

        # Get original values and reg_no
        original_values = self.tree.item(selected)['values']
        reg_no = original_values[0]  # Keep reg_no fixed

        # Build new values in order of columns
        edited_entries = {col: entry.get() for col, entry in self.editing_cells}
        new_values = []
        for col in self.tree['columns']:
            if col == "reg_no":
                new_values.append(reg_no)
            else:
                # Use edited value or fallback to current value in Treeview
                new_values.append(edited_entries.get(col, self.tree.set(selected, col)))

        print("DEBUG: reg_no to update:", reg_no)
        print("DEBUG: New values:", new_values)

        # Update Treeview row
        self.tree.item(selected, values=new_values)

        # Update database
        conn = sqlite3.connect("students.db")
        cursor = conn.cursor()
        try:
            cursor.execute("""
                UPDATE students SET
                    surname=?, othernames=?, sex=?, dob=?,
                    nationality=?, session=?, reg_date=?, year=?
                WHERE reg_no=?
            """, new_values[1:] + [reg_no])  # reg_no goes last in WHERE clause

            conn.commit()
            print("DEBUG: Database updated successfully")

        except Exception as e:
            messagebox.showerror("Database Error", f"Could not update record: {e}")
            print("DEBUG: Exception:", e)

        finally:
            conn.close()

        # Clean up inline editors
        for _, entry in self.editing_cells:
            entry.destroy()
        self.editing_cells.clear()

        # Disable buttons
        self.save_btn.config(state=tk.DISABLED)
        self.cancel_btn.config(state=tk.DISABLED)
        self.edit_btn.config(state=tk.NORMAL)
        self.delete_btn.config(state=tk.DISABLED)

    def save_inline_editing(self):
        selected = self.tree.focus()
        if not selected:
            return

        values = list(self.tree.item(selected)['values'])
        for i, (col, entry) in enumerate(self.editing_cells, start=1):
            values[i] = entry.get()
            entry.destroy()

        self.tree.item(selected, values=values)
        self.editing_cells = []

        self.save_btn.config(state=tk.DISABLED)
        self.cancel_btn.config(state=tk.DISABLED)
        self.edit_btn.config(state=tk.NORMAL)

        # Optional: Save to database here

        conn = sqlite3.connect("students.db")
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE students SET 
                surname=?, othernames=?, sex=?, dob=?, nationality=?, session=?, reg_date=?, year=?
            WHERE reg_no=?""",
                       values[1:] + [values[0]])
        conn.commit()
        conn.close()

    def cancel_inline_editing(self):
        for _, entry in self.editing_cells:
            entry.destroy()
        self.editing_cells = []

        self.save_btn.config(state=tk.DISABLED)
        self.cancel_btn.config(state=tk.DISABLED)
        self.edit_btn.config(state=tk.NORMAL)

    def delete_candidate(self):
        selected = self.tree.focus()
        if not selected:
            return
        reg_no = self.tree.item(selected)['values'][0]

        # Delete from database
        conn = sqlite3.connect("students.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM students WHERE reg_no=?", (reg_no,))
        conn.commit()
        conn.close()

        # Remove from Treeview
        self.tree.delete(selected)

        self.edit_btn.config(state=tk.DISABLED)
        self.delete_btn.config(state=tk.DISABLED)

    def open_utme_portal(self):
        win = tk.Toplevel(self.root)
        win.title("UTME / POST-UTME Scores Portal")
        win.geometry(f"{SCREEN_WIDTH}x{SCREEN_HEIGHT}")
        win.configure(bg=BG_COLOR)

        tk.Label(win, text="Enter UTME and POST-UTME Scores", font=FONT_HEADER, bg=BG_COLOR).pack(pady=20)

        form_frame = tk.Frame(win, bg=BG_COLOR)
        form_frame.pack(pady=10)

        # Select student
        tk.Label(form_frame, text="Registration Number:", font=FONT_NORMAL, bg=BG_COLOR).grid(row=0, column=0,
                                                                                              sticky='e', padx=10,
                                                                                              pady=10)
        conn = sqlite3.connect("students.db")
        cursor = conn.cursor()
        cursor.execute("SELECT reg_no FROM students")
        reg_nos = [row[0] for row in cursor.fetchall()]
        conn.close()

        selected_reg = tk.StringVar()
        reg_combo = ttk.Combobox(form_frame, textvariable=selected_reg, values=reg_nos, font=FONT_NORMAL,
                                 state="readonly")
        reg_combo.grid(row=0, column=1, padx=10, pady=10)

        # UTME subjects and scores
        utme_subjects = []
        utme_scores = []
        for i in range(4):
            tk.Label(form_frame, text=f"UTME Subject {i + 1}:", font=FONT_NORMAL, bg=BG_COLOR).grid(row=i + 1, column=0,
                                                                                                    sticky='e', padx=10,
                                                                                                    pady=5)
            subj = tk.Entry(form_frame, font=FONT_NORMAL)
            subj.grid(row=i + 1, column=1, padx=10, pady=5)
            utme_subjects.append(subj)

            tk.Label(form_frame, text=f"Score {i + 1}:", font=FONT_NORMAL, bg=BG_COLOR).grid(row=i + 1, column=2,
                                                                                             sticky='e', padx=10,
                                                                                             pady=5)
            score = tk.Entry(form_frame, font=FONT_NORMAL)
            score.grid(row=i + 1, column=3, padx=10, pady=5)
            utme_scores.append(score)

        # POST UTME
        tk.Label(form_frame, text="POST-UTME Score:", font=FONT_NORMAL, bg=BG_COLOR).grid(row=6, column=0, sticky='e',
                                                                                          padx=10, pady=10)
        postutme_score = tk.Entry(form_frame, font=FONT_NORMAL)
        postutme_score.grid(row=6, column=1, padx=10, pady=10)

        # Total UTME Score
        tk.Label(form_frame, text="Total UTME Score:", font=FONT_NORMAL, bg=BG_COLOR).grid(row=5, column=0, sticky='e',
                                                                                           padx=10, pady=10)

        total_score_var = tk.StringVar()
        total_score_entry = tk.Entry(form_frame, textvariable=total_score_var, font=FONT_NORMAL, state='readonly')
        total_score_entry.grid(row=5, column=1, padx=10, pady=10)


        # Function to update total score
        def update_total_score(event=None):
            total = 0
            for entry in utme_scores:
                try:
                    val = int(entry.get())
                    total += val
                except ValueError:
                    continue
            total_score_var.set(str(total))

        # Bind each UTME score entry to update total on key release
        for score_entry in utme_scores:
            score_entry.bind("<KeyRelease>", update_total_score)

        def save_scores():
            reg = selected_reg.get()
            if not reg:
                messagebox.showerror("Error", "Please select a student.")
                return

            try:
                utme_data = [(subj.get(), int(score.get())) for subj, score in zip(utme_subjects, utme_scores)]
                total_score = sum(score for _, score in utme_data)
                post_score = int(postutme_score.get())
            except ValueError:
                messagebox.showerror("Error", "Please ensure all scores are valid numbers.")
                return

            conn = sqlite3.connect("students.db")
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS utme_postutme (
                    reg_no TEXT PRIMARY KEY,
                    subject1 TEXT, score1 INTEGER,
                    subject2 TEXT, score2 INTEGER,
                    subject3 TEXT, score3 INTEGER,
                    subject4 TEXT, score4 INTEGER,
                    total_score INTEGER,
                    post_utme_score INTEGER
                )
            ''')

            # Corrected value list for 11 columns
            values = [reg]
            for subject, score in utme_data:
                values.extend([subject, score])
            values.extend([total_score, post_score])

            cursor.execute('''
                INSERT OR REPLACE INTO utme_postutme (
                    reg_no, subject1, score1, subject2, score2,
                    subject3, score3, subject4, score4, total_score, post_utme_score
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', values)

            conn.commit()
            conn.close()
            messagebox.showinfo("Success", f"UTME and POST-UTME scores saved for {reg}")
            win.destroy()

        button_frame = tk.Frame(win, bg=BG_COLOR)
        button_frame.pack(pady=20)

        tk.Button(button_frame, text="Save Score", font=FONT_NORMAL, command=save_scores) \
            .grid(row=0, column=0, padx=10)

        tk.Button(button_frame, text="Exit", font=FONT_NORMAL, command=win.destroy) \
            .grid(row=1, column=0, padx=10, pady=(10, 0))

    def import_candidate_prediction_data(self):
        from tkinter import filedialog
        import pandas as pd
        import joblib
        import sqlite3

        # Load trained model
        try:
            model = joblib.load("admission_model.pkl")
        except Exception as e:
            messagebox.showerror("Model Error", f"Failed to load prediction model:\n{e}")
            return

        file_path = filedialog.askopenfilename(
            filetypes=[("CSV Files", "*.csv"), ("Excel Files", "*.xlsx")],
            title="Select Candidate Data File"
        )
        if not file_path:
            return

        try:
            if file_path.endswith('.csv'):
                df = pd.read_csv(file_path)
            else:
                df = pd.read_excel(file_path)
        except Exception as e:
            messagebox.showerror("File Error", f"Could not read file:\n{e}")
            return

        required_cols = ['reg_no', 'name', 'preferred_course']
        if not all(col in df.columns for col in required_cols):
            messagebox.showerror("Format Error", "File must contain: reg_no, name, preferred_course")
            return

        conn = sqlite3.connect("students.db")
        cursor = conn.cursor()
        successful = 0

        for _, row in df.iterrows():
            reg_no = row['reg_no']
            name = row['name']
            preferred = row['preferred_course']

            # Fetch UTME/Post-UTME scores
            cursor.execute("SELECT total_score, post_utme_score FROM utme_postutme WHERE reg_no=?", (reg_no,))
            utme_row = cursor.fetchone()
            if not utme_row:
                continue
            total_utme, post_utme = utme_row

            # Fetch O'Level grades
            cursor.execute('''
                SELECT grade1, grade2, grade3, grade4, grade5, grade6, grade7, grade8
                FROM olevel_results WHERE reg_no=?
            ''', (reg_no,))
            olevel_row = cursor.fetchone()
            if not olevel_row:
                continue

            # Convert grades to numbers
            grade_map = {
                "A1": 1, "B2": 2, "B3": 3,
                "C4": 4, "C5": 5, "C6": 6,
                "D7": 7, "E8": 8, "F9": 9
            }
            numeric_grades = [grade_map.get(g.upper(), 9) for g in olevel_row]

            try:
                # Build features
                features_df = pd.DataFrame([{
                    'UTME Score': total_utme,
                    'Post-UTME Score': post_utme,
                    'English': numeric_grades[0],
                    'Maths': numeric_grades[1],
                    'Physics': numeric_grades[2],
                    'Chemistry': numeric_grades[3],
                    'Biology': numeric_grades[4],
                    'Agric': numeric_grades[5]
                }])

                # Predict
                predicted_course_encoded = model.predict(features_df)[0]
                print(f"Predicted value for {reg_no}: {predicted_course_encoded}")

                # Decode course
                course_map = {
                    0: "Computer Science",
                    1: "Microbiology",
                    2: "Biochemistry",
                    3: "Physics",
                    4: "Applied Physics",
                    5: "Industrial Chemistry",
                    6: "Mathematics and Statistics",
                    7: "Animal and Environmental Biology",
                    8: "Plant Science and Biotechnology"
                }
                course_name = course_map.get(predicted_course_encoded, "Unknown")

                # Admission check
                core_subjects = numeric_grades[0:6]
                admission_status = "Admitted" if (
                        total_utme > 200 and post_utme > 60 and all(g <= 6 for g in core_subjects)
                ) else "Not Admitted"

                # Save prediction
                cursor.execute('''
                    INSERT OR REPLACE INTO candidate_courses
                    (reg_no, name, preferred_course, predicted_course, admission_status)
                    VALUES (?, ?, ?, ?, ?)
                ''', (reg_no, name, preferred, course_name, admission_status))

                successful += 1

            except Exception as e:
                print(f"Prediction error for {reg_no}: {e}")
                continue

        conn.commit()
        conn.close()
        self.load_candidate_courses_data()
        messagebox.showinfo("Import Complete", f"{successful} candidates successfully imported and predicted.")

    def registered_candidates(self):
        win = tk.Toplevel(self.root)
        win.title("Registered Candidates")
        win.geometry(f"{SCREEN_WIDTH}x{SCREEN_HEIGHT}")
        win.configure(bg=BG_COLOR)

        frame = tk.Frame(win, bg=BG_COLOR)
        frame.pack(fill="both", expand=True)

        # Define Treeview columns
        columns = ("sn", "reg_no", "surname", "othernames", "sex", "dob", "nationality", "session", "reg_date", "year")
        self.tree = ttk.Treeview(frame, columns=columns, show="headings", height=25)

        for col in columns:
            heading = "S/N" if col == "sn" else col.replace("_", " ").title()
            width = 60 if col == "sn" else 120
            self.tree.heading(col, text=heading)
            self.tree.column(col, anchor='center', width=width)

        self.tree.bind("<<TreeviewSelect>>", self.on_row_select)
        self.tree.grid(row=0, column=0, padx=20, pady=10, sticky="nsew")

        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=0, column=1, sticky="ns")

        # Buttons
        btn_frame = tk.Frame(frame, bg=BG_COLOR)
        btn_frame.grid(row=1, column=0, columnspan=2, pady=10, sticky="w")

        self.edit_btn = tk.Button(btn_frame, text="Edit", command=self.enable_inline_editing)
        self.edit_btn.grid(row=0, column=0, padx=10)

        self.save_btn = tk.Button(btn_frame, text="Save", command=self.save_changes, state=tk.DISABLED)
        self.save_btn.grid(row=0, column=1, padx=10)

        self.cancel_btn = tk.Button(btn_frame, text="Cancel", command=self.cancel_editing, state=tk.DISABLED)
        self.cancel_btn.grid(row=0, column=2, padx=10)

        self.delete_btn = tk.Button(btn_frame, text="Delete", command=self.delete_candidate, state=tk.DISABLED)
        self.delete_btn.grid(row=0, column=3, padx=5)

        import_btn = tk.Button(btn_frame, text="Import File", command=self.import_full_candidate_data)
        import_btn.grid(row=0, column=4, padx=10)

        export_btn = tk.Button(btn_frame, text="Export", command=self.export_treeview_data)
        export_btn.grid(row=0, column=5, padx=5)

        profile_btn = tk.Button(btn_frame, text="View Profile", command=self.show_full_profile)
        profile_btn.grid(row=0, column=6, padx=5)

        go_back_btn = tk.Button(btn_frame, text="Exit", command=win.destroy)
        go_back_btn.grid(row=0, column=7, padx=20)

        # Photo display area
        photo_frame = tk.Frame(frame, bg=BG_COLOR)
        photo_frame.grid(row=0, column=2, padx=30, sticky="n")

        self.photo_label = tk.Label(photo_frame, bg=BG_COLOR)
        self.photo_label.pack(pady=10)

        # Load student data into the Treeview
        self.load_registered_candidates()

    def load_registered_candidates(self):
        conn = sqlite3.connect("students.db")
        cursor = conn.cursor()

        # Adjust this SELECT to fetch only needed DB fields
        cursor.execute("""
            SELECT reg_no, surname, othernames, sex, dob, nationality, session, reg_date, year
            FROM students
        """)
        rows = cursor.fetchall()
        conn.close()

        self.tree.delete(*self.tree.get_children())  # Clear previous rows

        for i, row in enumerate(rows, start=1):
            # Add serial number as first value, then unpack rest of the DB row
            self.tree.insert("", "end", values=(i, *row))
    def on_select(event):
        selected_item = tree.selection()
        if selected_item:
            reg_no = tree.item(selected_item[0])['values'][0]

            conn = sqlite3.connect("students.db")
            cursor = conn.cursor()
            cursor.execute("SELECT photo_path FROM students WHERE reg_no=?", (reg_no,))
            row = cursor.fetchone()
            conn.close()

            if row and os.path.exists(row[0]):
                img = Image.open(row[0])
                img = img.resize((50, 50))
                photo = ImageTk.PhotoImage(img)
                self.photo_label.configure(image=photo)
                self.photo_label.image = photo  # Prevent garbage collection
            else:
                self.photo_label.configure(image='', text="No Photo Found")

    # Bind selection event to Treeview (uncomment this line when tree is defined)
    # tree.bind("<<TreeviewSelect>>", on_select)

    # Load data from DB into the Treeview

    def import_file_data(self):
        file_path = filedialog.askopenfilename(
            title="Select CSV or Excel file",
            filetypes=[("CSV files", "*.csv"), ("Excel files", "*.xlsx *.xls")]
        )
        if not file_path:
            return

        try:
            if file_path.endswith('.csv'):
                df = pd.read_csv(file_path)
            else:
                df = pd.read_excel(file_path)

            required_columns = [
                'reg_no', 'surname', 'othernames', 'sex', 'dob', 'preferred_course',
                'nationality', 'session', 'reg_date', 'year'
            ]

            if not all(col in df.columns for col in required_columns):
                messagebox.showerror("Error", "Missing required columns in file.")
                return

            conn = sqlite3.connect("students.db")
            cursor = conn.cursor()

            # Load model and encoder
            model = joblib.load("admission_model.pkl")
            label_encoder = joblib.load("label_encoder.pkl")

            for _, row in df.iterrows():
                values = tuple(row[col] for col in required_columns)

                # Insert student data
                cursor.execute("""
                    INSERT OR REPLACE INTO students (
                        reg_no, surname, othernames, sex, dob, preferred_course, 
                        nationality, session, reg_date, year
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, values)

                self.tree.insert("", "end", values=values)

                # Fetch scores from another table (adjust column/table names as needed)
                reg_no = row['reg_no']
                cursor.execute("""
                    SELECT utme_score, post_utme_score, English, Maths, Physics,
                           Chemistry, Biology, Agric
                    FROM scores WHERE reg_no = ?
                """, (reg_no,))
                result = cursor.fetchone()
                if not result:
                    continue

                # Map O'Level grades to numeric
                grade_map = {
                    "A1": 8, "B2": 7, "B3": 6,
                    "C4": 5, "C5": 4, "C6": 3,
                    "D7": 2, "E8": 1, "F9": 0
                }

                utme_score, post_utme_score, *grades = result
                numeric_grades = [grade_map.get(g, 0) for g in grades]

                # Prepare model input
                model_input = [[utme_score, post_utme_score] + numeric_grades]

                # Predict
                predicted_class = model.predict(model_input)[0]
                predicted_course = label_encoder.inverse_transform([predicted_class])[0]

                # Rule-based eligibility
                admitted = "Admitted" if utme_score > 200 and post_utme_score > 60 else "Not Admitted"

                # Save prediction
                cursor.execute("""
                    INSERT OR REPLACE INTO admission_results (
                        reg_no, preferred_course, predicted_course, admission_status
                    ) VALUES (?, ?, ?, ?)
                """, (reg_no, row['preferred_course'], predicted_course, admitted))

            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Data imported and predictions made successfully.")

        except Exception as e:
            messagebox.showerror("Import Error", f"Could not import file:\n{e}")

        self.load_candidate_courses_data()

    def predict_admissions(self):
        import pandas as pd
        import sqlite3
        import joblib

        try:
            # Load trained model and encoder
            model = joblib.load("admission_model.pkl")
            label_encoder = joblib.load("label_encoder.pkl")

            # Grade mapping
            grade_map = {
                "A1": 8, "B2": 7, "B3": 6,
                "C4": 5, "C5": 4, "C6": 3,
                "D7": 2, "E8": 1, "F9": 0
            }

            # Connect to DB
            conn = sqlite3.connect("students.db")
            cursor = conn.cursor()

            # Fetch scores table
            cursor.execute("SELECT * FROM scores")
            rows = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]
            df = pd.DataFrame(rows, columns=columns)

            if df.empty:
                messagebox.showwarning("Warning", "No score data found.")
                return

            # Convert O'Level grades to numeric
            subjects = ['English', 'Maths', 'Physics', 'Chemistry', 'Biology', 'Agric']
            for subject in subjects:
                df[subject] = df[subject].map(grade_map)

            # Prepare data for prediction
            X = df[['utme_score', 'post_utme_score'] + subjects].copy()

            # Rename to match model’s training feature names
            X.rename(columns={
                "utme_score": "UTME Score",
                "post_utme_score": "Post-UTME Score"
            }, inplace=True)

            reg_nos = df['reg_no'].tolist()
            predicted_codes = model.predict(X)
            predicted_courses = label_encoder.inverse_transform(predicted_codes)

            # ✅ Course-specific admission check function
            def check_admission(course, utme, putme):
                cutoffs = {
                    "Computer Science": (239, 74),
                    "Biochemistry": (220, 68),
                    "Microbiology": (210, 65),
                    "Plant Science and Biotechnology": (200, 60),
                }
                general_utme = 200
                general_putme = 60

                if utme < general_utme or putme < general_putme:
                    return "Not Admitted"

                required_utme, required_putme = cutoffs.get(course, (200, 60))
                return "Admitted" if utme >= required_utme and putme >= required_putme else "Not Admitted"

            # Save predictions + admission decision
            for i in range(len(df)):
                reg_no = reg_nos[i]
                course = predicted_courses[i]
                utme = df.loc[i, 'utme_score']
                putme = df.loc[i, 'post_utme_score']
                admission_status = check_admission(course, utme, putme)

                # Fetch name and preferred course
                cursor.execute("SELECT surname, othernames, preferred_course FROM students WHERE reg_no = ?", (reg_no,))
                info = cursor.fetchone()
                if info:
                    surname, othernames, preferred_course = info
                    full_name = f"{surname} {othernames}"
                else:
                    full_name = "Unknown"
                    preferred_course = "Unknown"

                # Insert or update candidate course record
                cursor.execute("""
                    INSERT OR REPLACE INTO candidate_courses (
                        reg_no, name, preferred_course, predicted_course, admission_status
                    ) VALUES (?, ?, ?, ?, ?)
                """, (reg_no, full_name, preferred_course, course, admission_status))

            conn.commit()
            conn.close()

            self.load_candidate_courses_data()  # Refresh treeview

        except Exception as e:
            messagebox.showerror("Prediction Error", f"❌ Prediction failed:\n{e}")

    def load_registered_candidates_data(self):
        conn = sqlite3.connect("students.db")
        cursor = conn.cursor()
        cursor.execute(
            "SELECT reg_no, surname, othernames, sex, dob, nationality, session, reg_date, year FROM students")
        rows = cursor.fetchall()
        conn.close()

        # Clear any existing rows in the Treeview
        self.tree.delete(*self.tree.get_children())

        # Insert each row with a serial number
        for idx, row in enumerate(rows, start=1):
            self.tree.insert("", "end", values=(idx, *row))

    def import_full_candidate_data(self):
        from tkinter import filedialog, messagebox
        import pandas as pd
        import sqlite3

        # Ask user to select a file
        file_path = filedialog.askopenfilename(
            filetypes=[("CSV Files", "*.csv")],
            title="Select Full Candidate Data File"
        )
        if not file_path:
            return

        try:
            df = pd.read_csv(file_path)
        except Exception as e:
            messagebox.showerror("File Error", f"Could not read file:\n{e}")
            return

        # Required columns in the CSV
        required_columns = [
            "reg_no", "surname", "othernames", "sex", "dob", "nationality",
            "session", "reg_date", "year", "preferred_course",
            "subject1", "grade1", "subject2", "grade2", "subject3", "grade3",
            "subject4", "grade4", "subject5", "grade5", "subject6", "grade6",
            "subject7", "grade7", "subject8", "grade8", "subject9", "grade9",
            "utme_subject1", "utme_score1", "utme_subject2", "utme_score2",
            "utme_subject3", "utme_score3", "utme_subject4", "utme_score4",
            "total_utme_score", "post_utme_score"
        ]

        if not all(col in df.columns for col in required_columns):
            messagebox.showerror("Format Error", f"CSV file must contain all required columns.")
            return

        conn = sqlite3.connect("students.db")
        cursor = conn.cursor()
        success_count = 0

        for _, row in df.iterrows():
            try:
                # --- Insert into students (biodata) ---
                cursor.execute('''
                    INSERT OR REPLACE INTO students
                    (reg_no, surname, othernames, sex, dob, nationality, session, reg_date, year, preferred_course)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    row["reg_no"], row["surname"], row["othernames"], row["sex"], row["dob"],
                    row["nationality"], row["session"], row["reg_date"], row["year"], row["preferred_course"]
                ))

                # --- Insert into olevel_results ---
                cursor.execute('''
                    INSERT OR REPLACE INTO olevel_results
                    (reg_no, subject1, grade1, subject2, grade2, subject3, grade3, subject4, grade4,
                     subject5, grade5, subject6, grade6, subject7, grade7, subject8, grade8, subject9, grade9)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    row["reg_no"],
                    row["subject1"], row["grade1"], row["subject2"], row["grade2"],
                    row["subject3"], row["grade3"], row["subject4"], row["grade4"],
                    row["subject5"], row["grade5"], row["subject6"], row["grade6"],
                    row["subject7"], row["grade7"], row["subject8"], row["grade8"],
                    row["subject9"], row["grade9"]
                ))

                # --- Insert into utme_postutme ---
                cursor.execute('''
                    INSERT OR REPLACE INTO utme_postutme
                    (reg_no, subject1, score1, subject2, score2, subject3, score3,
                     subject4, score4, total_score, post_utme_score)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    row["reg_no"],
                    row["utme_subject1"], row["utme_score1"],
                    row["utme_subject2"], row["utme_score2"],
                    row["utme_subject3"], row["utme_score3"],
                    row["utme_subject4"], row["utme_score4"],
                    row["total_utme_score"], row["post_utme_score"]
                ))

                # --- Insert into candidate_courses ---
                cursor.execute('''
                    INSERT OR REPLACE INTO candidate_courses
                    (reg_no, name, preferred_course)
                    VALUES (?, ?, ?)
                ''', (
                    row["reg_no"],
                    row["surname"] + " " + row["othernames"],
                    row["preferred_course"]
                ))

                success_count += 1
            except Exception as e:
                print(f"Error importing {row['reg_no']}: {e}")
                continue

        conn.commit()
        conn.close()

        # Reload treeview
        self.load_registered_candidates_data()
        messagebox.showinfo("Import Complete", f"{success_count} candidate records successfully imported.")

    def export_treeview_data(self):
        # Get data from Treeview
        data = []
        headers = self.tree['columns']
        for row_id in self.tree.get_children():
            row = self.tree.item(row_id)['values']
            data.append(row)

        if not data:
            messagebox.showinfo("No Data", "There is no data to export.")
            return

        # Ask user where to save
        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV Files", "*.csv"), ("Excel Files", "*.xlsx")],
            title="Save as"
        )
        if not file_path:
            return  # User cancelled

        try:
            df = pd.DataFrame(data, columns=headers)

            if file_path.endswith('.xlsx'):
                df.to_excel(file_path, index=False)
            else:
                df.to_csv(file_path, index=False)

            messagebox.showinfo("Export Successful", f"Data exported to {file_path}")
        except Exception as e:
            messagebox.showerror("Export Failed", str(e))

    def show_full_profile(self):
        selected = self.tree.focus()
        if not selected:
            return

        # Dynamically get the correct reg_no from the tree based on column name
        columns = self.tree["columns"]
        try:
            reg_index = columns.index("reg_no")
        except ValueError:
            messagebox.showerror("Column Error", "'reg_no' column not found in the Treeview.")
            return

        reg_no = str(self.tree.item(selected)['values'][reg_index]).strip().upper()


        # Correct DB path
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(BASE_DIR, "students.db")
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        profile_win = tk.Toplevel(self.root)
        profile_win.title(f"Candidate Profile: {reg_no}")
        profile_win.geometry("800x600")
        profile_win.configure(bg=BG_COLOR)

        # ========== Bio Data ==========
        bio_frame = tk.LabelFrame(profile_win, text="Bio Data", bg=BG_COLOR, padx=10, pady=10)
        bio_frame.pack(fill="x", padx=20, pady=10)

        try:
            cursor.execute("""
                SELECT surname || ' ' || othernames AS full_name, sex, dob 
                FROM students WHERE reg_no=?
            """, (reg_no,))
            bio_data = cursor.fetchone()

            labels = ["Full Name:", "Sex:", "Date of Birth:"]
            if bio_data:
                for i, label in enumerate(labels[:len(bio_data)]):
                    value = bio_data[i] if bio_data[i] else "N/A"
                    tk.Label(bio_frame, text=label, bg=BG_COLOR, anchor="w", width=15).grid(row=i, column=0, sticky="w")
                    tk.Label(bio_frame, text=value, bg=BG_COLOR, anchor="w").grid(row=i, column=1, sticky="w")
            else:
                tk.Label(bio_frame, text="No Bio Data Found", bg=BG_COLOR, fg="red").grid(row=0, column=0, columnspan=2,
                                                                                          sticky="w")
        except Exception as e:
            tk.Label(bio_frame, text=f"Error: {str(e)}", bg=BG_COLOR, fg="red").grid(row=0, column=0, columnspan=2,
                                                                                     sticky="w")

        # ========== UTME and POST-UTME Scores ==========
        scores_frame = tk.LabelFrame(profile_win, text="UTME and Post-UTME Scores", bg=BG_COLOR, padx=10, pady=10)
        scores_frame.pack(fill="x", padx=20, pady=10)

        try:
            cursor.execute("""
                SELECT subject1, score1, subject2, score2, subject3, score3, subject4, score4,
                       total_score, post_utme_score
                FROM utme_postutme WHERE reg_no=?
            """, (reg_no,))
            scores_data = cursor.fetchone()

            if scores_data:
                for i in range(4):
                    subj = scores_data[i * 2] or "N/A"
                    score = scores_data[i * 2 + 1] or "N/A"
                    tk.Label(scores_frame, text=f"{subj}:", bg=BG_COLOR, anchor="w", width=20).grid(row=i, column=0,
                                                                                                    sticky="w")
                    tk.Label(scores_frame, text=score, bg=BG_COLOR, anchor="w").grid(row=i, column=1, sticky="w")

                tk.Label(scores_frame, text="Total UTME Score:", bg=BG_COLOR, anchor="w", width=20).grid(row=4,
                                                                                                         column=0,
                                                                                                         sticky="w")
                tk.Label(scores_frame, text=scores_data[8] or "N/A", bg=BG_COLOR, anchor="w").grid(row=4, column=1,
                                                                                                   sticky="w")

                tk.Label(scores_frame, text="Post-UTME Score:", bg=BG_COLOR, anchor="w", width=20).grid(row=5, column=0,
                                                                                                        sticky="w")
                tk.Label(scores_frame, text=scores_data[9] or "N/A", bg=BG_COLOR, anchor="w").grid(row=5, column=1,
                                                                                                   sticky="w")
            else:
                tk.Label(scores_frame, text="No UTME/Post-UTME scores found", bg=BG_COLOR, fg="red").grid(row=0,
                                                                                                          column=0,
                                                                                                          columnspan=2,
                                                                                                          sticky="w")
        except Exception as e:
            tk.Label(scores_frame, text=f"Error loading scores: {str(e)}", bg=BG_COLOR, fg="red").grid(row=0, column=0,
                                                                                                       columnspan=2,
                                                                                                       sticky="w")

        # ========== O'Level Results ==========
        olevel_frame = tk.LabelFrame(profile_win, text="O'Level Results", bg=BG_COLOR, padx=10, pady=10)
        olevel_frame.pack(fill="x", padx=20, pady=10)

        try:
            cursor.execute("""
                SELECT subject1, grade1, subject2, grade2, subject3, grade3,
                       subject4, grade4, subject5, grade5, subject6, grade6,
                       subject7, grade7, subject8, grade8, subject9, grade9
                FROM olevel_results WHERE reg_no=?
            """, (reg_no,))
            olevel_data = cursor.fetchone()

            if olevel_data:
                for i in range(9):
                    subject = olevel_data[i * 2] or "N/A"
                    grade = olevel_data[i * 2 + 1] or "N/A"
                    tk.Label(olevel_frame, text=f"{subject}:", bg=BG_COLOR, anchor="w", width=20).grid(row=i, column=0,
                                                                                                       sticky="w")
                    tk.Label(olevel_frame, text=grade, bg=BG_COLOR, anchor="w").grid(row=i, column=1, sticky="w")
            else:
                tk.Label(olevel_frame, text="No O'Level Results Found", bg=BG_COLOR, fg="red").grid(row=0, column=0,
                                                                                                    columnspan=2,
                                                                                                    sticky="w")
        except Exception as e:
            tk.Label(olevel_frame, text=f"Error loading O'Level data: {str(e)}", bg=BG_COLOR, fg="red").grid(row=0,
                                                                                                             column=0,
                                                                                                             columnspan=2,
                                                                                                             sticky="w")

        conn.close()

    def enable_editing(self):
        selected = self.tree.focus()
        if not selected:
            return

        self.editing_entries = {}  # Track the editable fields
        values = self.tree.item(selected)['values']
        cols = self.tree['columns']

        for i, (col, val) in enumerate(zip(cols, values)):
            bbox = self.tree.bbox(selected, column=col)
            if bbox:
                x, y, width, height = bbox
                entry = tk.Entry(self.tree)
                entry.place(x=x, y=y, width=width, height=height)
                entry.insert(0, val)
                self.editing_entries[col] = entry

        self.save_btn.config(state=tk.NORMAL)
        self.cancel_btn.config(state=tk.NORMAL)
        self.delete_btn.config(state=tk.NORMAL)

    def enable_inline_editing(self):
        selected = self.tree.focus()
        if not selected:
            return

        self.editing_cells = []
        values = self.tree.item(selected)['values']
        columns = self.tree['columns']

        for i, col in enumerate(columns[1:], start=1):  # Skip reg_no
            x, y, width, height = self.tree.bbox(selected, column=col)
            entry = tk.Entry(self.tree)
            entry.insert(0, values[i])
            entry.place(x=x, y=y, width=width, height=height)
            self.editing_cells.append((col, entry))

        self.save_btn.config(state=tk.NORMAL)
        self.cancel_btn.config(state=tk.NORMAL)
        self.edit_btn.config(state=tk.DISABLED)

    def cancel_editing(self):
        if hasattr(self, 'editing_cells'):
            for _, entry in self.editing_cells:
                entry.destroy()
            self.editing_cells.clear()

        # Re-enable only Edit (since nothing was saved or deleted)
        self.edit_btn.config(state=tk.NORMAL)
        self.save_btn.config(state=tk.DISABLED)
        self.cancel_btn.config(state=tk.DISABLED)
        self.delete_btn.config(state=tk.DISABLED)

    def delete_candidate(self):
        selected = self.tree.focus()
        if not selected:
            return

        values = self.tree.item(selected)['values']
        reg_no = values[0]

        confirm = messagebox.askyesno("Delete Candidate", f"Are you sure you want to delete candidate {reg_no}?")
        if not confirm:
            return

        # Delete from database
        conn = sqlite3.connect("students.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM students WHERE reg_no=?", (reg_no,))
        conn.commit()
        conn.close()

        # Remove from Treeview
        self.tree.delete(selected)

        # Reset photo and buttons
        self.photo_label.config(image='', text='No Photo Found')
        self.save_btn.config(state=tk.DISABLED)
        self.cancel_btn.config(state=tk.DISABLED)
        self.delete_btn.config(state=tk.DISABLED)

    def on_row_select(self, event):
        selected_item = self.tree.selection()
        if selected_item:
            # Re-enable Edit/Delete
            self.edit_btn.config(state=tk.NORMAL)
            self.save_btn.config(state=tk.DISABLED)
            self.cancel_btn.config(state=tk.DISABLED)
            self.delete_btn.config(state=tk.NORMAL)

            # Load photo
            reg_no = self.tree.item(selected_item[0])['values'][0]
            conn = sqlite3.connect("students.db")
            cursor = conn.cursor()
            cursor.execute("SELECT photo_path FROM students WHERE reg_no=?", (reg_no,))
            row = cursor.fetchone()
            conn.close()
            if row and os.path.exists(row[0]):
                img = Image.open(row[0])
                img = img.resize((120, 120))
                photo = ImageTk.PhotoImage(img)
                self.photo_label.configure(image=photo)
                self.photo_label.image = photo
            else:
                self.photo_label.configure(image='', text="No Photo Found")

    def student_registration(self):
        reg_win = tk.Toplevel(self.root)
        reg_win.title("Student Registration Portal")
        reg_win.geometry(f"{SCREEN_WIDTH}x{SCREEN_HEIGHT}")
        reg_win.configure(bg=BG_COLOR)

        self.reg_entries = {}
        self.photo_path = tk.StringVar()

        row = 0

        # --- Biodata Fields ---
        fields = {
            'Registration Number': None,
            'Surname': None,
            'Other Names': None,
            'Sex': ['Male', 'Female'],
            'Preferred Course of Study': [
                "Computer Science", "Physics", "Industrial Chemistry", "Microbiology",
                "Animal and Environmental Biology", "Biochemistry",
                "Plant Science and Biotechnology", "Applied Physics", "Mathematics and Statistics"
            ],
            'Date of Birth': None,
            'Nationality': None,
            'Session': None,
            'Date of Registration': None,
            'Year': None
        }

        for label, options in fields.items():
            tk.Label(reg_win, text=label + ':', font=FONT_NORMAL, bg=BG_COLOR).grid(row=row, column=0, sticky='e',
                                                                                    padx=10, pady=6)
            if isinstance(options, list):
                cb = ttk.Combobox(reg_win, values=options, font=FONT_NORMAL, state="readonly")
                cb.grid(row=row, column=1, sticky='w', pady=6)
                self.reg_entries[label] = cb
            else:
                entry = tk.Entry(reg_win, font=FONT_NORMAL)
                entry.grid(row=row, column=1, sticky='w', pady=6)
                self.reg_entries[label] = entry
            row += 1

        # --- Photo Upload ---
        tk.Label(reg_win, text="Passport Photo:", font=FONT_NORMAL, bg=BG_COLOR).grid(row=row, column=0, sticky='e',
                                                                                      pady=6)
        tk.Entry(reg_win, textvariable=self.photo_path, font=FONT_NORMAL, state='readonly').grid(row=row, column=1,
                                                                                                 sticky='w', pady=6)
        tk.Button(reg_win, text="Browse", font=FONT_NORMAL, command=self.browse_photo).grid(row=row, column=2, padx=10)
        row += 1

        # --- Buttons ---
        btn_frame = tk.Frame(reg_win, bg=BG_COLOR)
        btn_frame.grid(row=row, columnspan=3, pady=20)

        tk.Button(btn_frame, text="Save", font=FONT_NORMAL, command=self.full_student_registration).grid(row=0,
                                                                                                         column=0,
                                                                                                         padx=10)
        tk.Button(btn_frame, text="Cancel", font=FONT_NORMAL, command=self.clear_entries).grid(row=0, column=1, padx=10)
        tk.Button(btn_frame, text="Close", font=FONT_NORMAL, command=reg_win.destroy).grid(row=0, column=2, padx=10)
        tk.Button(btn_frame, text="Proceed to O'Level Portal", font=FONT_NORMAL,
                  command=self.olevel_subject_portal).grid(row=0, column=3, padx=10)

    def browse_photo(self):
        file_path = filedialog.askopenfilename(filetypes=[["Image Files", "*.png *.jpg *.jpeg"]])
        if file_path:
            self.photo_path.set(file_path)

    def clear_entries(self):
        for widget in self.reg_entries.values():
            if isinstance(widget, ttk.Combobox):
                widget.set('')
            else:
                widget.delete(0, tk.END)
        self.photo_path.set('')

    def save_registration(self):
        data = {}
        for label, widget in self.reg_entries.items():
            value = widget.get().strip()
            if not value:
                messagebox.showerror("Input Error", f"Please enter/select {label}.")
                return
            data[label] = value

        reg_no = data['Registration Number']
        preferred_course = data['Preferred Course of Study']
        photo = self.photo_path.get()
        if not photo:
            messagebox.showerror("Input Error", "Please upload a passport photo.")
            return

        try:
            conn = sqlite3.connect("students.db")
            cursor = conn.cursor()
            cursor.execute('''INSERT INTO students (
                                reg_no, surname, othernames, sex, preferred_course,
                                dob, nationality, session, reg_date, year, photo_path)
                              VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                           (reg_no, data['Surname'], data['Other Names'], data['Sex'], preferred_course,
                            data['Date of Birth'], data['Nationality'], data['Session'],
                            data['Date of Registration'], data['Year'], photo))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Student registered successfully!")
            self.clear_entries()
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "A student with this registration number already exists.")

    def prediction_portal(self):
        pred_win = tk.Toplevel(self.root)
        pred_win.title("Prediction Portal")
        pred_win.geometry(f"{SCREEN_WIDTH}x{SCREEN_HEIGHT}")
        pred_win.configure(bg=BG_COLOR)

        tk.Label(pred_win, text="Student Prediction Portal", font=FONT_HEADER, bg=BG_COLOR).pack(pady=20)

        form_frame = tk.Frame(pred_win, bg=BG_COLOR)
        form_frame.pack(pady=10)

        tk.Label(form_frame, text="Select Registration Number:", font=FONT_NORMAL, bg=BG_COLOR) \
            .grid(row=0, column=0, padx=10, pady=10)

        # Fetch registration numbers
        conn = sqlite3.connect("students.db")
        cursor = conn.cursor()
        cursor.execute("SELECT reg_no FROM students")
        reg_nos = [row[0] for row in cursor.fetchall()]
        conn.close()

        self.selected_reg_no = tk.StringVar()
        reg_no_dropdown = ttk.Combobox(form_frame, textvariable=self.selected_reg_no,
                                       values=reg_nos, font=FONT_NORMAL, state='readonly')
        reg_no_dropdown.grid(row=0, column=1, padx=10, pady=10)

        # Predict Course button
        predict_btn = tk.Button(form_frame, text="Predict Course", font=FONT_NORMAL,
                                command=self.perform_prediction, width=20)
        predict_btn.grid(row=1, columnspan=2, pady=15)

        # View Candidate Courses button
        view_btn = tk.Button(form_frame, text="View Candidate Courses", font=FONT_NORMAL,
                             command=self.view_candidate_courses, width=20)
        view_btn.grid(row=2, columnspan=2, pady=10)

        # Exit button
        exit_btn = tk.Button(form_frame, text="Exit", font=FONT_NORMAL,
                             command=pred_win.destroy, width=12)
        exit_btn.grid(row=3, columnspan=2, pady=20)

        # Prediction result display
        self.prediction_result = tk.StringVar()
        tk.Label(pred_win, textvariable=self.prediction_result, font=FONT_HEADER,
                 bg=BG_COLOR, fg="blue").pack(pady=20)

    def view_candidate_courses(self):
        win = tk.Toplevel(self.root)
        win.title("Candidate Courses Portal")
        win.geometry(f"{SCREEN_WIDTH}x{SCREEN_HEIGHT}")
        win.configure(bg=BG_COLOR)

        tk.Label(win, text="Candidate Course Records", font=FONT_HEADER, bg=BG_COLOR, fg="white").pack(pady=20)

        # Outer container to hold Treeview and buttons together
        container = tk.Frame(win, bg=BG_COLOR)
        container.pack(fill="both", expand=True, padx=20, pady=10)

        # Treeview section
        tree_frame = tk.Frame(container, bg=BG_COLOR)
        tree_frame.pack(fill="both", expand=True)

        columns = ("sn", "reg_no", "name", "preferred_course", "predicted_course", "admission_status")
        tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=20)

        for col in columns:
            heading = "S/N" if col == "sn" else col.replace("_", " ").title()
            width = 60 if col == "sn" else 200
            tree.heading(col, text=heading)
            tree.column(col, anchor='center', width=width)

        tree.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        self.candidate_tree = tree  # Save reference

        # Button frame — directly below treeview
        btn_frame = tk.Frame(container, bg=BG_COLOR)
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="Print", width=15, command=self.print_candidate_data).grid(row=0, column=1, padx=10)
        tk.Button(btn_frame, text="Export XLSX", width=15, command=self.export_candidate_excel).grid(row=0, column=2,
                                                                                                     padx=10)
        tk.Button(btn_frame, text="Export PDF", width=15, command=self.export_candidate_pdf).grid(row=0, column=3,
                                                                                                  padx=10)
        tk.Button(btn_frame, text="Clear All", width=15, command=self.clear_candidate_data).grid(row=0, column=4,
                                                                                                 padx=10)
        tk.Button(btn_frame, text="Exit", width=15, command=win.destroy).grid(row=0, column=5, padx=10)
        tk.Button(btn_frame, text="Import & Predict", width=15, command=self.import_candidate_prediction_data).grid(
            row=0, column=0, padx=10)

        self.predict_admissions()
        self.load_candidate_courses_data()

    def load_candidate_courses_data(self):
        try:
            # If the Treeview is not defined or destroyed, exit early
            if not hasattr(self, 'candidate_tree') or not self.candidate_tree.winfo_exists():
                return

            conn = sqlite3.connect("students.db")
            cursor = conn.cursor()
            cursor.execute(
                "SELECT reg_no, name, preferred_course, predicted_course, admission_status FROM candidate_courses"
            )
            rows = cursor.fetchall()
            conn.close()

            # Clear existing rows
            for row in self.candidate_tree.get_children():
                self.candidate_tree.delete(row)

            # Insert new data
            for idx, row in enumerate(rows, start=1):
                self.candidate_tree.insert("", "end", values=(idx, *row))

        except Exception as e:
            messagebox.showerror("Load Error", f"❌ Could not load data:\n{e}")

    def export_candidate_excel(self):
        import pandas as pd
        conn = sqlite3.connect("students.db")
        df = pd.read_sql_query("SELECT * FROM candidate_courses", conn)
        df.to_excel("candidate_courses.xlsx", index=False)
        conn.close()

    def export_candidate_pdf(self):
        from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
        from reportlab.lib import colors

        conn = sqlite3.connect("students.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM candidate_courses")
        data = cursor.fetchall()
        conn.close()

        pdf = SimpleDocTemplate("candidate_courses.pdf")
        table_data = [("Reg No", "Name", "Preferred Course", "Predicted Course", "Admission Status")] + data
        table = Table(table_data)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        pdf.build([table])

    def clear_candidate_data(self):
        confirm = messagebox.askyesno("Confirm", "Are you sure you want to clear all candidate course entries?")
        if confirm:
            conn = sqlite3.connect("students.db")
            cursor = conn.cursor()
            cursor.execute("DELETE FROM candidate_courses")
            conn.commit()
            conn.close()
            self.load_candidate_courses_data()

    def print_candidate_data(self):
        import tempfile
        import os

        # Create a temporary text file with candidate data
        with tempfile.NamedTemporaryFile(delete=False, suffix=".txt", mode='w', encoding='utf-8') as temp_file:
            temp_file.write("Reg No\tName\tPreferred Course\tPredicted Course\tAdmission Status\n")
            for row in self.candidate_tree.get_children():
                values = self.candidate_tree.item(row)["values"]
                line = "\t".join(str(v) for v in values)
                temp_file.write(f"{line}\n")
            temp_path = temp_file.name

        try:
            # Attempt to open print dialog on Windows
            os.startfile(temp_path, "print")
        except Exception as e:
            messagebox.showerror("Print Error", f"Could not send to printer: {e}")

    def olevel_subject_portal(self):
        win = tk.Toplevel(self.root)
        win.title("O'Level Subject Portal")
        win.geometry(f"{SCREEN_WIDTH}x{SCREEN_HEIGHT}")
        win.configure(bg=BG_COLOR)

        tk.Label(win, text="Enter O'Level Results", font=FONT_HEADER, bg=BG_COLOR).pack(pady=20)

        form_frame = tk.Frame(win, bg=BG_COLOR)
        form_frame.pack()

        # Fetch registered reg_nos
        conn = sqlite3.connect("students.db")
        cursor = conn.cursor()
        cursor.execute("SELECT reg_no FROM students")
        reg_nos = [row[0] for row in cursor.fetchall()]
        conn.close()

        tk.Label(form_frame, text="Select Registration Number:", font=FONT_NORMAL, bg=BG_COLOR).grid(row=0, column=0, padx=10, pady=10, sticky='e')
        self.selected_olevel_reg = tk.StringVar()
        reg_combo = ttk.Combobox(form_frame, textvariable=self.selected_olevel_reg, values=reg_nos, font=FONT_NORMAL, state='readonly')
        reg_combo.grid(row=0, column=1, padx=10, pady=10, sticky='w')

        # Input for 9 subjects and grades
        self.olevel_subjects = []
        self.olevel_grades = []
        grades = ["A1", "B2", "B3", "C4", "C5", "C6", "D7", "E8", "F9"]

        for i in range(9):
            tk.Label(form_frame, text=f"Subject {i+1}:", font=FONT_NORMAL, bg=BG_COLOR).grid(row=i+1, column=0, padx=10, pady=5, sticky='e')
            sub_entry = tk.Entry(form_frame, font=FONT_NORMAL)
            sub_entry.grid(row=i+1, column=1, padx=10, pady=5, sticky='w')
            self.olevel_subjects.append(sub_entry)

            grade_combo = ttk.Combobox(form_frame, values=grades, font=FONT_NORMAL, state='readonly', width=5)
            grade_combo.grid(row=i+1, column=2, padx=10, pady=5, sticky='w')
            self.olevel_grades.append(grade_combo)

        tk.Button(win, text="Save Results", font=FONT_NORMAL, command=self.save_olevel_results).pack(pady=20)
        tk.Button(win, text="Proceed to UTME/POST-UTME Portal", font=FONT_NORMAL, command=self.open_utme_portal).pack(
            pady=10)
        tk.Button(win, text="Exit", font=FONT_NORMAL, command=win.destroy).pack(pady=(0, 20))

    def print_candidate_data(self):
        if not hasattr(self, 'candidate_tree'):
            return

        data = []
        headers = [self.candidate_tree.heading(col)["text"] for col in self.candidate_tree["columns"]]
        data.append("\t".join(headers))

        for item in self.candidate_tree.get_children():
            row = self.candidate_tree.item(item)["values"]
            data.append("\t".join(str(val) for val in row))

        output_text = "\n".join(data)

        # Write to a temporary file
        with tempfile.NamedTemporaryFile("w", delete=False, suffix=".txt") as f:
            f.write(output_text)
            temp_filename = f.name

        # Open default print dialog (Windows only)
        os.startfile(temp_filename, "print")

    def save_olevel_results(self):
        reg_no = self.selected_olevel_reg.get()
        if not reg_no:
            messagebox.showerror("Error", "Please select a registration number.")
            return

        subjects = [entry.get().strip() for entry in self.olevel_subjects]
        grades = [combo.get().strip() for combo in self.olevel_grades]

        if any(not s for s in subjects) or any(not g for g in grades):
            messagebox.showerror("Input Error", "All 9 subjects and grades must be filled.")
            return

        try:
            conn = sqlite3.connect("students.db")
            cursor = conn.cursor()
            cursor.execute('''
                INSERT OR REPLACE INTO olevel_results (
                    reg_no,
                    subject1, grade1,
                    subject2, grade2,
                    subject3, grade3,
                    subject4, grade4,
                    subject5, grade5,
                    subject6, grade6,
                    subject7, grade7,
                    subject8, grade8,
                    subject9, grade9
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (reg_no, *sum(zip(subjects, grades), ())))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "O'Level results saved successfully!")
        except Exception as e:
            messagebox.showerror("Database Error", str(e))

    def perform_prediction(self):
        reg_no = self.selected_reg_no.get()
        if not reg_no:
            messagebox.showerror("Error", "Please select a registration number.")
            return

        predicted_courses = ["Computer Science", "Physics", "Industrial Chemistry", "Microbiology",
                             "Animal and Environmental Biology", "Biochemistry", "Plant Science and Biotechnology",
                             "Applied Physics", "Mathematics and Statistics"]
        result = random.choice(predicted_courses)

        self.prediction_result.set(f"Predicted Course of Study for {reg_no}: {result}")

# --- Initialize App ---
if __name__ == "__main__":
    initialize_db()
    root = tk.Tk()
    LoginScreen(root)
    root.mainloop()

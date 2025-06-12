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



# Ensure consistent connection to the correct database
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "students.db")
conn = sqlite3.connect(db_path)






# --- Constants ---
SCREEN_WIDTH = 1400
SCREEN_HEIGHT = 1050
BG_COLOR = "#F5F5F5"  # Milk color
FONT_HEADER = ("Helvetica", 18, "bold")
FONT_NORMAL = ("Helvetica", 12)
DB_NAME = "students.db"

# --- Database Setup ---
def initialize_db():
    conn = sqlite3.connect(DB_NAME)
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
    cursor.execute("DROP TABLE IF EXISTS olevel_results")

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
        self.root.configure(bg=BG_COLOR)

        tk.Label(root, text="Welcome to the Curriculum Enhancement System", font=FONT_HEADER, bg=BG_COLOR).pack(pady=60)

        frame = tk.Frame(root, bg=BG_COLOR)
        frame.pack()

        tk.Label(frame, text="Username:", font=FONT_NORMAL, bg=BG_COLOR).grid(row=0, column=0, pady=10, sticky="e")
        self.username_entry = tk.Entry(frame, font=FONT_NORMAL)
        self.username_entry.grid(row=0, column=1, pady=10)

        tk.Label(frame, text="Password:", font=FONT_NORMAL, bg=BG_COLOR).grid(row=1, column=0, pady=10, sticky="e")
        self.password_entry = tk.Entry(frame, font=FONT_NORMAL, show="*")
        self.password_entry.grid(row=1, column=1, pady=10)

        tk.Button(frame, text="Login", font=FONT_NORMAL, command=self.login).grid(row=2, columnspan=2, pady=20)

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

        menubar = tk.Menu(root)

        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Student Registration", command=self.student_registration)
        filemenu.add_command(label="Registered Candidates", command=self.registered_candidates)
        filemenu.add_command(label="O'Level Subject Portal", command=self.olevel_subject_portal)
        filemenu.add_command(label="UTME/POST-UTME Scores Portal", command=self.open_utme_portal)
        filemenu.add_command(label="Prediction Portal", command=self.prediction_portal)
        menubar.add_cascade(label="File", menu=filemenu)

        utilitymenu = tk.Menu(menubar, tearoff=0)
        utilitymenu.add_command(label="UTME/POST UTME Comparison")
        menubar.add_cascade(label="Utility", menu=utilitymenu)

        root.config(menu=menubar)

        tk.Label(root, text="Admin Dashboard", font=FONT_HEADER, bg=BG_COLOR).pack(pady=40)

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
        conn = sqlite3.connect(DB_NAME)
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

        conn = sqlite3.connect(DB_NAME)
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
        conn = sqlite3.connect(DB_NAME)
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
        conn = sqlite3.connect(DB_NAME)
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

            conn = sqlite3.connect(DB_NAME)
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

        tk.Button(win, text="Save Scores", font=FONT_NORMAL, command=save_scores).pack(pady=20)

    def registered_candidates(self):
        win = tk.Toplevel(self.root)
        win.title("Registered Candidates")
        win.geometry(f"{SCREEN_WIDTH}x{SCREEN_HEIGHT}")
        win.configure(bg=BG_COLOR)

        frame = tk.Frame(win, bg=BG_COLOR)
        frame.pack(fill="both", expand=True)

        columns = ("reg_no", "surname", "othernames", "sex", "dob", "nationality", "session", "reg_date", "year")
        tree = ttk.Treeview(frame, columns=columns, show="headings", height=25)

        # Buttons
        btn_frame = tk.Frame(frame, bg=BG_COLOR)  # ✅ Attach it to 'frame', not 'win'
        btn_frame.grid(row=1, column=0, columnspan=2, pady=10, sticky="w")

        export_btn = tk.Button(btn_frame, text="Export", command=self.export_treeview_data)
        export_btn.grid(row=0, column=5, padx=5)

        import_btn = tk.Button(btn_frame, text="Import File", command=self.import_file_data)
        import_btn.grid(row=0, column=4, padx=10)

        profile_btn = tk.Button(btn_frame, text="View Profile", command=self.show_full_profile)
        profile_btn.grid(row=0, column=6, padx=5)

        # view_btn = tk.Button(btn_frame, text="View Profile", command=self.show_full_profile)
        # view_btn.grid(row=0, column=4, padx=10)

        self.edit_btn = tk.Button(btn_frame, text="Edit", command=self.enable_inline_editing)
        self.edit_btn.grid(row=0, column=0, padx=10)

        self.save_btn = tk.Button(btn_frame, text="Save", command=self.save_changes, state=tk.DISABLED)
        self.save_btn.grid(row=0, column=1, padx=10)

        self.cancel_btn = tk.Button(btn_frame, text="Cancel", command=self.cancel_editing, state=tk.DISABLED)
        self.cancel_btn.grid(row=0, column=2, padx=10)

        self.delete_btn = tk.Button(btn_frame, text="Delete", command=self.delete_candidate, state=tk.DISABLED)
        self.delete_btn.grid(row=0, column=3, padx=10)

        for col in columns:
            tree.heading(col, text=col.replace("_", " ").title())
            tree.column(col, anchor='center', width=120)

        self.tree = tree  # Store treeview for global access in this window
        tree.bind("<<TreeviewSelect>>", self.on_row_select)

        tree.grid(row=0, column=0, padx=20, pady=10, sticky="nsew")

        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=0, column=1, sticky="ns")

        # Photo display area
        photo_frame = tk.Frame(frame, bg=BG_COLOR)
        photo_frame.grid(row=0, column=2, padx=30, sticky="n")

        self.photo_label = tk.Label(photo_frame, bg=BG_COLOR)
        self.photo_label.pack(pady=10)

        self.delete_btn = tk.Button(btn_frame, text="Delete", command=self.delete_candidate, state=tk.DISABLED)
        self.delete_btn.grid(row=0, column=3, padx=5)

        def on_select(event):
            selected_item = tree.selection()
            if selected_item:
                reg_no = tree.item(selected_item[0])['values'][0]
                conn = sqlite3.connect(DB_NAME)
                cursor = conn.cursor()
                cursor.execute("SELECT photo_path FROM students WHERE reg_no=?", (reg_no,))
                row = cursor.fetchone()
                conn.close()
                if row and os.path.exists(row[0]):
                    img = Image.open(row[0])
                    img = img.resize((50, 50))
                    photo = ImageTk.PhotoImage(img)
                    self.photo_label.configure(image=photo)
                    self.photo_label.image = photo
                else:
                    self.photo_label.configure(image='', text="No Photo Found")

        # tree.bind("<<TreeviewSelect>>", on_select)

        # Load data from DB
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT reg_no, surname, othernames, sex, dob, nationality, session, reg_date, year FROM students")
        for row in cursor.fetchall():
            tree.insert("", "end", values=row)
        conn.close()

    def import_file_data(self):
        file_path = filedialog.askopenfilename(
            title="Select CSV or Excel file",
            filetypes=[("CSV files", "*.csv"), ("Excel files", "*.xlsx *.xls")]
        )
        if not file_path:
            return  # User cancelled

        try:
            # Auto-detect file type and load with pandas
            if file_path.endswith('.csv'):
                df = pd.read_csv(file_path)
            else:
                df = pd.read_excel(file_path)

            required_columns = ['reg_no', 'surname', 'othernames', 'sex', 'dob',
                                'nationality', 'session', 'reg_date', 'year']

            if not all(col in df.columns for col in required_columns):
                messagebox.showerror("Error", "Missing required columns in file.")
                return

            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()

            for _, row in df.iterrows():
                values = tuple(row[col] for col in required_columns)

                # Insert into DB
                cursor.execute("""
                    INSERT OR REPLACE INTO students (
                        reg_no, surname, othernames, sex, dob, 
                        nationality, session, reg_date, year
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, values)

                # Insert into Treeview
                self.tree.insert("", "end", values=values)

            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Data imported successfully.")
        except Exception as e:
            messagebox.showerror("Import Error", f"Could not import file:\n{e}")

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

        reg_no = self.tree.item(selected)['values'][0]

        # Correct DB path
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(BASE_DIR, "students.db")
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        profile_win = tk.Toplevel(self.root)
        profile_win.title(f"Candidate Profile: {reg_no}")
        profile_win.geometry("800x600")
        profile_win.configure(bg=BG_COLOR)

        # ========== Frame for Bio Data ==========
        bio_frame = tk.LabelFrame(profile_win, text="Bio Data", bg=BG_COLOR, padx=10, pady=10)
        bio_frame.pack(fill="x", padx=20, pady=10)

        try:
            cursor.execute("""
                SELECT surname || ' ' || othernames AS full_name, sex, dob 
                FROM students WHERE reg_no=?
            """, (reg_no,))
            bio_data = cursor.fetchone()

            labels = ["Full Name:", "Sex:", "Date of Birth:", "Email:"]
            if bio_data:
                for i, label in enumerate(labels[:len(bio_data)]):  # Avoid IndexError
                    value = bio_data[i] if bio_data[i] else "N/A"
                    tk.Label(bio_frame, text=label, bg=BG_COLOR, anchor="w", width=15).grid(row=i, column=0, sticky="w")
                    tk.Label(bio_frame, text=value, bg=BG_COLOR, anchor="w").grid(row=i, column=1, sticky="w")
            else:
                tk.Label(bio_frame, text="No Bio Data Found", bg=BG_COLOR, fg="red").grid(row=0, column=0, columnspan=2,
                                                                                          sticky="w")

        except Exception as e:
            tk.Label(bio_frame, text=f"Error: {str(e)}", bg=BG_COLOR, fg="red").grid(row=0, column=0, columnspan=2,
                                                                                     sticky="w")

        # ========== UTME and POST-UTME Scores Frame ==========
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

                # ========== O'Level Results Frame ==========
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
                            tk.Label(olevel_frame, text=f"{subject}:", bg=BG_COLOR, anchor="w", width=20).grid(
                                    row=i, column=0, sticky="w")
                            tk.Label(olevel_frame, text=grade, bg=BG_COLOR, anchor="w").grid(row=i, column=1,
                                                                                                 sticky="w")
                    else:
                        tk.Label(olevel_frame, text="No O'Level Results Found", bg=BG_COLOR, fg="red").grid(row=0,
                                                                                                                column=0,
                                                                                                                columnspan=2,
                                                                                                                sticky="w")

                except Exception as e:
                    tk.Label(olevel_frame, text=f"Error loading O'Level data: {str(e)}", bg=BG_COLOR,
                                fg="red").grid(row=0, column=0, columnspan=2, sticky="w")

                # Display total and post-UTME scores
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
        conn = sqlite3.connect(DB_NAME)
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
            conn = sqlite3.connect(DB_NAME)
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

        fields = {
            'Registration Number': None,
            'Surname': None,
            'Other Names': None,
            'Sex': ['Male', 'Female'],
            'Date of Birth': None,
            'Nationality': None,
            'Session': None,
            'Date of Registration': None,
            'Year': None
        }

        self.reg_entries = {}
        self.photo_path = tk.StringVar()

        row = 0
        for label, options in fields.items():
            tk.Label(reg_win, text=label + ':', font=FONT_NORMAL, bg=BG_COLOR).grid(row=row, column=0, sticky='e', pady=8, padx=10)
            if isinstance(options, list):
                cb = ttk.Combobox(reg_win, values=options, font=FONT_NORMAL, state="readonly")
                cb.grid(row=row, column=1, pady=8, sticky='w')
                self.reg_entries[label] = cb
            else:
                entry = tk.Entry(reg_win, font=FONT_NORMAL)
                entry.grid(row=row, column=1, pady=8, sticky='w')
                self.reg_entries[label] = entry
            row += 1

        # Photo Upload
        tk.Label(reg_win, text="Passport Photo:", font=FONT_NORMAL, bg=BG_COLOR).grid(row=row, column=0, sticky='e', pady=8)
        tk.Entry(reg_win, textvariable=self.photo_path, font=FONT_NORMAL, state='readonly').grid(row=row, column=1, pady=8, sticky='w')
        tk.Button(reg_win, text="Browse", font=FONT_NORMAL, command=self.browse_photo).grid(row=row, column=2, padx=10)

        row += 1

        # Buttons
        btn_frame = tk.Frame(reg_win, bg=BG_COLOR)
        btn_frame.grid(row=row, columnspan=3, pady=20)

        tk.Button(btn_frame, text="Save", font=FONT_NORMAL, command=self.save_registration).grid(row=0, column=0, padx=10)
        tk.Button(btn_frame, text="Cancel", font=FONT_NORMAL, command=lambda: self.clear_entries()).grid(row=0, column=1, padx=10)
        tk.Button(btn_frame, text="Close", font=FONT_NORMAL, command=reg_win.destroy).grid(row=0, column=2, padx=10)

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
        photo = self.photo_path.get()
        if not photo:
            messagebox.showerror("Input Error", "Please upload a passport photo.")
            return

        try:
            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()
            cursor.execute('''INSERT INTO students (reg_no, surname, othernames, sex, dob, nationality, session, reg_date, year, photo_path)
                              VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                           (reg_no, data['Surname'], data['Other Names'], data['Sex'], data['Date of Birth'],
                            data['Nationality'], data['Session'], data['Date of Registration'], data['Year'], photo))
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

        tk.Label(form_frame, text="Select Registration Number:", font=FONT_NORMAL, bg=BG_COLOR).grid(row=0, column=0, padx=10, pady=10)

        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT reg_no FROM students")
        reg_nos = [row[0] for row in cursor.fetchall()]
        conn.close()

        self.selected_reg_no = tk.StringVar()
        reg_no_dropdown = ttk.Combobox(form_frame, textvariable=self.selected_reg_no, values=reg_nos, font=FONT_NORMAL, state='readonly')
        reg_no_dropdown.grid(row=0, column=1, padx=10, pady=10)

        tk.Button(form_frame, text="Predict Course", font=FONT_NORMAL, command=self.perform_prediction).grid(row=1, columnspan=2, pady=20)

        self.prediction_result = tk.StringVar()
        tk.Label(pred_win, textvariable=self.prediction_result, font=FONT_HEADER, bg=BG_COLOR, fg="blue").pack(pady=20)
    def olevel_subject_portal(self):
        win = tk.Toplevel(self.root)
        win.title("O'Level Subject Portal")
        win.geometry(f"{SCREEN_WIDTH}x{SCREEN_HEIGHT}")
        win.configure(bg=BG_COLOR)

        tk.Label(win, text="Enter O'Level Results", font=FONT_HEADER, bg=BG_COLOR).pack(pady=20)

        form_frame = tk.Frame(win, bg=BG_COLOR)
        form_frame.pack()

        # Fetch registered reg_nos
        conn = sqlite3.connect(DB_NAME)
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
            conn = sqlite3.connect(DB_NAME)
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

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

    ttk.Button(filter_frame, text="Apply Filter", command=filter_data, style="Small.TButton")\
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

    ttk.Button(action_frame, text="Import CSV", command=import_data, style="Small.TButton")\
        .grid(row=0, column=0, padx=5)
    ttk.Button(action_frame, text="Export CSV", command=export_csv, style="Small.TButton")\
        .grid(row=0, column=1, padx=5)
    ttk.Button(action_frame, text="Export PDF", command=export_pdf, style="Small.TButton")\
        .grid(row=0, column=2, padx=5)

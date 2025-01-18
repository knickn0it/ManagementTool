import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import customtkinter as ctk
import pandas as pd
import database

class EmployeeManagementApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Digit88 Employee Management System")
        self.root.geometry("900x600")  # Set the window size

        # Create the layout of the GUI (fields and labels)
        self.create_main_layout()
        
        # Load employee data
        self.show_employees()

    def create_main_layout(self):
        """Create all components for the main layout."""
        self.main_frame = ctk.CTkFrame(self.root)
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Create the layout of the GUI (fields and labels)
        self.create_search_field()
        self.create_input_fields()
        self.create_buttons()

        # Employee List Table (Treeview)
        self.create_table()

    def create_search_field(self):
        """Create search field and button."""
        self.search_label = ctk.CTkLabel(self.main_frame, text="Search:")
        self.search_label.grid(row=0, column=0, padx=10, pady=10, sticky="e")
        
        self.search_entry = ctk.CTkEntry(self.main_frame, placeholder_text="Search by Name, Team, Role, or ID")
        self.search_entry.grid(row=0, column=1, padx=10, pady=10, sticky="w")
        
        self.search_button = ctk.CTkButton(self.main_frame, text="Search", command=self.search_employees, width=200)
        self.search_button.grid(row=0, column=2, padx=20, pady=10)

    def create_input_fields(self):
        """Create input fields for Employee data."""
        labels = ["Employee ID", "Name", "Email", "Designation", "Role", "Team", "Skills"]
        self.entries = {}
        
        for i, label in enumerate(labels, start=1):
            ctk.CTkLabel(self.main_frame, text=label).grid(row=i, column=0, padx=10, pady=10, sticky="e")
            entry = ctk.CTkEntry(self.main_frame, placeholder_text=label)
            entry.grid(row=i, column=1, padx=10, pady=10, sticky="w")
            self.entries[label] = entry

    def create_buttons(self):
        """Create action buttons for Upload File, Add, Update, Delete, New Employee."""
        # Create a frame to hold the buttons, and place them in the second column
        self.button_frame = ctk.CTkFrame(self.main_frame)
        self.button_frame.grid(row=1, column=2, rowspan=8, padx=20, pady=10, sticky="ns")

        # Upload button
        self.upload_button = ctk.CTkButton(self.button_frame, text="Upload File", command=self.upload_file, width=200)
        self.upload_button.grid(row=0, column=0, padx=20, pady=10)

        # New Employee button
        self.new_employee_button = ctk.CTkButton(self.button_frame, text="New Employee", command=self.new_employee, width=200)
        self.new_employee_button.grid(row=1, column=0, padx=20, pady=10)

        # Add Employee button
        self.add_employee_button = ctk.CTkButton(self.button_frame, text="Add Employee", command=self.add_employee, width=200)
        self.add_employee_button.grid(row=2, column=0, padx=20, pady=10)

        # Update Employee button
        self.update_employee_button = ctk.CTkButton(self.button_frame, text="Update Employee", command=self.update_employee, width=200)
        self.update_employee_button.grid(row=3, column=0, padx=20, pady=10)

        # Delete Employee button
        self.delete_employee_button = ctk.CTkButton(self.button_frame, text="Delete Employee", command=self.delete_employee, width=200)
        self.delete_employee_button.grid(row=4, column=0, padx=20, pady=10)

        # Delete All button
        self.delete_all_button = ctk.CTkButton(self.button_frame, text="Delete All", command=self.delete_all_employees, width=200)
        self.delete_all_button.grid(row=5, column=0, padx=20, pady=10)

    def create_table(self):
        """Create the Employee List Table (Treeview)."""
        self.tree = ttk.Treeview(self.main_frame, columns=("ID", "Name", "Email", "Designation", "Role", "Team", "Skills"), show="headings")
        self.tree.grid(row=9, column=0, columnspan=3, padx=20, pady=10)

        # Define columns and their headings
        self.tree.heading("ID", text="Employee ID")
        self.tree.heading("Name", text="Name")
        self.tree.heading("Email", text="Email")
        self.tree.heading("Designation", text="Designation")
        self.tree.heading("Role", text="Role")
        self.tree.heading("Team", text="Team")
        self.tree.heading("Skills", text="Skills")

        # Set column widths and borders
        self.tree.column("ID", width=100, anchor="center", minwidth=50)
        self.tree.column("Name", width=150, anchor="w", minwidth=100)
        self.tree.column("Email", width=200, anchor="w", minwidth=100)
        self.tree.column("Designation", width=150, anchor="w", minwidth=100)
        self.tree.column("Role", width=100, anchor="center", minwidth=60)
        self.tree.column("Team", width=150, anchor="w", minwidth=100)
        self.tree.column("Skills", width=200, anchor="w", minwidth=100)

        # Style for the table
        style = ttk.Style(self.root)
        style.configure("Treeview.Heading", font=("Helvetica", 12, "bold"), background="#4CAF50", foreground="black")
        style.configure("Treeview", font=("Helvetica", 10), rowheight=30, background="white", fieldbackground="white", highlightthickness=0, bd=0)

        # Apply alternating row colors without borders
        style.configure("Treeview", rowheight=30, background="white", fieldbackground="white")
        self.tree.tag_configure("evenrow", background="#f4f4f4")  # Lighter background for even rows
        self.tree.tag_configure("oddrow", background="#ffffff")  # White background for odd rows

        # Highlight selected row color
        style.map("Treeview", background=[('selected', '#A9D08E')])  # Row color when selected

        # Bind row selection
        self.tree.bind("<ButtonRelease-1>", self.on_table_row_select)

    def add_employee(self):
        """Add a new employee."""
        employee = {
            "employee_id": self.entries["Employee ID"].get(),
            "name": self.entries["Name"].get(),
            "email": self.entries["Email"].get(),
            "designation": self.entries["Designation"].get(),
            "role": self.entries["Role"].get(),
            "team": self.entries["Team"].get(),
            "skills": self.entries["Skills"].get(),  # Added skills
        }

        if any(value == "" for value in employee.values()):
            messagebox.showerror("Error", "Please fill all fields")
            return
        
        database.add_employee(employee)
        self.show_employees()
        messagebox.showinfo("Success", "Employee Added Successfully!")

    def search_employees(self):
        """Search employees based on the filter term."""
        filter_term = self.search_entry.get()  # Get the search term
        self.show_employees(filter_term)  # Pass it to show_employees to update the table

    def update_employee(self):
        """Update an existing employee."""
        employee = {
            "employee_id": self.entries["Employee ID"].get(),
            "name": self.entries["Name"].get(),
            "email": self.entries["Email"].get(),
            "designation": self.entries["Designation"].get(),
            "role": self.entries["Role"].get(),
            "team": self.entries["Team"].get(),
            "skills": self.entries["Skills"].get(),  # Added skills
        }

        if any(value == "" for value in employee.values()):
            messagebox.showerror("Error", "Please fill all fields")
            return
        
        database.update_employee(employee)
        self.show_employees()
        messagebox.showinfo("Success", "Employee Updated Successfully!")

    def delete_employee(self):
        """Delete an employee."""
        employee_id = self.entries["Employee ID"].get()
        database.delete_employee(employee_id)
        self.show_employees()
        messagebox.showinfo("Success", "Employee Deleted Successfully!")

    def delete_all_employees(self):
        """Delete all employees from the database."""
        if messagebox.askyesno("Delete All", "Are you sure you want to delete all employee records?"):
            database.delete_all_employees()
            self.show_employees()
            messagebox.showinfo("Success", "All Employee Records Deleted!")

    def show_employees(self, filter_term=""):
        """Show all employees in the table with optional filtering."""
        employees = database.get_all_employees(filter_term)
        
        # Clear the table
        for row in self.tree.get_children():
            self.tree.delete(row)
        
        # Insert employee data into the table with alternating row colors
        for idx, emp in enumerate(employees):
            # Apply alternating row styles
            tag = "evenrow" if idx % 2 == 0 else "oddrow"
            self.tree.insert("", "end", values=(emp[0], emp[1], emp[2], emp[3], emp[4], emp[5], emp[6]), tags=(tag,))

    def on_table_row_select(self, event):
        """Select employee from table and fill data into the input fields."""
        selected_item = self.tree.selection()[0]
        selected_data = self.tree.item(selected_item, "values")

        # Populate input fields with selected employee data
        self.entries["Employee ID"].delete(0, ctk.END)
        self.entries["Employee ID"].insert(0, selected_data[0])

        self.entries["Name"].delete(0, ctk.END)
        self.entries["Name"].insert(0, selected_data[1])

        self.entries["Email"].delete(0, ctk.END)
        self.entries["Email"].insert(0, selected_data[2])

        self.entries["Designation"].delete(0, ctk.END)
        self.entries["Designation"].insert(0, selected_data[3])

        self.entries["Role"].delete(0, ctk.END)
        self.entries["Role"].insert(0, selected_data[4])

        self.entries["Team"].delete(0, ctk.END)
        self.entries["Team"].insert(0, selected_data[5])

        self.entries["Skills"].delete(0, ctk.END)
        self.entries["Skills"].insert(0, selected_data[6])

    def new_employee(self):
        """Clear all fields for a new employee."""
        for field in self.entries.values():
            field.delete(0, ctk.END)

    def upload_file(self):
        """Upload .csv or .xlsx file and populate the data."""
        file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv"), ("Excel Files", "*.xlsx")])

        if not file_path:
            return

        try:
            # Read file into DataFrame
            if file_path.endswith('.csv'):
                df = pd.read_csv(file_path)
            elif file_path.endswith('.xlsx'):
                df = pd.read_excel(file_path)

            # Check if the file matches the expected structure
            required_columns = ["Employee ID", "Name", "Email", "Designation", "Role", "Team", "Skills"]
            if not all(col in df.columns for col in required_columns):
                messagebox.showerror("Error", "The file does not have the correct columns.")
                return

            # Insert each row into the database
            for _, row in df.iterrows():
                employee = {
                    "employee_id": row["Employee ID"],
                    "name": row["Name"],
                    "email": row["Email"],
                    "designation": row["Designation"],
                    "role": row["Role"],
                    "team": row["Team"],
                    "skills": row["Skills"]
                }
                # Add employee to the database (will ignore if the ID already exists)
                database.add_employee(employee)

            self.show_employees()
            messagebox.showinfo("Success", "Employee data uploaded successfully!")

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

if __name__ == "__main__":
    root = ctk.CTk()
    app = EmployeeManagementApp(root)
    root.mainloop()

import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.font import Font
import pyodbc

class CharityApp:
    def __init__(self,win):
        self.root = root
        self.root.title("Charity Management System")
        self.root.geometry("600x400")
        self.root.configure(bg="white")
        
        self.style = ttk.Style()
        self.style.configure('TButton', font=('Arial', 12, 'bold'), padding=10)
        self.style.configure('TFrame', background='#f4f4f4')
        self.style.configure('TLabel', background='#f4f4f4', font=('Arial', 12))

        # Title
        ttk.Label(root, text="Charity Management System", font=('Arial', 20, 'bold'), background='#f4f4f4').pack(pady=50)
        
        self.main_frame = ttk.Frame(root)
        self.main_frame.pack(expand=True)
        
        self.create_button("Donation", "💰", self.show_donation, 0, )
        self.create_button("Receiver", "🤲", self.show_receiver, 1, )
        self.create_button("Manager", "👨💼", self.show_manager, 2, )
        self.create_button("Charity", "❤️", self.show_charity, 3, )
        
        self.style.map("TButton", background=[("active", "yellow")], foreground=[("active", "red")])
        
        
        self.status = ttk.Label(root, text="Connected to database: graceApp", relief=tk.SUNKEN)
        self.status.pack(side=tk.BOTTOM, fill=tk.X)

    def create_button(self, text, emoji, command, column):
        btn_frame = ttk.Frame(self.main_frame)
        btn_frame.grid(row=0, column=column, padx=40, pady=0)

        icon_label = ttk.Label(btn_frame, text=emoji, font=("Segoe UI Emoji", 36))
        icon_label.grid(row=10, column=0)
        icon_label.pack()
    
        btn = ttk.Button(btn_frame, text=text, command=command)
        btn.pack()

    def db_connection(self):
        try:
            return pyodbc.connect(
                r'DRIVER={SQL Server};'
                r'SERVER=DESKTOP-KDB6CJ2;'
                r'DATABASE=graceApp;'
                r'Trusted_Connection=yes;'
            )
        except pyodbc.Error as e:
            messagebox.showerror("Database Error", str(e))
            return None


    def show_donation(self):
        
        self.donor_window = tk.Toplevel(self.root)
        self.donor_window.title("Donor Registration")
        self.donor_window.geometry("400x300")

        ttk.Label(self.donor_window, text="Donor Registration Form", font=('Helvetica', 14)).pack(pady=10)

        form_frame = ttk.Frame(self.donor_window)
        form_frame.pack(padx=20, pady=10)

        ttk.Label(form_frame, text="Full Name:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.name_entry = ttk.Entry(form_frame, width=30)
        self.name_entry.grid(row=0, column=1, pady=5)

        ttk.Label(form_frame, text="Address:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.address_entry = ttk.Entry(form_frame, width=30)
        self.address_entry.grid(row=1, column=1, pady=5)

        ttk.Label(form_frame, text="Phone:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.phone_entry = ttk.Entry(form_frame, width=30)
        self.phone_entry.grid(row=2, column=1, pady=5)

        ttk.Label(form_frame, text="Email:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.email_entry = ttk.Entry(form_frame, width=30 ,)
        self.email_entry.grid(row=3, column=1, pady=5)

        button_frame = ttk.Frame(self.donor_window)
        button_frame.pack(pady=30)

        ttk.Button(button_frame, text="Back", command=self.donor_window.destroy).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Next", command=self.save_donor).pack(side=tk.LEFT, padx=5)





#------------------------------------------------------------------------------------------



    def save_donor(self):
        # Get form data
        name = self.name_entry.get()
        address = self.address_entry.get()
        phone = self.phone_entry.get()
        email = self.email_entry.get()

        # Basic validation
        if not all([name, address, phone, email]):
            messagebox.showerror("Error", "All fields are required!")
            return

        try:
            conn = self.db_connection()
            if conn:
                cursor = conn.cursor()
                
                # Insert into donor table only
                cursor.execute("""
                    INSERT INTO donors (full_name, address, phone, email)
                    VALUES (?, ?, ?, ?)
                """, (name, address, phone, email))
                
                conn.commit()
                messagebox.showinfo("Success", "Donor registered successfully!")
                self.donor_window.destroy()
                
                cursor.close()
                conn.close()
                
        except pyodbc.Error as e:
            messagebox.showerror("Database Error", f"Failed to save donor:\n{str(e)}")
        
        self.donor_data = (name, address, phone, email)
        
        self.donation_window = tk.Toplevel(self.root)
        self.donation_window.title("Donation Details")
        self.donation_window.geometry("400x350")
        
        ttk.Label(self.donation_window, text="Donation Details", font=('Helvetica', 14)).pack(pady=10)

        form_frame = ttk.Frame(self.donation_window)
        form_frame.pack(padx=20, pady=10)

        ttk.Label(form_frame, text="Country:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.country_var = tk.StringVar()
        country_combobox = ttk.Combobox(form_frame, textvariable=self.country_var, 
                                    values=["Debre Berhan", "Addis Ababa", "Debre Zeyit", "Dire Dawa"])
        country_combobox.grid(row=0, column=1, pady=5)

        # Charity Selection
        ttk.Label(form_frame, text="Charity:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.charity_var = tk.StringVar()
        charity_combobox = ttk.Combobox(form_frame, textvariable=self.charity_var,
                                    values=["Meqedonia", "Habesha Aregawi", "Refugees Support"])
        charity_combobox.grid(row=1, column=1, pady=5)

        # Food Item Selection
        ttk.Label(form_frame, text="Food Item:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.food_var = tk.StringVar()
        food_combobox = ttk.Combobox(form_frame, textvariable=self.food_var,
                                    values=["food"])
        food_combobox.grid(row=2, column=1, pady=5)

        # Hotel Selection
        ttk.Label(form_frame, text="Hotel:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.hotel_var = tk.StringVar()
        hotel_combobox = ttk.Combobox(form_frame, textvariable=self.hotel_var,
                                    values=["Janhoy Hotel", "Bernos Resort", "Sunshine Inn"])
        hotel_combobox.grid(row=3, column=1, pady=5)

        # Buttons
        button_frame = ttk.Frame(self.donation_window)
        button_frame.pack(pady=10)

        ttk.Button(button_frame, text="Back", command=self.donation_window.destroy).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Submit", command=self.save_donation).pack(side=tk.LEFT, padx=5)

    def save_donation(self):
        # Get selected values from donation form
        country = self.country_var.get()
        charity = self.charity_var.get()
        food_item = self.food_var.get()
        hotel = self.hotel_var.get()

        # Validate selections
        if not all([country, charity, food_item, hotel]):
            messagebox.showerror("Error", "All fields are required!")
            return

        # Create food donation window
        self.food_window = tk.Toplevel(self.root)
        self.food_window.title("Food Donation")
        self.food_window.geometry("400x300")

        # Food prices dictionary
        self.food_prices = {
            "Pasta": 80,
            "Tebs": 500,
            "Kitfo": 700,
            "Beyaynet": 80
        }

        # Create form elements
        ttk.Label(self.food_window, text="Food Donation Details", font=('Helvetica', 14)).pack(pady=10)

        form_frame = ttk.Frame(self.food_window)
        form_frame.pack(padx=20, pady=10)

        # Food Name Combobox
        ttk.Label(form_frame, text="Food Name:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.food_name_var = tk.StringVar()
        food_combobox = ttk.Combobox(form_frame, textvariable=self.food_name_var, 
                                values=list(self.food_prices.keys()))
        food_combobox.grid(row=0, column=1, pady=5)
        food_combobox.bind("<<ComboboxSelected>>", self.update_price)

        # Quantity Spinbox
        ttk.Label(form_frame, text="Quantity:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.quantity_var = tk.IntVar(value=1)
        spinbox = ttk.Spinbox(form_frame, from_=1, to=100, textvariable=self.quantity_var)
        spinbox.grid(row=1, column=1, pady=5)

        # Price Display
        ttk.Label(form_frame, text="Price:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.price_label = ttk.Label(form_frame, text="0.00")
        self.price_label.grid(row=2, column=1, pady=5)

        # Total Display
        ttk.Label(form_frame, text="Total:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.total_label = ttk.Label(form_frame, text="0.00")
        self.total_label.grid(row=3, column=1, pady=5)

        # Update total when quantity changes
        self.quantity_var.trace_add("write", self.update_total)

        # Buttons
        button_frame = ttk.Frame(self.food_window)
        button_frame.pack(pady=10)
        
        ttk.Button(button_frame, text="Back", command=self.food_window.destroy).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Donate", command=self.save_food).pack(side=tk.LEFT, padx=5)




    def update_price(self, event=None):
        selected_food = self.food_name_var.get()
        self.current_price = self.food_prices.get(selected_food, 0)
        self.price_label.config(text=f"{self.current_price:.2f}")
        self.update_total()

    def update_total(self, *args):
        quantity = self.quantity_var.get()
        total = quantity * self.current_price
        self.total_label.config(text=f"{total:.2f}")
        

    def save_food(self):
        food_name = self.food_name_var.get()
        quantity = self.quantity_var.get()
        
        if not food_name or quantity < 1:
            messagebox.showerror("Error", "Please select a food item and quantity")
            return

        # Store food data temporarily
        self.food_data = (food_name, quantity, self.current_price)
        
        # Create payment window
        self.payment_window = tk.Toplevel(self.root)
        self.payment_window.title("Payment Details")
        self.payment_window.geometry("400x400")

        # Create form elements
        ttk.Label(self.payment_window, text="Payment Information", font=('Helvetica', 14)).pack(pady=10)

        form_frame = ttk.Frame(self.payment_window)
        form_frame.pack(padx=20, pady=10)


        # Account Type
        ttk.Label(form_frame, text="Account Type:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.account_type_var = tk.StringVar()
        account_type_combobox = ttk.Combobox(form_frame, textvariable=self.account_type_var, 
                                        values=["CBE", "AWASH", "Abisinia"])
        account_type_combobox.grid(row=1, column=1, pady=5)
        
        # Account Number
        ttk.Label(form_frame, text="Account Number:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.account_entry = ttk.Entry(form_frame)
        self.account_entry.grid(row=0, column=1, pady=5)



        # PIN Number
        ttk.Label(form_frame, text="PIN Number:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.pin_entry = ttk.Entry(form_frame, show="*")
        self.pin_entry.grid(row=2, column=1, pady=5)

        # Checkboxes
        self.confirm_org_var = tk.IntVar()
        ttk.Checkbutton(form_frame, text="Send confirmation to organization", 
                    variable=self.confirm_org_var).grid(row=3, column=0, columnspan=2, pady=5, sticky=tk.W)

        self.confirm_charity_var = tk.IntVar()
        ttk.Checkbutton(form_frame, text="Send donation to charity", 
                    variable=self.confirm_charity_var).grid(row=4, column=0, columnspan=2, pady=5, sticky=tk.W)

        # Buttons
        button_frame = ttk.Frame(self.payment_window)
        button_frame.pack(pady=10)
        
        ttk.Button(button_frame, text="Back", command=self.payment_window.destroy).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Confirm", command=self.process_payment).pack(side=tk.LEFT, padx=5)

    def process_payment(self):
     
        account_no = self.account_entry.get()
        org_account_type = self.account_type_var.get()
        pin_number = self.pin_entry.get()
        confirm_org = self.confirm_org_var.get()
        confirm_charity = self.confirm_charity_var.get()

        
        if not all([account_no, org_account_type, pin_number]):
            messagebox.showerror("Error", "All payment fields are required!")
            return
        
        # Validate checkboxes
        if not (confirm_org and confirm_charity):
            messagebox.showerror("Error", "You must confirm both options!")
            return

        try:
            conn = self.db_connection()
            if conn:
                cursor = conn.cursor()
                
                 
                cursor.execute("""
                    INSERT INTO foodmenu (name, quantity, price, manager_id)
                    VALUES (?, ?, ?, ?)
                """, (*self.food_data, 1))
                
                cursor.execute("""
                    INSERT INTO payment (account_no, org_account_type, pin_number, donor_id, charity_id)
                    VALUES (?, ?, ?, ?, ?)
                """, (account_no, org_account_type, pin_number, 1, 1))  # Replace 1 with actual IDs
          
           
                
                conn.commit()
                messagebox.showinfo("Success", "Payment processed successfully!")
                self.payment_window.destroy()
                self.food_window.destroy()
                
                cursor.close()
                conn.close()
                
        except pyodbc.Error as e:
            messagebox.showerror("Database Error", f"Failed to process payment:\n{str(e)}")


   
   
              
    def show_receiver(self):
        # Create receiver registration window
        self.receiver_win = tk.Toplevel(self.root)
        self.receiver_win.title("Receiver Registration")
        self.receiver_win.geometry("400x300")
        
        # Form elements
        ttk.Label(self.receiver_win, text="Receiver Registration", font=('Helvetica', 14)).pack(pady=10)
        
        form_frame = ttk.Frame(self.receiver_win)
        form_frame.pack(padx=20, pady=10)

        # Name
        ttk.Label(form_frame, text="Full Name:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.rcv_name = ttk.Entry(form_frame)
        self.rcv_name.grid(row=0, column=1, pady=5)

        # Email
        ttk.Label(form_frame, text="Email:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.rcv_email = ttk.Entry(form_frame)
        self.rcv_email.grid(row=1, column=1, pady=5)

        # Password
        ttk.Label(form_frame, text="Password:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.rcv_pass = ttk.Entry(form_frame, show="*")
        self.rcv_pass.grid(row=2, column=1, pady=5)

        # Buttons
        btn_frame = ttk.Frame(self.receiver_win)
        btn_frame.pack(pady=10)
        ttk.Button(btn_frame, text="Register", command=self.save_receiver).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Back", command=self.receiver_win.destroy).pack(side=tk.LEFT, padx=5)

    def save_receiver(self):
        name = self.rcv_name.get()
        email = self.rcv_email.get()
        password = self.rcv_pass.get()

        if not all([name, email, password]):
            messagebox.showerror("Error", "All fields are required!")
            return

        try:
            conn = self.db_connection()
            cursor = conn.cursor()
            
            # Save to receiver table
            cursor.execute("""
                INSERT INTO receivers (name, email, password)
                VALUES (?, ?, ?)
            """, (name, email, password))
            
            conn.commit()
            receiver_id = cursor.execute("SELECT SCOPE_IDENTITY()").fetchone()[0]
            
            # Show donation details
            self.show_receiver_donations(receiver_id)
            self.receiver_win.destroy()
            
            cursor.close()
            conn.close()
            
        except pyodbc.Error as e:
            messagebox.showerror("Database Error", str(e))

    def show_receiver_donations(self, receiver_id):
        dashboard = tk.Toplevel(self.root)
        dashboard.title("Receiver Dashboard")
        dashboard.geometry("800x500")
        
        # Charity name input
        ttk.Label(dashboard, text="Associated Charity:").pack(pady=5)
        self.charity_name = ttk.Entry(dashboard)
        self.charity_name.pack(pady=5)
        
        # Donation details treeview
        columns = ("Food Item", "Quantity", "Price", "Payment Method")
        self.donation_tree = ttk.Treeview(dashboard, columns=columns, show="headings")
        
        for col in columns:
            self.donation_tree.heading(col, text=col)
            self.donation_tree.column(col, width=150)
        
        self.donation_tree.pack(pady=10, padx=10, fill='both', expand=True)
        
        # Load existing donations
        try:
            conn = self.db_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT f.name, f.quantity, f.price, p.org_account_type 
                FROM donation d
                JOIN foodmenu f ON d.food_id = f.food_id
                JOIN payment p ON d.payment_id = p.payment_id
                WHERE d.receiver_id = ?
            """, (receiver_id,))
            
            for row in cursor.fetchall():
                self.donation_tree.insert("", tk.END, values=row)
                
            cursor.close()
            conn.close()
            
        except pyodbc.Error as e:
            messagebox.showerror("Database Error", str(e))
        
        # Refresh button
        ttk.Button(dashboard, text="Refresh", 
                command=lambda: self.load_donations(receiver_id)).pack(pady=5)

    def load_donations(self, receiver_id):
        self.donation_tree.delete(*self.donation_tree.get_children())
        
        try:
            conn = self.db_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT f.name, f.quantity, f.price, p.org_account_type 
                FROM donation d
                JOIN foodmenu f ON d.food_id = f.food_id
                JOIN payment p ON d.payment_id = p.payment_id
                WHERE d.receiver_id = ?
            """, (receiver_id,))
            
            for row in cursor.fetchall():
                self.donation_tree.insert("", tk.END, values=row)
                
            cursor.close()
            conn.close()
            
        except pyodbc.Error as e:
            messagebox.showerror("Database Error", str(e))
            
                        

    def show_manager(self):
        # Manager registration window
        self.manager_win = tk.Toplevel(self.root)
        self.manager_win.title("Manager Portal")
        self.manager_win.geometry("400x300")
        
        # Form elements
        ttk.Label(self.manager_win, text="Manager Registration", font=('Helvetica', 14)).pack(pady=10)
        
        form_frame = ttk.Frame(self.manager_win)
        form_frame.pack(padx=20, pady=10)

        # Name
        ttk.Label(form_frame, text="Full Name:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.mgr_name = ttk.Entry(form_frame)
        self.mgr_name.grid(row=0, column=1, pady=5)

        # Username
        ttk.Label(form_frame, text="Username:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.mgr_user = ttk.Entry(form_frame)
        self.mgr_user.grid(row=1, column=1, pady=5)

        # Password
        ttk.Label(form_frame, text="Password:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.mgr_pass = ttk.Entry(form_frame, show="*")
        self.mgr_pass.grid(row=2, column=1, pady=5)

        # Buttons
        btn_frame = ttk.Frame(self.manager_win)
        btn_frame.pack(pady=10)
        ttk.Button(btn_frame, text="Login", command=self.save_manager).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Back", command=self.manager_win.destroy).pack(side=tk.LEFT, padx=5)

    def save_manager(self):
        name = self.mgr_name.get()
        username = self.mgr_user.get()
        password = self.mgr_pass.get()

        if not all([name, username, password]):
            messagebox.showerror("Error", "All fields are required!")
            return

        try:
            conn = self.db_connection()
            cursor = conn.cursor()
            
            # Save to manager table
            cursor.execute("""
                INSERT INTO managers (name, username, password)
                VALUES (?, ?, ?)
            """, (name, username, password))
            
            conn.commit()
            manager_id = cursor.execute("SELECT SCOPE_IDENTITY()").fetchone()[0]
            
            # Show food management dashboard
            self.show_food_dashboard(manager_id)
            self.manager_win.destroy()
            
            cursor.close()
            conn.close()
            
        except pyodbc.Error as e:
            messagebox.showerror("Database Error", str(e))
            

    def show_food_dashboard(self, manager_id):
        dashboard = tk.Toplevel(self.root)
        dashboard.title("Food Management")
        dashboard.geometry("800x500")
        
        # Food list
        columns = ("ID", "Food Name", "Quantity", "Price")
        self.food_tree = ttk.Treeview(dashboard, columns=columns, show="headings")
        
        for col in columns:
            self.food_tree.heading(col, text=col)
            self.food_tree.column(col, width=120)
        
        self.food_tree.pack(pady=10, padx=10, fill='both', expand=True)
        
        # Action buttons
        btn_frame = ttk.Frame(dashboard)
        btn_frame.pack(pady=10)
        
        ttk.Button(btn_frame, text="Add New", command=lambda: self.add_food_form(manager_id)).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Update", command=lambda: self.update_food_form(manager_id)).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Refresh", command=lambda: self.load_foods(manager_id)).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Back", command=dashboard.destroy).pack(side=tk.LEFT, padx=5)
        
        # Load initial data
        self.load_foods(manager_id)

    def load_foods(self, manager_id):
        self.food_tree.delete(*self.food_tree.get_children())
        try:
            conn = self.db_connection()
            cursor = conn.cursor()
            
            cursor.execute("SELECT food_id, name, quantity, price FROM foodmenu WHERE manager_id=?", manager_id)
            
            for row in cursor.fetchall():
                self.food_tree.insert("", tk.END, values=row)
                
            cursor.close()
            conn.close()
            
        except pyodbc.Error as e:
            messagebox.showerror("Database Error", str(e))

    def add_food_form(self, manager_id):
        add_win = tk.Toplevel(self.root)
        add_win.title("Add New Food Item")
        
        # Form elements
        ttk.Label(add_win, text="Food Name:").grid(row=0, column=0, padx=5, pady=5)
        food_name = ttk.Entry(add_win)
        food_name.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(add_win, text="Quantity:").grid(row=1, column=0, padx=5, pady=5)
        quantity = ttk.Spinbox(add_win, from_=1, to=1000)
        quantity.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(add_win, text="Price:").grid(row=2, column=0, padx=5, pady=5)
        price = ttk.Entry(add_win)
        price.grid(row=2, column=1, padx=5, pady=5)
        
        def save_food():
            try:
                conn = self.db_connection()
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO foodmenu (name, quantity, price, manager_id)
                    VALUES (?, ?, ?, ?)
                """, (food_name.get(), quantity.get(), price.get(), manager_id))
                conn.commit()
                self.load_foods(manager_id)
                add_win.destroy()
            except pyodbc.Error as e:
                messagebox.showerror("Database Error", str(e))
            finally:
                conn.close()
        
            ttk.Button(add_win, text="Save", command=save_food).grid(row=3, columnspan=2, pady=10)

    def update_food_form(self, manager_id):
        selected = self.food_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a food item to update")
            return
        
        item = self.food_tree.item(selected[0])
        food_id, name, qty, price = item['values']
        
        update_win = tk.Toplevel(self.root)
        update_win.title("Update Food Item")
        
        # Form elements with existing values
        ttk.Label(update_win, text="Food Name:").grid(row=0, column=0, padx=5, pady=5)
        food_name = ttk.Entry(update_win)
        food_name.insert(0, name)
        food_name.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(update_win, text="Quantity:").grid(row=1, column=0, padx=5, pady=5)
        quantity = ttk.Spinbox(update_win, from_=1, to=1000)
        quantity.set(qty)
        quantity.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(update_win, text="Price:").grid(row=2, column=0, padx=5, pady=5)
        price_entry = ttk.Entry(update_win)
        price_entry.insert(0, price)
        price_entry.grid(row=2, column=1, padx=5, pady=5)
        
        def update_food():
            try:
                conn = self.db_connection()
                cursor = conn.cursor()
                cursor.execute("""
                    UPDATE foodmenu 
                    SET name=?, quantity=?, price=?
                    WHERE food_id=? AND manager_id=?
                """, (food_name.get(), quantity.get(), price_entry.get(), food_id, manager_id))
                conn.commit()
                self.load_foods(manager_id)
                update_win.destroy()
            except pyodbc.Error as e:
                messagebox.showerror("Database Error", str(e))
            finally:
                conn.close()
        
        ttk.Button(update_win, text="Update", command=update_food).grid(row=3, columnspan=2, pady=10)            
            
            
            

    def show_charity(self):
        # Charity registration window
        self.charity_win = tk.Toplevel(self.root)
        self.charity_win.title("Charity Registration")
        self.charity_win.geometry("400x250")
        
        # Form elements
        ttk.Label(self.charity_win, text="Charity Registration", font=('Helvetica', 14)).pack(pady=10)
        
        form_frame = ttk.Frame(self.charity_win)
        form_frame.pack(padx=20, pady=10)

        # Charity Name
        ttk.Label(form_frame, text="Charity Name:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.charity_name_entry = ttk.Entry(form_frame)
        self.charity_name_entry.grid(row=0, column=1, pady=5)

        # Password
        ttk.Label(form_frame, text="Password:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.charity_pass_entry = ttk.Entry(form_frame, show="*")
        self.charity_pass_entry.grid(row=1, column=1, pady=5)

        # Buttons
        btn_frame = ttk.Frame(self.charity_win)
        btn_frame.pack(pady=10)
        ttk.Button(btn_frame, text="Next", command=self.save_charity).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Cancel", command=self.charity_win.destroy).pack(side=tk.LEFT, padx=5)




    def save_charity(self):
        charity_name = self.charity_name_entry.get()
        password = self.charity_pass_entry.get()

        if not all([charity_name, password]):
            messagebox.showerror("Error", "All fields are required!")
            return

        try:
            conn = self.db_connection()
            cursor = conn.cursor()
            
            # Save to charity table
            cursor.execute("""
                INSERT INTO charity (charity_name, password)
                VALUES (?, ?)
            """, (charity_name, password))
            
            conn.commit()
            charity_id = cursor.execute("SELECT SCOPE_IDENTITY()").fetchone()[0]
            
            # Show charity dashboard
            self.show_charity_dashboard(charity_id)
            self.charity_win.destroy()
            
            cursor.close()
            conn.close()
            
        except pyodbc.Error as e:
            messagebox.showerror("Database Error", str(e))


    def show_charity_dashboard(self, charity_id):
        dashboard = tk.Toplevel(self.root)
        dashboard.title("Charity Dashboard")
        dashboard.geometry("800x500")
        
        # Dashboard content
        ttk.Label(dashboard, text="Donation Details", font=('Helvetica', 14)).pack(pady=10)
        
        # Treeview for donations
        columns = ("Donor Email", "Food Item", "Quantity")
        donation_tree = ttk.Treeview(dashboard, columns=columns, show="headings")
        
        for col in columns:
            donation_tree.heading(col, text=col)
            donation_tree.column(col, width=150)
        
        donation_tree.pack(pady=10, padx=10, fill='both', expand=True)
        

        try:
            conn = self.db_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT d.email, f.name, f.quantity 
                FROM donation dn
                JOIN donor d ON dn.donor_id = d.donor_id
                JOIN foodmenu f ON dn.food_id = f.food_id
                WHERE dn.charity_id = ?
            """, (charity_id,))
            
            for row in cursor.fetchall():
                donation_tree.insert("", tk.END, values=row)
                
            cursor.close()
            conn.close()
            
        except pyodbc.Error as e:
            messagebox.showerror("Database Error", str(e))
        
        # Back button
        ttk.Button(dashboard, text="Back to Home", command=dashboard.destroy).pack(pady=10)


if __name__ == "__main__":
    root = tk.Tk()
    app = CharityApp(root)
    root.mainloop()
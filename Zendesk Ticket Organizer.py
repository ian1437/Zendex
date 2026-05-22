# Zendesk Ticket Organizer

import sqlite3 as sql
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkcalendar import DateEntry

class ZendexGUI:
    def __init__(self, main):
        # Main t.window
        self.root = main
        self.root.title("Tickets")
        self.root.geometry("600x500")
        
        # Ticket init with vars
        self.tickets = ttk.Frame(main)
        self.tickets.pack()
        
        self.tict_dict = {
            'Open': [],
            'Onboard': [],
            'Install': [],
            'Scheduled': [],
            'Complete': []
        }

        # Ticket entry vars
        self.e_handoff_id = StringVar()
        self.e_full_name = StringVar()        
        self.e_b_name = StringVar()        
        self.e_phone = StringVar()
        self.e_email = StringVar()
        self.e_ord_num = StringVar()        
        self.e_shipping = StringVar()
        self.e_shipping.set("Not Sent")
        self.e_cs_req = StringVar()
        self.e_ticket_status = StringVar()
        self.e_ticket_status.set("Open")
        self.e_manage_acc = StringVar()
        self.add_new = False
        self.selected_ticket = None
        self.selected_listbox = None

        # Add buttons
        self.add = ttk.Button(self.tickets, text="New Ticket", command=self.new_tic)
        self.add.grid(row=0, column=0, padx=5, pady=5)

        self.add_install = ttk.Button(self.tickets,text="Install Ticket", command=self.new_install_ticket)
        self.add_install.grid(row=0, column=1, padx=5, pady=5)
                
        # Tabs style
        style = ttk.Style()
        style.configure("TNotebook.Tab", padding=[40, 0], font=("Arial", 10))
        
        # Building tabs to differentiate the ticket status
        self.notebook = ttk.Notebook(main)

        self.orders = ttk.Frame(self.notebook)
        self.oboard = ttk.Frame(self.notebook)
        self.install = ttk.Frame(self.notebook)
        self.sched = ttk.Frame(self.notebook)
        self.complete = ttk.Frame(self.notebook)
        
        self.notebook.add(self.orders, text ="Open tickets")
        self.notebook.add(self.oboard, text = "Onboarding")
        self.notebook.add(self.install, text = "Install")    
        self.notebook.add(self.sched, text = "Scheduled")
        self.notebook.add(self.complete, text = "Complete")
        self.notebook.pack(fill="both", expand=True)
        
        # 
        self.open_ticket_list = self.build_ticket_tab(self.orders)
        self.onboard_ticket_list = self.build_ticket_tab(self.oboard)
        self.install_ticket_list = self.build_install_tab(self.install)
        self.scheduled_ticket_list = self.build_install_tab(self.sched)
        self.complete_ticket_list = self.build_ticket_tab(self.complete)

        self.ticket_lists = {
            "Open": self.open_ticket_list,
            "Onboard": self.onboard_ticket_list,
            "Install": self.install_ticket_list,
            "Scheduled": self.scheduled_ticket_list,
            "Complete": self.complete_ticket_list
        }

        self.open_ticket_list.table_type = "handoff"
        self.onboard_ticket_list.table_type = "handoff"
        self.complete_ticket_list.table_type = "handoff"
        self.install_ticket_list.table_type = "install"
        self.scheduled_ticket_list.table_type = "install"

        self.load_tickets()    
  
    def delete_ticket(self):
        if self.selected_ticket is None:
            return

        confirm = messagebox.askyesno(
            title="Delete Ticket",
            message="Delete this ticket?"
        )

        if not confirm:
            return

        db_conn = sql.connect('PR_Tickets.db')
        cx = db_conn.cursor()

        cx.execute(
            "DELETE FROM handoff_tickets WHERE handoff_id = ?",
            (self.selected_ticket,)
        )

        db_conn.commit()
        db_conn.close()

        selected_index = self.selected_listbox.curselection()

        if selected_index:
            self.selected_listbox.delete(selected_index[0])

        self.selected_ticket = None
        self.selected_listbox = None

        messagebox.showinfo(
            title="Deleted",
            message="Ticket deleted successfully."
        )

    def build_ticket_tab(self, tab):
    
    # Main self.container inside each notebook tab
        self.container = ttk.Frame(tab)
        self.container.pack(fill="both", expand=True, padx=10, pady=10)

        # Left ticket list area
        self.left_frame = ttk.Frame(self.container, width=120)
        self.left_frame.pack(side="left", fill="y", padx=(0, 10))

        self.ticket_label = ttk.Label(self.left_frame, text="Ticket #")
        self.ticket_label.pack(pady=5)

        self.ticket_list = Listbox(self.left_frame, width=15)
        self.ticket_list.pack(fill="y", expand=True)
        self.ticket_list.bind("<<ListboxSelect>>", self.show_handoff_info)

        # Right ticket info area
        self.right_frame = ttk.Frame(self.container)
        self.right_frame.pack(side="left", fill="both", expand=True)

        details_frame = ttk.LabelFrame(self.right_frame, text="Ticket Details")
        details_frame.pack(pady=10, padx=20, fill="x")

        handoff_vars = {
            "full_name": StringVar(),
            "b_name": StringVar(),
            "email": StringVar(),
            "phone": StringVar(),
            "ord_num": StringVar(),
            "manage_acc": StringVar()
        }

        labels = {
            "full_name": "Name",
            "b_name": "Business",
            "email": "Email",
            "phone": "Phone",
            "ord_num": "Ord #",
            "manage_acc": "Manage #"
        }

        row = 0
        for key, label_text in labels.items():
            ttk.Label(details_frame, text=label_text).grid(row=row, column=0, sticky="w", padx=5, pady=3)
            entry = ttk.Entry(details_frame, textvariable=handoff_vars[key], width=35)
            entry.grid(row=row, column=1, padx=5, pady=3)

            row += 1

        self.ticket_list.handoff_vars = handoff_vars
        
        ttk.Label(details_frame, text="Ticket Status").grid(row=0, column=3, padx=10, pady=5)
        status_var = StringVar(value="Install")
        self.status_menu = ttk.OptionMenu(details_frame, status_var, "Install", "Install", "Scheduled", "Complete")
        self.status_menu.grid(row=0, column=4, padx=10, pady=10)
        self.ticket_list.status_var = status_var 
        
        ttk.Label(details_frame, text="Shipped Status").grid(row=1, column=3, padx=10, pady=5)
        shipping_var = StringVar(value="Not Sent")
        self.shipping_status = ttk.OptionMenu(
            details_frame,
            shipping_var,
            "Not Sent",
            "Not Sent",
            "Ready to Ship",
            "Complete"
        )
        self.shipping_status.grid(row=1, column=4, padx=10, pady=5)
        self.ticket_list.shipping_var = shipping_var

        ttk.Label(details_frame, text="CS Action").grid(row=2, column=3, padx=10, pady=5)
        cs_var = StringVar(value="")
        self.cs_action = ttk.OptionMenu(
            details_frame,
            cs_var, 
            "", "", "Onboard Only", "Install Only","Onboard + Install", "No Onboard + No Install")
        
        self.cs_action.grid(row=2, column=4, padx=10, pady=5)
        self.ticket_list.cs_var = cs_var

        status_var = StringVar(value="Open")
        self.status_menu = ttk.OptionMenu(details_frame, status_var, "Open", "Open", "Onboard", "Complete")
        self.status_menu.grid(row=3, column=4, padx=10, pady=5)
        self.ticket_list.status_var = status_var
      
      # Shipping / CS section
        self.action_frame = LabelFrame(self.right_frame, text="Notes", bd=0)
        self.action_frame.pack()
        self.notes_box = Text(self.action_frame, height=4, width=30)
        self.notes_box.grid(row=0, rowspan = 4, column= 2, columnspan=2, padx=10, pady=10)
        
        # Status section
        self.status_frame = ttk.Frame(self.right_frame)
        self.status_frame.pack(expand=True)
        delete_button = ttk.Button(self.status_frame, text="Delete Ticket", command=self.delete_ticket)
        delete_button.grid(row =0, column=0, pady=10)

        update_button = ttk.Button(self.status_frame, text="Update Ticket", command=self.update_handoff)
        update_button.grid(row = 0, column=1, pady=10)
        
        return self.ticket_list
    
    def build_install_tab(self, tab):
        
        # Main self.container inside each notebook tab
        self.container = ttk.Frame(tab)
        self.container.pack(fill="both", expand=True, padx=10, pady=10)

        # Left ticket list area
        self.left_frame = ttk.Frame(self.container, width=120)
        self.left_frame.pack(side="left", fill="y", padx=(0, 10))

        self.ticket_label = ttk.Label(self.left_frame, text="Ticket #")
        self.ticket_label.pack(pady=5)

        self.ticket_list = Listbox(self.left_frame, width=15)
        self.ticket_list.pack(fill="y", expand=True)
        self.ticket_list.bind("<<ListboxSelect>>", self.show_install_info)

        # Right ticket info area
        self.right_frame = ttk.Frame(self.container)
        self.right_frame.pack(side="left", fill="both", expand=True)

        details_frame = ttk.LabelFrame(self.right_frame, text="Install Details")
        details_frame.pack(pady=10, padx=20, fill="x")

        install_vars = {
            "install_id": StringVar(),
            "tech_name": StringVar(),
            "work_ord_num": StringVar(),
            "tracking_number": StringVar()
            }

        labels = {
            "install_id": "Install Ticket",
            "tech_name": "Technician",
            "work_ord_num": "WO #",
            "tracking_number": "Tracking Number"
        }
        
        ttk.Label(details_frame, text="Handoff ID").grid(row=0, column=0, sticky="w", padx=5, pady=3)
        handoff_button_var = StringVar(value = "No ID Selected")
        handoff_button = ttk.Button(details_frame, textvariable= handoff_button_var, command=self.show_handoff_details)
        handoff_button.grid(row=0, column=1, padx=5, pady=3)
        self.ticket_list.handoff_button_var = handoff_button_var

        row = 1
        for key, label_text in labels.items():
            ttk.Label(details_frame, text=label_text).grid(row=row, column=0, sticky="w", padx=5, pady=3)
            entry = ttk.Entry(details_frame, textvariable=install_vars[key], width=35)
            entry.grid(row=row, column=1, padx=5, pady=3)
            row += 1
        
        self.ticket_list.install_vars = install_vars
        
        ttk.Label(details_frame, text="Install Date").grid(row=row, column=0, sticky="w", padx=5, pady=3)
        install_date = DateEntry(details_frame, width=27, state = "normal", date_pattern="yyyy-mm-dd")
        install_date.grid(row=row, column=1, padx=10, pady=5)
        self.ticket_list.install_date_widget = install_date
        
        ttk.Label(details_frame, text="Ticket Status").grid(row=0, column=3, padx=10, pady=5)
        status_var = StringVar(value="Install")
        self.status_menu = ttk.OptionMenu(details_frame, status_var, "Install", "Install", "Scheduled", "Complete")
        self.status_menu.grid(row=0, column=4, padx=10, pady=10)
        self.ticket_list.status_var = status_var

        ttk.Label(details_frame, text="Install Company").grid(row=1, column=3, padx=10, pady=5)
        company_var = StringVar(value="")
        self.shipping_status = ttk.OptionMenu(details_frame, company_var, "", "", "TL", "TSP")
        self.shipping_status.grid(row=1, column=4, padx=10, pady=5)
        self.ticket_list.company_var = company_var
                
        ttk.Label(details_frame, text="Tech Account").grid(row=2, column=3, padx=10, pady=5)
        admin_var = StringVar(value="")
        self.shipping_status = ttk.OptionMenu(details_frame, admin_var, "", "", "Create", "Added", "Deleted")
        self.shipping_status.grid(row=2, column=4, padx=10, pady=5)
        self.ticket_list.admin_var = admin_var
       
        ttk.Label(details_frame, text="Install Status").grid(row=3, column=3, padx=10, pady=5)
        installation_var = StringVar(value="")
        self.shipping_status = ttk.OptionMenu(details_frame, installation_var, "", "", "RMA", "Scheduled", "Completed")
        self.shipping_status.grid(row=3, column=4, padx=10, pady=5)
        self.ticket_list.installation_var = installation_var

        ttk.Label(details_frame, text="QC Status").grid(row=4, column=3, padx=10, pady=5)
        qc_var = StringVar(value="")
        self.shipping_status = ttk.OptionMenu(details_frame, qc_var, "", "", "Pending", "Pass", "Fail")
        self.shipping_status.grid(row=4, column=4, padx=10, pady=5)
        self.ticket_list.qc_var = qc_var

        # Shipping / CS section
        self.action_frame = LabelFrame(self.right_frame, text="Notes", bd=0)
        self.action_frame.pack()
        self.notes_box = Text(self.action_frame, height=4, width=30)
        self.notes_box.grid(row=0, rowspan = 4, column= 2, columnspan=2, padx=10, pady=10)
        
        # Status section
        self.status_frame = ttk.Frame(self.right_frame)
        self.status_frame.pack(expand=True)
        delete_button = ttk.Button(self.status_frame, text="Delete Ticket", command=self.delete_ticket)
        delete_button.grid(row =0, column=0, pady=10)

        update_button = ttk.Button(self.status_frame, text="Update Ticket", command=self.update_handoff)
        update_button.grid(row = 0, column=1, pady=10)
        
        return self.ticket_list   
    
    def load_tickets(self):
        db_conn = sql.connect('PR_Tickets.db')
        cx = db_conn.cursor()

        # Load handoff tickets
        cx.execute("""
            SELECT handoff_id, ticket_status
            FROM handoff_tickets
            WHERE ticket_status IN ('Open', 'Onboard', 'Complete')
        """)

        handoff_records = cx.fetchall()

        for handoff_id, status in handoff_records:
            if status in self.ticket_lists:
                self.ticket_lists[status].insert(END, str(handoff_id))

        # Load install tickets
        cx.execute("""
            SELECT install_id, install_complete, qc_complete
            FROM install_tickets
        """)

        install_records = cx.fetchall()

        for install_id, install_complete, qc_complete in install_records:
            if install_complete != "Complete":
                self.ticket_lists["Install"].insert(END, str(install_id))
            elif qc_complete != "Complete":
                self.ticket_lists["Scheduled"].insert(END, str(install_id))

        db_conn.close()

    def new_tic(self): # Creating new ticket
        if self.add_new != False:
            self.add_new.destroy()

        # Creates a new ticket window
        self.add_new = Toplevel(self.root) 
        self.add_new.geometry("300x300")
        self.entry = ttk.Frame(self.add_new)
        self.entry.grid()  
        
        # New ticket entry boxes 
        self.handoff_id = ttk.Entry(self.add_new, width = 30)
        self.handoff_id.grid(row = 0, column = 1, padx = 10)
        self.handoff_id_label = ttk.Label(self.add_new, text = "Ticket ID")
        self.handoff_id_label.grid(row = 0, column = 0, padx = 10)

        self.full_name = ttk.Entry(self.add_new, width = 30)
        self.full_name.grid(row = 1, column = 1, padx = 10)
        self.full_name_label = ttk.Label(self.add_new, text = "Full Name")
        self.full_name_label.grid(row = 1, column = 0, padx = 10)

        self.b_name = ttk.Entry(self.add_new, width = 30)
        self.b_name.grid(row = 2, column = 1, padx = 10)
        self.b_name_label = ttk.Label(self.add_new, text = "Business Name")
        self.b_name_label.grid(row = 2, column = 0, padx = 10)

        self.phone = ttk.Entry(self.add_new, width = 30)
        self.phone.grid(row = 3, column = 1, padx = 10)
        self.phone_label = ttk.Label(self.add_new, text = "Phone Number")
        self.phone_label.grid(row = 3, column = 0, padx = 10)

        self.email = ttk.Entry(self.add_new, width = 30)
        self.email.grid(row = 4, column = 1, padx = 10)
        self.email_label = ttk.Label(self.add_new, text = "Email Address")
        self.email_label.grid(row = 4, column = 0, padx = 10)

        self.ord_num = ttk.Entry(self.add_new, width = 30)
        self.ord_num.grid(row = 5, column = 1, padx = 10)
        self.ord_num_label = ttk.Label(self.add_new, text = "ORD Number")
        self.ord_num_label.grid(row = 5, column = 0, padx = 10)

        self.shipping = OptionMenu(self.add_new, self.e_shipping,"Not Sent","Ready to Ship", \
                                   "Complete")
        self.shipping.grid(row = 6, column = 1, padx = 10)
        self.shipping_label = ttk.Label(self.add_new, text = "Shipped Status")
        self.shipping_label.grid(row = 6, column = 0, padx = 10)

        self.cs_req = OptionMenu(self.add_new, self.e_cs_req, "Onboard Only", "Install Only", \
                                 "Onboard + Install", "No Onboard + No Install")
        self.cs_req.grid(row = 7, column = 1, padx = 10)
        self.cs_req_label = ttk.Label(self.add_new, text = "CS Action")
        self.cs_req_label.grid(row = 7, column = 0, padx = 10)

        self.manage_acc = ttk.Entry(self.add_new, width = 30)
        self.manage_acc.grid(row = 8, column = 1, padx = 10)
        self.manage_acc_label = ttk.Label(self.add_new, text = "Manage Accout")
        self.manage_acc_label.grid(row = 8, column = 0, padx = 10)        
        
        self.ticket_status = OptionMenu(self.add_new, self.e_ticket_status, "Open", "Onboard", \
                                 "Install", "Scheduled", "Complete")
        self.ticket_status.grid(row = 9, column = 1, padx = 10)
        self.ticket_status_label = ttk.Label(self.add_new, text = "Status")
        self.ticket_status_label.grid(row = 9, column = 0, padx = 10)

        self.submit_new = ttk.Button(self.add_new, text = "Add Ticket", command = self.submit_ticket)
        self.submit_new.grid(row = 10, column = 1, columnspan = 1, pady = 10, padx = 10)
        self.clear_new = ttk.Button(self.add_new, text = "Clear", command = self.clear_text)
        self.clear_new.grid(row = 10, column = 0, columnspan = 1, pady = 10, padx = 10)
    
    def show_handoff_info(self, event):
        if not event.widget.curselection():
            return

        selected_ticket = event.widget.get(event.widget.curselection()[0])

        self.selected_ticket = selected_ticket
        self.selected_listbox = event.widget
        
        db_conn = sql.connect('PR_Tickets.db')
        cx = db_conn.cursor()

        cx.execute("""
            SELECT full_name, b_name, email, phone, ord_num, shipping, cs_req, ticket_status, manage_acc 
                   FROM handoff_tickets WHERE handoff_id = ?""", (selected_ticket,))

        record = cx.fetchone()
        db_conn.close()

        if record:
            full_name, b_name, email, phone, ord_num, shipping, cs_req, ticket_status, manage_acc = record

            event.widget.handoff_vars["full_name"].set(full_name)
            event.widget.handoff_vars["b_name"].set(b_name)
            event.widget.handoff_vars["email"].set(email)
            event.widget.handoff_vars["phone"].set(phone)
            event.widget.handoff_vars["ord_num"].set(ord_num)
            event.widget.handoff_vars["manage_acc"].set(manage_acc)
            event.widget.shipping_var.set(shipping)
            event.widget.cs_var.set(cs_req)
            event.widget.status_var.set(ticket_status)

    def show_install_info(self, event):
        if not event.widget.curselection():
            return

        selected_ticket = event.widget.get(event.widget.curselection()[0])

        self.selected_ticket = selected_ticket
        self.selected_listbox = event.widget
        
        db_conn = sql.connect('PR_Tickets.db')
        cx = db_conn.cursor()

        cx.execute("""SELECT install_id, handoff_id, install_company, install_date, tech_name, tech_on_admin, work_ord_num, install_complete,
                   qc_complete, tracking_number FROM install_tickets WHERE install_id = ?""", (selected_ticket,))

        record = cx.fetchone()
        db_conn.close()

        if record:
            install_id, handoff_id, install_company, install_date, tech_name, tech_on_admin, work_ord_num, \
                install_complete, qc_complete, tracking_number = record

            if install_date:
                event.widget.install_date_widget.set_date(install_date)
            else:
                event.widget.install_date_widget.delete(0, END)    
            event.widget.handoff_button_var.set(str(handoff_id))
            event.widget.install_vars["install_id"].set(install_id)
            event.widget.install_vars["tech_name"].set(tech_name)
            event.widget.install_vars["work_ord_num"].set(work_ord_num)
            event.widget.install_vars["tracking_number"].set(tracking_number)
            event.widget.company_var.set(install_company)
            event.widget.admin_var.set(tech_on_admin)
            event.widget.installation_var.set(install_complete)
            event.widget.qc_var.set(qc_complete)
 
    def show_handoff_details(self):
        handoff_id_value = self.selected_listbox.handoff_button_var.get()
        self.install_window = Toplevel(self.root)
        self.install_window.title("Handoff Details")
        self.install_window.geometry("350x350")
        
        db_conn = sql.connect('PR_Tickets.db')
        cx = db_conn.cursor()

        cx.execute("""
            SELECT handoff_id, full_name, b_name, phone, email, ord_num, manage_acc
            FROM handoff_tickets
            WHERE handoff_id = ?
        """, (handoff_id_value,))

        record = cx.fetchone()
        db_conn.close()

        if not record:
            return

        handoff_id, full_name, b_name, phone, email, ord_num, manage_acc = record

        fields = {
            "Handoff_id": handoff_id,
            "Full Name": full_name,
            "Business": b_name,
            "Phone": phone,
            "Email": email,
            "ORD #": ord_num,
            "Manage #": manage_acc
        }

        row = 0
        for label, value in fields.items():
            ttk.Label(self.install_window, text=label).grid(row=row, column=0, padx=10, pady=5, sticky="w")
            entry = ttk.Entry(self.install_window, width=30)
            entry.grid(row=row, column=1, padx=10, pady=5)
            entry.insert(0, value)
            entry.config(state="readonly")

            row += 1
   
    def submit_ticket(self):
        db_conn = sql.connect('PR_Tickets.db')
        cx = db_conn.cursor()

        cx.execute("""INSERT INTO handoff_tickets VALUES 
            (:handoff_id, :full_name, :b_name, :phone, :email, :ord_num,
            :e_shipping, :e_cs_req, :e_ticket_status, :manage_acc)""",
            {
                'handoff_id': self.handoff_id.get(),
                'full_name': self.full_name.get(),
                'b_name': self.b_name.get(),
                'phone': self.phone.get(),
                'email': self.email.get(),
                'ord_num': self.ord_num.get(),
                'e_shipping': self.e_shipping.get(),
                'e_cs_req': self.e_cs_req.get(),
                'e_ticket_status': self.e_ticket_status.get(),
                'manage_acc': self.manage_acc.get()
            }
        )

        db_conn.commit()
        db_conn.close()

        status = self.e_ticket_status.get()
        ticket_text = str(self.handoff_id.get())

        if status in self.ticket_lists:
            self.ticket_lists[status].insert(END, ticket_text)

        self.clear_text()

    def update_handoff(self):
        if self.selected_ticket is None:
            return
        old_listbox = self.selected_listbox
        handoff_vars = self.selected_listbox.handoff_vars

        full_name = handoff_vars["full_name"].get()
        b_name = handoff_vars["b_name"].get()
        email = handoff_vars["email"].get()
        phone = handoff_vars["phone"].get()
        ord_num = handoff_vars["ord_num"].get()
        manage_acc = handoff_vars["manage_acc"].get()
        shipping = self.selected_listbox.shipping_var.get()
        cs_req = self.selected_listbox.cs_var.get()
        ticket_status = self.selected_listbox.status_var.get()
        db_conn = sql.connect('PR_Tickets.db')
        cx = db_conn.cursor()

        cx.execute("""
            UPDATE handoff_tickets
            SET full_name = ?,
                b_name = ?,
                email = ?,
                phone = ?,
                ord_num = ?,
                shipping = ?,
                cs_req = ?,
                ticket_status = ?,
                manage_acc = ?
            WHERE handoff_id = ?
        """, (
            full_name,
            b_name,
            email,
            phone,
            ord_num,
            shipping,
            cs_req,
            ticket_status,
            manage_acc,
            self.selected_ticket
        ))

        db_conn.commit()
        db_conn.close()
        
        current_index = self.selected_listbox.curselection()

        new_listbox = self.ticket_lists[ticket_status]

        if old_listbox != new_listbox:
            current_index = old_listbox.curselection()

            if current_index:
                old_listbox.delete(current_index[0])

            new_listbox.insert(END, self.selected_ticket)

            self.selected_listbox = new_listbox

        messagebox.showinfo(
            title="Updated",
            message="Ticket updated successfully."
        )

    def update_install(self):
            if self.selected_ticket is None:
                return
            old_listbox = self.selected_listbox
            handoff_vars = self.selected_listbox.handoff_vars

            full_name = handoff_vars["full_name"].get()
            b_name = handoff_vars["b_name"].get()
            email = handoff_vars["email"].get()
            phone = handoff_vars["phone"].get()
            ord_num = handoff_vars["ord_num"].get()
            manage_acc = handoff_vars["manage_acc"].get()
            shipping = self.selected_listbox.shipping_var.get()
            cs_req = self.selected_listbox.cs_var.get()
            ticket_status = self.selected_listbox.status_var.get()
            db_conn = sql.connect('PR_Tickets.db')
            cx = db_conn.cursor()

            cx.execute("""
                UPDATE handoff_tickets
                SET full_name = ?,
                    b_name = ?,
                    email = ?,
                    phone = ?,
                    ord_num = ?,
                    shipping = ?,
                    cs_req = ?,
                    ticket_status = ?,
                    manage_acc = ?
                WHERE handoff_id = ?
            """, (
                full_name,
                b_name,
                email,
                phone,
                ord_num,
                shipping,
                cs_req,
                ticket_status,
                manage_acc,
                self.selected_ticket
            ))

            db_conn.commit()
            db_conn.close()
            
            current_index = self.selected_listbox.curselection()

            new_listbox = self.ticket_lists[ticket_status]

            if old_listbox != new_listbox:
                current_index = old_listbox.curselection()

                if current_index:
                    old_listbox.delete(current_index[0])

                new_listbox.insert(END, self.selected_ticket)

                self.selected_listbox = new_listbox

            messagebox.showinfo(
                title="Updated",
                message="Ticket updated successfully."
            )
    
    # def new_enter_key(self, case, new_tic, window):
    #     self.add_to_list(case, new_tic)
    #     self.close_window(window)

    def add_to_list(self, t_list, ticket): #Add ticket to ticket list
        self.tict_dict[t_list].append(ticket)
        print(self.tict_dict.get(t_list))

    def close_window(self,window):
        window.destroy()
    
    def clear_text(self): #Clear entries after sending       
        self.handoff_id.delete(0,END)
        self.full_name.delete(0,END)
        self.b_name.delete(0,END)
        self.phone.delete(0,END)
        self.email.delete(0,END)
        self.ord_num.delete(0,END)
        self.e_shipping.set("Not Sent")
        self.e_cs_req.set("")
        self.e_ticket_status.set("Open")
        self.manage_acc.delete(0,END) 

    def new_install_ticket(self):
        if self.selected_ticket is None:
            messagebox.showerror(
                title="Error",
                message="No ticket selected"
            )
            return
        if self.selected_listbox.table_type == "install":
            messagebox.showerror(
                title="Error",
                message="Invalid Selection"
            )
            return

        self.install_window = Toplevel(self.root)
        self.install_window.geometry("400x400")
        self.install_window.title("New Install Ticket")

        self.install_handoff_button_var = StringVar(value=self.selected_ticket)
        self.install_company_var = StringVar(value="")
        self.tech_admin_var = StringVar(value="")
        self.install_complete_var = StringVar(value="")
        self.qc_complete_var = StringVar(value="")

        ttk.Label(self.install_window, text="Handoff Ticket ID").grid(row=0, column=0, padx=10, pady=5)
        ttk.Entry(
            self.install_window,
            textvariable=self.install_handoff_button_var,
            state="readonly",
            width=30
        ).grid(row=0, column=1, padx=10, pady=5)

        ttk.Label(self.install_window, text="Install Ticket ID").grid(row=1, column=0, padx=10, pady=5)
        self.install_id = ttk.Entry(self.install_window, width=30)
        self.install_id.grid(row=1, column=1, padx=10, pady=5)

        ttk.Label(self.install_window, text="Install Company").grid(row=2, column=0, padx=10, pady=5)
        OptionMenu(self.install_window, self.install_company_var, "TL", "TSP").grid(row=2, column=1, padx=10, pady=5)

        ttk.Label(self.install_window, text="Install Date").grid(row=3, column=0, padx=10, pady=5)
        self.install_date = DateEntry(
            self.install_window,
            width=27,
            date_pattern="yyyy-mm-dd"
        )
        self.install_date.grid(row=3, column=1, padx=10, pady=5)

        ttk.Label(self.install_window, text="Tech Name").grid(row=4, column=0, padx=10, pady=5)
        self.tech_name = ttk.Entry(self.install_window, width=30)
        self.tech_name.grid(row=4, column=1, padx=10, pady=5)

        ttk.Label(self.install_window, text="Tech on Admin").grid(row=5, column=0, padx=10, pady=5)
        OptionMenu(self.install_window, self.tech_admin_var, "Create", "Added", "Deleted").grid(row=5, column=1, padx=10, pady=5)

        ttk.Label(self.install_window, text="Work Order #").grid(row=6, column=0, padx=10, pady=5)
        self.work_ord_num = ttk.Entry(self.install_window, width=30)
        self.work_ord_num.grid(row=6, column=1, padx=10, pady=5)

        ttk.Label(self.install_window, text="Install Complete").grid(row=7, column=0, padx=10, pady=5)
        OptionMenu(self.install_window, self.install_complete_var, "Cancelled", "RMA", "Yes").grid(row=7, column=1, padx=10, pady=5)

        ttk.Label(self.install_window, text="QC Complete").grid(row=8, column=0, padx=10, pady=5)
        OptionMenu(self.install_window, self.qc_complete_var, "Pending", "Pass").grid(row=8, column=1, padx=10, pady=5)

        ttk.Label(self.install_window, text="Tracking Number").grid(row=9, column=0, padx=10, pady=5)
        self.tracking_number = ttk.Entry(self.install_window, width=30)
        self.tracking_number.grid(row=9, column=1, padx=10, pady=5)

        ttk.Button(
            self.install_window,
            text="Create Install Ticket",
            command=self.submit_install_ticket
        ).grid(row=10, column=0, columnspan=2, pady=15)

    def submit_install_ticket(self):
        db_conn = sql.connect('PR_Tickets.db')
        cx = db_conn.cursor()

        cx.execute("""
            INSERT INTO install_tickets (
                install_id,
                handoff_id,
                install_company,
                install_date,
                tech_name,
                tech_on_admin,
                work_ord_num,
                install_complete,
                qc_complete,
                tracking_number
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            self.install_id.get(),
            self.install_handoff_button_var.get(),
            self.install_company_var.get(),
            self.install_date.get(),
            self.tech_name.get(),
            self.tech_admin_var.get(),
            self.work_ord_num.get(),
            self.install_complete_var.get(),
            self.qc_complete_var.get(),
            self.tracking_number.get()
        ))

        db_conn.commit()
        db_conn.close()

        self.ticket_lists["Install"].insert(END, self.install_id.get())

        messagebox.showinfo(
            title="Created",
            message="Install ticket created successfully."
        )
        self.install_window.destroy()

# GUI Database SQLITE3
db_conn = sql.connect('PR_Tickets.db') #Create database
cx = db_conn.cursor() #Create cursor 

cx.execute("""CREATE TABLE IF NOT EXISTS handoff_tickets (
           handoff_id INTEGER PRIMARY KEY,
           full_name TEXT,
           b_name TEXT,
           phone TEXT,
           email TEXT,
           ord_num TEXT,
           shipping TEXT,
           cs_req TEXT,
           ticket_status TEXT,
           manage_acc TEXT
           )""" )

cx.execute("""CREATE TABLE IF NOT EXISTS install_tickets(
            install_id INTEGER PRIMARY KEY,
            handoff_id INTEGER,
            install_company TEXT,
            install_date TEXT,
            tech_name TEXT,
            tech_on_admin TEXT,
            work_ord_num TEXT,
            install_complete TEXT,
            qc_complete TEXT,
            tracking_number TEXT
        )""")

db_conn.commit()
db_conn.close()

# Main root window
root = Tk()
ZDint = ZendexGUI(root)
root.geometry("750x500")
root.mainloop()
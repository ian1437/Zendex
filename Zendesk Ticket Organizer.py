# Zendesk Ticket Organizer

import sqlite3 as sql
from tkinter import *
from tkinter import ttk
from tkinter import messagebox


class ZendexGUI:
    def __init__(self, main):

        # Main t.window
        self.root = main
        self.root.title("Tickets")
        self.root.geometry("700x600")
        
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
        self.add = ttk.Button(self.tickets, text = "New Ticket", command = self.new_tic)
        self.add.pack()
        
        # Tabs style
        style = ttk.Style()
        style.configure(
            "TNotebook.Tab",
            padding=[40, 0],
           # font=("Arial", 10)
        )
        
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
        self.install_ticket_list = self.build_ticket_tab(self.install)
        self.scheduled_ticket_list = self.build_ticket_tab(self.sched)
        self.complete_ticket_list = self.build_ticket_tab(self.complete)

        self.ticket_lists = {
            "Open": self.open_ticket_list,
            "Onboard": self.onboard_ticket_list,
            "Install": self.install_ticket_list,
            "Scheduled": self.scheduled_ticket_list,
            "Complete": self.complete_ticket_list
        }

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
        self.ticket_list.bind("<<ListboxSelect>>", self.show_ticket_info)

        # Right ticket info area
        self.right_frame = ttk.Frame(self.container)
        self.right_frame.pack(side="left", fill="both", expand=True)

        details_frame = ttk.LabelFrame(self.right_frame, text="Ticket Details")
        details_frame.pack(pady=10, padx=20, fill="x")

        detail_vars = {
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

            entry = ttk.Entry(details_frame, textvariable=detail_vars[key], width=35)
            entry.grid(row=row, column=1, padx=5, pady=3)

            row += 1

        self.ticket_list.detail_vars = detail_vars

        # Shipping / CS section
        self.action_frame = ttk.Frame(self.right_frame)
        self.action_frame.pack(pady=20)

        ttk.Label(self.action_frame, text="Shipped Status").grid(row=0, column=0, padx=10, pady=5)
        shipping_var = StringVar(value="Not Sent")
        self.shipping_status = ttk.OptionMenu(
            self.action_frame,
            shipping_var,
            "Not Sent",
            "Not Sent",
            "Ready to Ship",
            "Complete"
        )
        self.shipping_status.grid(row=0, column=1, padx=10, pady=5)
        self.ticket_list.shipping_var = shipping_var

        ttk.Label(self.action_frame, text="CS Action").grid(row=1, column=0, padx=10, pady=5)
        cs_var = StringVar(value="")
        self.cs_action = ttk.OptionMenu(
            self.action_frame,
            cs_var,
            "",
            "Onboard Only",
            "Install Only",
            "Onboard + Install",
            "No Onboard + No Install"
        )
        self.cs_action.grid(row=1, column=1, padx=10, pady=5)
        self.ticket_list.cs_var = cs_var

        # Status section
        self.status_frame = ttk.LabelFrame(self.right_frame, text="Status")
        self.status_frame.pack(pady=20, fill="x", padx=30)

        status_var = StringVar(value="Open")
        self.status_menu = ttk.OptionMenu(
            self.status_frame,
            status_var,
            "Open",
            "Open",
            "Onboard",
            "Install",
            "Scheduled",
            "Complete"
        )
        self.status_menu.grid(row=0, column=1, padx=10, pady=10)
        self.ticket_list.status_var = status_var

        self.notes_box = Text(self.status_frame, height=4, width=30)
        self.notes_box.grid(row=1, column=0, columnspan=2, padx=10, pady=10)
        
        delete_button = ttk.Button(
            self.right_frame,
            text="Delete Ticket",
            command=self.delete_ticket
        )
        delete_button.pack(pady=10)

        update_button = ttk.Button(
            self.right_frame,
            text="Update Ticket",
            command=self.update_ticket
        )
        update_button.pack(pady=5)
        
        return self.ticket_list
    
    def load_tickets(self):
        db_conn = sql.connect('PR_Tickets.db')
        cx = db_conn.cursor()
        cx.execute("SELECT handoff_id, full_name, b_name, ticket_status FROM handoff_tickets")
        records = cx.fetchall()
        db_conn.close()

        for record in records:
            handoff_id, full_name, b_name, status = record
            if status in self.ticket_lists:
                ticket_text = str(handoff_id)
                self.ticket_lists[status].insert(END, ticket_text)

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
    
    def show_ticket_info(self, event):
        if not event.widget.curselection():
            return

        selected_ticket = event.widget.get(event.widget.curselection()[0])

        self.selected_ticket = selected_ticket
        self.selected_listbox = event.widget
        
        db_conn = sql.connect('PR_Tickets.db')
        cx = db_conn.cursor()

        cx.execute("""
            SELECT full_name, b_name, email, phone, ord_num, shipping, cs_req, ticket_status, manage_acc
            FROM handoff_tickets
            WHERE handoff_id = ?
        """, (selected_ticket,))

        record = cx.fetchone()

        db_conn.close()

        if record:
            full_name, b_name, email, phone, ord_num, shipping, cs_req, ticket_status, manage_acc = record

            event.widget.detail_vars["full_name"].set(full_name)
            event.widget.detail_vars["b_name"].set(b_name)
            event.widget.detail_vars["email"].set(email)
            event.widget.detail_vars["phone"].set(phone)
            event.widget.detail_vars["ord_num"].set(ord_num)
            event.widget.detail_vars["manage_acc"].set(manage_acc)
            event.widget.shipping_var.set(shipping)
            event.widget.cs_var.set(cs_req)
            event.widget.status_var.set(ticket_status)
    
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

    def update_ticket(self):
        if self.selected_ticket is None:
            return
        old_listbox = self.selected_listbox
        detail_vars = self.selected_listbox.detail_vars

        full_name = detail_vars["full_name"].get()
        b_name = detail_vars["b_name"].get()
        email = detail_vars["email"].get()
        phone = detail_vars["phone"].get()
        ord_num = detail_vars["ord_num"].get()
        manage_acc = detail_vars["manage_acc"].get()
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

    def new_enter_key(self, case, new_tic, window):
        self.add_to_list(case, new_tic)
        self.close_window(window)

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

    #def ticNum(self, number): #ticket number
    #   self.number = number



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
           handoff_id,
           install_company TEXT,
           install_date TEXT,
           tech_name TEXT,
           tech_on_admin TEXT,
           work_ord_num TEXT,
           install_complete TEXT,
           qc_complete TEXT,
           qc_result TEXT,
           tracking_number TEXT
           )""")

cx.execute("""CREATE TABLE IF NOT EXISTS fulfill(
           shipping PRIMARY KEY, 
           status TEXT
           )""")

fulfillment = [
    ('Not Sent',),
    ('Ready to Ship',),
    ('Complete  ',)
]

# cx.executemany("INSERT INTO fulfill (status) VALUES (?)", fulfillment)
           
cx.execute("""CREATE TABLE IF NOT EXISTS cs_req(
           shipping PRIMARY KEY, 
           status TEXT 
           )""")

action = [
    ('Onboard Only',),
    ('Install Only',),
    ('Onboard + Install',),
    ('No Onboard + No Install',)
]

# cx.executemany("INSERT INTO cs_req (status) VALUES (?)", action)

state = [
    ('Open',),
    ('Onboarding',),
    ('Install',),
    ('QC',),
    ('Complete',)
]

# cx.execute("""CREATE TABLE IF NOT EXISTS ticket_status(
#            shipping PRIMARY KEY, 
#            status TEXT 
#            )""")

# cx.executemany("INSERT INTO ticket_status (status) VALUES (?)", state)

db_conn.commit()
db_conn.close()

# Main root window
root = Tk()
ZDint = ZendexGUI(root)
root.geometry("800x800")
root.mainloop()
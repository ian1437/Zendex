# Zendesk Ticket Organizer

import sqlite3 as sql
from tkinter import *
from tkinter import ttk


class ZendexGUI:

    def __init__(self, main):
        
        # Main t.window
        self.root = main
        self.root.title("Tickets")
        self.root.geometry("480x600")
        
        # Ticket init with vars
        self.tickets = ttk.Frame(main)
        self.tickets.pack()
        
        self.tict_dict = {
            'open': [],
            'onboard': [],
            'install': [],
            'qc': [],
            'complete': []
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

        self.add = ttk.Button(self.tickets, text = "New Ticket", command = self.new_tic)
        self.add.pack()
        
        # Tabs to differentiate the ticket status
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

        self.notebook.pack()

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

        #self.handoff_id.bind('<Return>', lambda e: self.new_enter_key("open", self.handoff_id.get(), self.add_new))
    
    def submit_ticket(self):
        db_conn = sql.connect('PR_Tickets.db') #Create database
        cx = db_conn.cursor() #Create cursor 

        #Commit changes and submit to DB
        cx.execute("INSERT INTO handoff_tickets VALUES (:handoff_id, :full_name, :b_name, \
                   :phone, :email, :ord_num, :e_shipping, :e_cs_req, :e_ticket_status, :manage_acc)",
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

# Main root window
root = Tk()
ZDint = ZendexGUI(root)
root.geometry("480x540")

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

root.mainloop()
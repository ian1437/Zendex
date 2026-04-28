# Zendesk Ticket Organizer
# The purpose of this is to bridge the gaps between Onboarding and Installation

# Goals - GUI integreation
# Data to be entered 
# Pulled report 
#   Ticket ID
#   Ticket Status
#   Customer Status
#   Assigee
#   Updater
#   Updated


from tkinter import *
from tkinter import ttk

class ZendexGUI:

    def __init__(self, main):
        
        # Main window
        self.root = main
        self.root.title("Tickets")

        # Ticket init with vars
        self.tickets = ttk.Frame(main).pack()
        self.add_new = False
        self.add = ttk.Button(self.tickets, text = "New Ticket", command = self.new_tic).pack()
        
        self.tict_dict = {
            'open': [],
            'onboard': [],
            'install': [],
            'qc': [],
            'complete': []
        }

        self.tickets = ttk.Frame(main).pack()
        # self.ticket_entry = ttk.Entry(self.tickets, width = 10).pack()

        self.notebook = ttk.Notebook(main)

        self.orders = ttk.Frame(self.notebook)
        self.oboard = ttk.Frame(self.notebook)
        self.install = ttk.Frame(self.notebook)
        self.sched = ttk.Frame(self.notebook)
        self.complete = ttk.Frame(self.notebook)
        
        self.notebook.add(self.orders, text ="Open tickets")
        self.notebook.add(self.oboard, text = "Oboarding")
        self.notebook.add(self.install, text = "Install")    
        self.notebook.add(self.sched, text = "Scheduled")
        self.notebook.add(self.complete, text = "Complete")

        self.notebook.pack()
       
    def new_tic(self): # Creating new ticket
        if self.add_new != False:
            self.add_new.destroy()
        
        self.add_new = Toplevel(self.root) 
        self.entry = ttk.Frame(self.add_new).pack() 
        self.ticket_entry = ttk.Entry(self.add_new, width = 10).pack()
        self.ticket_num = StringVar()
        self.add_new.bind('<Return>', lambda e: self.new_enter_key("open", self.ticket_num.get(), self.add_new))

    def new_enter_key(self, case, new_tic, window):
        self.add_to_list(case, new_tic)
        window.destroy()

    def add_to_list(self, t_list, ticket): #Add ticket to ticket list
        self.tict_dict[t_list].append(ticket)
        print
        
        match t_list:
            case 100:
                self.open_tickets.append(ticket)
                print(self.open_tickets)   
            case 200:
                self.onboard_tickets.append(ticket) 
                print(self.onboard_tickets)
            case 300:
                self.install_tickets.append(ticket) 
                print(self.install_tickets)
            case 400:
                self.qc_tickets.append(ticket)
                print(self.qc_tickets)
            case 500:
                self.complete_tickets.append(ticket)
                print(self.complete_tickets)

    #def 

    def close_window(self):
        self.destroy()
    
    #def clear_text(self):
    #    self.clear 

    # def openFile(self, report):
    #     report = input("file name: ")
    #     with open(report, "r") as f:
    #         for line in f:
    #             print(line)

    def ticNum(self, number): #ticket number
       self.number = number


def main():
    root = Tk()
    ZDint = ZendexGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
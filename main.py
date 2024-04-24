import tkinter as tk
import tkinter.font as tkFont
from tkinter import messagebox
import sqlite3
import random
from datetime import date

class DatabaseConnection:

    def __init__(self):

        self.db_name = ('notes.db')
        self.db = sqlite3.connect(self.db_name)
        self.today = date.today()
        self.today = self.today.strftime("%d/%m/%Y")

    def db_creation(self):
        self.db.execute(

            '''CREATE TABLE rma_notes
         (
         RMA_NUMBER         INT PRIMARY KEY    NOT NULL,
         NOTES          TEXT,
         NAMES          TEXT    NOT NULL,
         DATE          TEXT);'''

        )

    def db_add(self, rma_numer, notes, names, date):
        query = f'INSERT INTO rma_notes (RMA_NUMBER,NOTES,NAMES,DATE)  VALUES ({rma_numer}, "{notes}", "{names}", "{date}")'
        self.db.execute(query)
        self.commit_changes()

    def commit_changes(self):
        self.db.commit()

    def close_db(self):
        self.db.close()

    def output_db(self):
        data = self.db.execute("SELECT RMA_NUMBER, NOTES, NAMES, DATE from rma_notes")

        return data.fetchall()
    
    def get_rma_notes(self, rma_number):
        data = self.db.execute(f"SELECT NOTES FROM rma_notes WHERE RMA_NUMBER={rma_number}")
        
        return data.fetchone()
    
    def add_notes(self, note, rma_number, name):
        prev_note = self.get_rma_notes(rma_number)[0]
        if prev_note == 'None':
            prev_note = ''
        note = '\n'+self.today + ' - '+ name + ': '+ note + '\n'+ prev_note
        #print(name)
        self.db.execute('UPDATE rma_notes SET NOTES=? WHERE RMA_NUMBER=?', (note, rma_number))
        self.commit_changes()

    def clear_db(self):
        sql = "DELETE FROM rma_notes WHERE RMA_NUMBER != ''"
        self.db.execute(sql)
        self.commit_changes()

class App:
    def __init__(self, root):
        #setting title
        root.title("RMA Notes")
        #setting window size
        width=800
        height=500
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        root.geometry(alignstr)
        root.resizable(width=False, height=False)
        self.init_db = DatabaseConnection()


        self.today = date.today()
        self.today = self.today.strftime("%d/%m/%Y")
        root.configure(background='#E9E9E9')
        self.rma_list=tk.Listbox(root)
        self.rma_list["borderwidth"] = "1px"
        ft = tkFont.Font(family='Times',size=10)
        self.rma_list["font"] = ft
        self.rma_list["fg"] = "#333333"
        self.rma_list["bg"] = '#E9E9E9'
        self.rma_list["justify"] = "center"
        self.rma_list.place(x=20,y=20,width=411,height=325)
        self.open_rma_button=tk.Button(root)
        self.open_rma_button["bg"] = '#E9E9E9'
        ft = tkFont.Font(family='Times',size=10)
        self.open_rma_button["font"] = ft
        self.open_rma_button["fg"] = "#000000"
        self.open_rma_button["justify"] = "center"
        self.open_rma_button["text"] = "View/Edit Notes"
        self.open_rma_button.place(x=20,y=360,width=97,height=30)
        self.open_rma_button["command"] = self.open_rma_button_command

        self.add_rma_button=tk.Button(root)
        ft = tkFont.Font(family='Times',size=10)
        self.add_rma_button["font"] = ft
        self.add_rma_button["fg"] = "#000000"
        self.add_rma_button["bg"] = '#E9E9E9'
        self.add_rma_button["justify"] = "center"
        self.add_rma_button["text"] = "Add RMA"
        self.add_rma_button.place(x=370,y=360,width=70,height=30)
        self.add_rma_button["command"] = self.add_rma_button_command

        GLabel_244=tk.Label(root)
        ft = tkFont.Font(family='Times',size=10)
        GLabel_244["font"] = ft
        GLabel_244["fg"] = "#333333"
        GLabel_244["justify"] = "center"
        GLabel_244["bg"] = '#E9E9E9'
        GLabel_244["text"] = "RMA Number:"
        GLabel_244.place(x=150,y=360,width=111,height=30)

        GLabel_245=tk.Label(root)
        ft = tkFont.Font(family='Times',size=10)
        GLabel_245["font"] = ft
        GLabel_245["fg"] = "#333333"
        GLabel_245["bg"] = '#E9E9E9'
        GLabel_245["justify"] = "center"
        GLabel_245["text"] = "Name:"
        GLabel_245.place(x=170,y=400,width=111,height=30)


        self.rma_notes_label=tk.Message(root)
        ft = tkFont.Font(family='Times',size=10)
        self.rma_notes_label["font"] = ft
        self.rma_notes_label["fg"] = "#333333"
        self.rma_notes_label["borderwidth"] = "0px"
        self.rma_notes_label["anchor"] = "nw"
        self.rma_notes_label["bg"] = '#E9e9e9'
        self.rma_notes_label.place(x=435,y=20,width=350,height=276)

        self.rma_number_input=tk.Entry(root)
        self.rma_number_input["borderwidth"] = "1px"
        ft = tkFont.Font(family='Times',size=10)
        self.rma_number_input["font"] = ft
        self.rma_number_input["fg"] = "#333333"
        self.rma_number_input["justify"] = "center"
        self.rma_number_input["text"] = "RMA Here"
        self.rma_number_input.place(x=255,y=360,width=115,height=30)

        self.import_rma_button=tk.Button(root)
        self.import_rma_button["bg"] = '#E9E9E9'
        ft = tkFont.Font(family='Times',size=10)
        self.import_rma_button["font"] = ft
        self.import_rma_button["fg"] = "#000000"
        self.import_rma_button["justify"] = "center"
        self.import_rma_button["text"] = "Import RMA"
        self.import_rma_button.place(x=20,y=400,width=96,height=30)
        self.import_rma_button["command"] = self.import_rma_button_command



        self.name_input=tk.Entry(root)
        self.name_input["borderwidth"] = "1px"
        ft = tkFont.Font(family='Times',size=10)
        self.name_input["font"] = ft
        self.name_input["fg"] = "#333333"
        self.name_input["justify"] = "center"
        self.name_input.place(x=255,y=400,width=115,height=30)

        self.invoice_input=tk.Entry(root)
        self.invoice_input["borderwidth"] = "1px"
        ft = tkFont.Font(family='Times',size=10)
        self.invoice_input["font"] = ft
        self.invoice_input["fg"] = "#333333"
        self.invoice_input["justify"] = "center"
        self.invoice_input.place(x=255,y=440,width=115,height=30)


        invoice_label=tk.Label(root)
        ft = tkFont.Font(family='Times',size=10)
        invoice_label["font"] = ft
        invoice_label["fg"] = "#333333"
        invoice_label["bg"] = '#E9E9E9'
        invoice_label["justify"] = "center"
        invoice_label["text"] = "Invoice No:"
        invoice_label.place(x=170,y=440,width=80,height=30)

        self.rma_notes_update=tk.Entry(root)
        self.rma_notes_update["borderwidth"] = "1px"
        ft = tkFont.Font(family='Times',size=10)
        self.rma_notes_update["font"] = ft
        self.rma_notes_update["fg"] = "#333333"
        self.rma_notes_update["justify"] = "left"
        self.rma_notes_update.place(x=520,y=360,width=191,height=30)


        self.update_notes_button=tk.Button(root)
        ft = tkFont.Font(family='Times',size=10)
        self.update_notes_button["font"] = ft
        self.update_notes_button["fg"] = "#000000"
        self.update_notes_button["bg"] = '#E9E9E9'
        self.update_notes_button["justify"] = "center"
        self.update_notes_button["text"] = "Update Notes"
        self.update_notes_button.place(x=710,y=360,width=80,height=30)
        self.update_notes_button["command"] = self.update_notes_button_command

        self.clear_database_button=tk.Button(root)
        self.clear_database_button["bg"] = "#f0f0f0"
        ft = tkFont.Font(family='Times',size=10)
        self.clear_database_button["font"] = ft
        self.clear_database_button["fg"] = "#000000"
        self.clear_database_button["bg"] = '#E9E9E9'
        self.clear_database_button["justify"] = "center"
        self.clear_database_button["text"] = "Clear database"
        self.clear_database_button.place(x=20,y=440,width=95,height=30)
        self.clear_database_button["command"] = self.clear_database_button_command

        self.add_customer_details=tk.Checkbutton(root)
        ft = tkFont.Font(family='Times',size=10)
        self.add_customer_details["font"] = ft
        self.add_customer_details["fg"] = "#333333"
        self.add_customer_details["justify"] = "center"
        self.add_customer_details["text"] = "Add Customer Info?"
        self.add_customer_details.place(x=515,y=390,width=200,height=25)
        self.add_customer_details["offvalue"] = "0"
        self.add_customer_details["onvalue"] = "1"
        self.add_customer_details["bg"] = '#E9E9E9'
        self.add_customer_details["command"] = self.generate_contact_fields



        self.update_rma_list()

    def generate_contact_fields(self):
        self.customer_name=tk.Entry(root)
        self.customer_name["borderwidth"] = "1px"
        ft = tkFont.Font(family='Times',size=10)
        self.customer_name["font"] = ft
        self.customer_name["fg"] = "#333333"
        self.customer_name["justify"] = "left"
        self.customer_name.place(x=520,y=420,width=191,height=30)

        self.customer_name_label=tk.Label(root)
        ft = tkFont.Font(family='Times',size=10)
        self.customer_name_label["font"] = ft
        self.customer_name_label["fg"] = "#333333"
        self.customer_name_label["bg"] = '#E9E9E9'
        self.customer_name_label["justify"] = "center"
        self.customer_name_label["text"] = "Customer Name:"
        self.customer_name_label.place(x=420,y=420,width=90,height=30)

        self.customer_contact=tk.Entry(root)
        self.customer_contact["borderwidth"] = "1px"
        ft = tkFont.Font(family='Times',size=10)
        self.customer_contact["font"] = ft
        self.customer_contact["fg"] = "#333333"
        self.customer_contact["justify"] = "left"
        self.customer_contact.place(x=520,y=460,width=191,height=30)

        self.customer_contact_label=tk.Label(root)
        ft = tkFont.Font(family='Times',size=10)
        self.customer_contact_label["font"] = ft
        self.customer_contact_label["fg"] = "#333333"
        self.customer_contact_label["bg"] = '#E9E9E9'
        self.customer_contact_label["justify"] = "center"
        self.customer_contact_label["text"] = "Customer Contact:"
        self.customer_contact_label.place(x=410,y=460,width=100,height=30)


        self.update_customer_button=tk.Button(root)
        ft = tkFont.Font(family='Times',size=10)
        self.update_customer_button["font"] = ft
        self.update_customer_button["fg"] = "#000000"
        self.update_customer_button["bg"] = '#E9E9E9'
        self.update_customer_button["justify"] = "center"
        self.update_customer_button["text"] = "Update"
        self.update_customer_button.place(x=720,y=440,width=70,height=30)
        self.update_customer_button["command"] = self.update_customer_button_command


    def update_customer_button_command(self):
        
            
        self.selected_value = self.rma_list.curselection()
        rma_number = self.rma_list.get(self.selected_value[0]).replace('RMA: ', '')

        '''self.init_db.db.execute("ALTER TABLE rma_notes ADD COLUMN customer_name STRING")
        self.init_db.db.execute("ALTER TABLE rma_notes ADD COLUMN customer_contact STRING")'''

        self.init_db.db.execute("UPDATE rma_notes SET customer_name=? WHERE RMA_NUMBER=?", (self.customer_name.get(), rma_number))
        self.init_db.db.execute("UPDATE rma_notes SET customer_contact=? WHERE RMA_NUMBER=?", (self.customer_contact.get(), rma_number))
        
            

        self.init_db.commit_changes()

        

    def clear_database_button_command(self):
        self.init_db.clear_db()
        self.update_rma_list()
        self.rma_list.delete(0,tk.END)

    def update_notes_button_command(self):
        try:
            self.selected_value = self.rma_list.curselection()
            rma_number = self.rma_list.get(self.selected_value[0]).replace('RMA: ', '')
        except IndexError:
            messagebox.showerror("Error", "Please select an RMA!")
            return
        if self.name_input.get() == '':
            messagebox.showerror("Warning!", "Please enter your name.")
            return
        self.init_db.add_notes(self.rma_notes_update.get(), rma_number, self.name_input.get())
        
        self.open_rma_button_command()


    def update_rma_list(self):
        output_data = output_data = self.init_db.output_db()
        for i in range(len(output_data)):
            self.rma_list.insert(i, f'RMA: {output_data[i][0]}')

    def open_rma_button_command(self):

        try:
            self.customer_contact_display_label["text"] = ""
            self.customer_name_display_label["text"] = ""
            try:
                self.invoice_number_label.master.destroy()
            except:
                pass
        except:
            pass
        try:
            self.selected_value = self.rma_list.curselection()
            rma_number = self.rma_list.get(self.selected_value[0]).replace('RMA: ', '')
        except IndexError:
            messagebox.showerror("Error", "Please select an RMA!")
            return
        n = self.init_db.get_rma_notes(rma_number)
        if n[0]  != 'None':
            self.rma_notes_label["text"] = n[0]
        else:
            self.rma_notes_label["text"] = 'No notes!'


        self.init_db.db.execute("UPDATE rma_notes SET invoice_number=? WHERE RMA_NUMBER=?", (self.invoice_input.get(),rma_number))
        check_invoice = self.init_db.db.execute("SELECT invoice_number FROM rma_notes WHERE RMA_NUMBER=(?)", (rma_number,))
        check_invoice = check_invoice.fetchone()
        if str(check_invoice[0]) != None or str(check_invoice[0]) != '':

            self.invoice_number_label=tk.Label(root)
            ft = tkFont.Font(family='Times',size=10)
            self.invoice_number_label["font"] = ft
            self.invoice_number_label["fg"] = "#333333"
            self.invoice_number_label["bg"] = '#E9E9E9'
            self.invoice_number_label["justify"] = "center"
            self.invoice_number_label["text"] = "Invoice No:\n"+str(check_invoice[0])
            self.invoice_number_label.place(x=630,y=150,width=150,height=30)
            self.invoice_input.delete(0, 'end')


        check_valid = self.init_db.db.execute("SELECT customer_name, customer_contact FROM rma_notes WHERE RMA_NUMBER=(?)", (rma_number,))
        check_valid = check_valid.fetchone()
        print(check_valid[0])
        if check_valid[0] != None and check_valid[0] != '':
            self.customer_contact_display_label=tk.Label(root)
            ft = tkFont.Font(family='Times',size=10)
            self.customer_contact_display_label["font"] = ft
            self.customer_contact_display_label["fg"] = "#333333"
            self.customer_contact_display_label["bg"] = '#E9E9E9'
            self.customer_contact_display_label["justify"] = "center"
            self.customer_contact_display_label["text"] = "Customer Name:\n"+str(check_valid[0])
            self.customer_contact_display_label.place(x=630,y=30,width=150,height=30)
            if check_valid[1] != None and check_valid[1] != '':
                self.customer_name_display_label=tk.Label(root)
                ft = tkFont.Font(family='Times',size=10)
                self.customer_name_display_label["font"] = ft
                self.customer_name_display_label["fg"] = "#333333"
                self.customer_name_display_label["bg"] = '#E9E9E9'
                self.customer_name_display_label["justify"] = "center"
                self.customer_name_display_label["text"] = "Customer Contact:\n"+str(check_valid[1])
                self.customer_name_display_label.place(x=635,y=90,width=150,height=30)
       
            
        self.init_db.commit_changes()



    def add_rma_button_command(self):
        try:
            if self.name_input.get() == '':
                messagebox.showerror("Warning", "Please enter your name!")
                return
            self.init_db.db_add(self.rma_number_input.get(), None, self.name_input.get(), '')
            output_data = self.init_db.output_db()

            lenDB = len(output_data)
            self.rma_list.insert(lenDB+1, f'RMA: {output_data[lenDB-1][0]}')
            self.init_db.commit_changes()
        except:
            messagebox.showerror("Error!", "Please enter a(n) RMA number")
            return


    def import_rma_button_command(self):
        pass

    
if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()

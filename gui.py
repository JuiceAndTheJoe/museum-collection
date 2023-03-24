import museum
from items import Item
from functions import *
from tkinter import *


class Application(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.grid()
        self.create_widgets()

    # ---------- THIS IS WHERE ALL THE GUI ITEMS ARE CREATED ---------
    def create_widgets(self):
        # create label and entries for name, y & z
        Label(self,
              text="Namn:"
              ).grid(row=0, column=1, sticky=W)
        
        self.name_ent = Entry(self)
        self.name_ent.grid(row=0, column=2, sticky=W)

        Label(self,
              text="ID-nummer:"
              ).grid(row=2, column=1, sticky=W)
        
        self.nr_ent = Entry(self)
        self.nr_ent.grid(row=2, column=2, sticky=W)

        Label(self,
              text="Beskrivning:"
              ).grid(row=3, column=1, sticky=W)
        
        self.beskr_ent = Entry(self)
        self.beskr_ent.grid(row=3, column=2, sticky=W)

        Label(self,
              text="Kontext:"
              ).grid(row=4, column=1, sticky=W)
        
        self.kont_ent = Entry(self)
        self.kont_ent.grid(row=4, column=2, sticky=W)

        # create VIP check button
        self.inkludera = BooleanVar()
        Checkbutton(self,
                    text="Inkludera utlånade föremål",
                    variable=self.inkludera
                    ).grid(row=5, column=1, sticky=W)

        # create buttons for adding items and running simulator
        self.bttn_add = Button(self,
                               text="Skapa nytt föremål",
                               command=self.bttn_create_item)
        self.bttn_add.grid(row=0, column=0, sticky=W)

        self.bttn_sim = Button(self,
                            text="Ta bort föremål",
                            command=self.bttn_delete)
        self.bttn_sim.grid(row=1, column=0, sticky=W)

        self.bttn_dep = Button(self,
                               text="Sök i samlingen",
                               command=self.bttn_search)
        self.bttn_dep.grid(row=2, column=0, sticky=W)

        self.bttn_chPIN = Button(self,
                               text="Byt ett föremåls beskrivning",
                               command=self.bttn_change_PIN)
        self.bttn_chPIN.grid(row=3, column=0, sticky=W)

        self.bttn_view_t = Button(self,
                                 text="Byt ett föremåls kontext",
                                 command=self.bttn_view_transactions)
        self.bttn_view_t.grid(row=4, column=0, sticky=W)

        self.bttn_view_t = Button(self,
                                 text="Hantera lån",
                                 command=self.bttn_view_transactions)
        self.bttn_view_t.grid(row=5, column=0, sticky=W)

        # create text field
        self.output_txt = Text(self, width=55, height=10, wrap=WORD)
        self.output_txt.grid(row=6, column=0, columnspan=2)

    # ---------- SOME HELPING FUNCTIONS ---------

    def get_name_id(self):
        try:
            self.name = self.name_ent.get()
            if len(self.name) == 0:
                raise ValueError("inget namn angiven")
            self.nr = int(self.nr_ent.get())
        except ValueError as error:
            self.output_txt.delete(0.0, END)
            self.output_txt.insert(0.0, "ID-nummer måste vara ett tal och fältet får inte vara tomt!")
            return False
        else:
            return True

    def get_beskr_kont(self):
        if not (self.beskr_ent.get() or self.kont_ent.get()):
            self.output_txt.delete(0.0, END)
            self.output_txt.insert(0.0, "Tom beskrivning!")
            return False
        else:
            return True

    # ---------- THESE ARE THE FUNCTIONS EXECUTED BY THE GUI ITEMS  ---------

    def bttn_create_item(self):
        if self.get_name_id() == True:
            museum.item_dict[self.name_ent.get()] = Item(self.name_ent.get(), self.nr_ent.get(), self.beskr_ent.get(), self.kont_ent.get())
            result = f"Objekt skapad! {self.name_ent.get()} finns nu i samlingen."
            save_dict(museum.item_dict)
        else:
            result = f"Ange ett namn och ID-nummer."
        self.output_txt.delete(0.0, END)
        self.output_txt.insert(0.0, result)

    def bttn_delete(self):
        if self.get_name_id() == True:
            try:
                del museum.item_dict[self.name_ent.get()]
                result = f"{self.name_ent.get()} har blivit borttagen från samlingen."
                save_dict(museum.item_dict)
            except KeyError:
                result = f"Inga objekt hittades under namnet \"{self.name_ent.get()}\""
        self.output_txt.delete(0.0, END)
        self.output_txt.insert(0.0, result)

    def bttn_search(self):
        self.output_txt.delete(0.0, END)
        if self.get_beskr_kont() == True:
            if self.beskr_ent.get():
                result = str(fritext("d", self.beskr_ent.get(), museum.item_dict))
                if not result:
                    result = f"Inga föremål hittades under beskrivning \"{self.beskr_ent.get()}\". Testa att omformulera dig!"
            else:
                result = str(fritext("k", self.kont_ent.get(), museum.item_dict))
                if not result:
                    result = f"Inga föremål hittades under beskrivning \"{self.kont_ent.get()}\". Testa att omformulera dig!"
        else:
            result = "Skriv en beskrivning eller kontext!"
        self.output_txt.delete(0.0, END)
        self.output_txt.insert(0.0, result)

    def bttn_change_PIN(self):
        old_pin = self.pin
        if self.get_name_pin() == True:
            if self.name in museum.item_dict:
                result = museum.item_dict[self.name].change_PIN(old_pin, self.pin)
            else:
                result = self.name + " does not have an account with us, would you like to create one?"
            self.output_txt.delete(0.0, END)
            self.output_txt.insert(0.0, result)


    def bttn_view_transactions(self):
        if self.get_name_pin() == True:
            if self.name in museum.item_dict:
                if museum.item_dict[self.name].ok_PIN(self.pin):
                    result = museum.item_dict[self.name]
                else:
                    result = "Wrong PIN"
            else:
                result = self.name + " does not have an account with us, would you like to create one?"
            self.output_txt.delete(0.0, END)
            self.output_txt.insert(0.0, result)


 # ---------- SETTING UP THE MAIN WINDOW ---------


root = Tk()
root.title("Museets hjälpreda!")
root.geometry("1400x600")
my_app = Application(root)
root.mainloop()
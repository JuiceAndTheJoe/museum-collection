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

        self.desc_ent = Entry(self)
        self.desc_ent.grid(row=3, column=2, sticky=W)

        Label(self,
              text="Kontext:"
              ).grid(row=4, column=1, sticky=W)

        self.cont_ent = Entry(self)
        self.cont_ent.grid(row=4, column=2, sticky=W)

        # create check button
        self.include = BooleanVar()
        Checkbutton(self,
                    text="Inkludera utlånade föremål",
                    variable=self.include
                    ).grid(row=5, column=1, sticky=W)

        # create buttons for adding items and running simulator
        self.bttn_add = Button(self,
                               text="Skapa nytt föremål",
                               command=self.bttn_create_item)
        self.bttn_add.grid(row=0, column=0, sticky=W)

        self.bttn_del = Button(self,
                               text="Ta bort föremål",
                               command=self.bttn_delete)
        self.bttn_del.grid(row=1, column=0, sticky=W)

        self.bttn_dc = Button(self,
                               text="Sök beskrivning/kontext",
                               command=self.bttn_search)
        self.bttn_dc.grid(row=2, column=0, sticky=W)

        self.bttn_chD = Button(self,
                                 text="Byt ett föremåls beskrivning",
                                 command=self.bttn_change_desc)
        self.bttn_chD.grid(row=3, column=0, sticky=W)

        self.bttn_chC = Button(self,
                                  text="Byt ett föremåls kontext",
                                  command=self.bttn_change_cont)
        self.bttn_chC.grid(row=4, column=0, sticky=W)

        self.bttn_m = Button(self,
                                  text="Hantera lån",
                                  command=self.bttn_manage)
        self.bttn_m.grid(row=5, column=0, sticky=W)

        self.bttn_view = Button(self,
                                  text="Visa hela samlingen",
                                  command=self.bttn_show)
        self.bttn_view.grid(row=6, column=0, sticky=W)

        # create clear button
        self.clear_bttn = Button(self,
                                 text="Rensa inputs",
                                 command=self.clear)
        self.clear_bttn.grid(row=6, column=2, sticky=W)

        # create text field
        self.output_txt = Text(self, width=100, height=25, wrap=WORD)
        self.output_txt.grid(row=7, column=0, columnspan=3)

    # ---------- SOME HELPING FUNCTIONS ---------

    def get_name_id(self):
        try:
            self.name = self.name_ent.get()
            if len(self.name) == 0:
                raise ValueError("inget namn angiven")
            self.nr = int(self.nr_ent.get())
        except ValueError:
            self.output_txt.delete(0.0, END)
            self.output_txt.insert(
                0.0, "ID-nummer måste vara ett tal och fältet får inte vara tomt!")
            return False
        else:
            return True

    def get_desc_cont(self):
        if not (self.desc_ent.get() or self.cont_ent.get()):
            self.output_txt.delete(0.0, END)
            self.output_txt.insert(0.0, "Tom beskrivning!")
            return False
        else:
            return True

    # ---------- THESE ARE THE FUNCTIONS EXECUTED BY THE GUI ITEMS  ---------

    def bttn_create_item(self):
        if self.get_name_id() == True:
            cont_list = self.cont_ent.get().split(", ")
            museum.item_dict[self.name_ent.get()] = Item(
                self.name_ent.get(), self.nr_ent.get(), self.desc_ent.get(), cont_list)
            result = f"Objekt skapad! {self.name_ent.get()} finns nu i samlingen."
            save_dict(museum.item_dict)
        else:
            result = f"Ange ett namn och ID-nummer."
        self.output_txt.delete(0.0, END)
        self.output_txt.insert(0.0, result)

    def bttn_delete(self):
        if self.name_ent.get():
            try:
                del museum.item_dict[self.name_ent.get()]
                result = f"{self.name_ent.get()} har blivit borttagen från samlingen."
                save_dict(museum.item_dict)
            except KeyError:
                result = f"Inga objekt hittades under namnet \"{self.name_ent.get()}\""
        else:
            result = "Ange föremålsnamn."
        self.output_txt.delete(0.0, END)
        self.output_txt.insert(0.0, result)

    def bttn_search(self):

        self.output_txt.delete(0.0, END)

        if self.get_desc_cont() == True:

            if self.desc_ent.get():
                matches = fritext("d", self.desc_ent.get(), museum.item_dict)
                self.output_txt.insert(0.0, matches)
                m = []
                for a in matches:
                    self.output_txt.insert(0.0, a)
                    museum.item_dict[a].antal += 1
                    m.append(museum.item_dict[a])
                result = m
                if not matches:
                    result = f"Inga föremål hittades under beskrivning \"{self.desc_ent.get()}\". Testa att omformulera dig!"

            elif self.cont_ent.get():
                matches = fritext("k", self.cont_ent.get(), museum.item_dict)
                self.output_txt.insert(0.0, matches)
                m = []
                for a in matches:
                    self.output_txt.insert(0.0, a)
                    museum.item_dict[a].antal += 1
                    m.append(museum.item_dict[a])
                result = m
                if not matches:
                    result = f"Inga föremål hittades under kontext \"{self.cont_ent.get()}\". Testa att omformulera dig!"
        else:
            result = "Skriv en beskrivning eller kontext!"
        self.output_txt.delete(0.0, END)
        self.output_txt.insert(0.0, result)

    def bttn_change_desc(self):
        if self.name_ent.get() and self.get_desc_cont():
            try:
                result = museum.item_dict[self.name_ent.get()].change_desc(
                    self.desc_ent.get())
                save_dict(museum.item_dict)
            except KeyError:
                result = f"Inget föremål med namn {self.name_ent.get()} hittades i samlingen."
        else:
            result = f"Ange föremålsnamn och beskrivning."
        self.output_txt.delete(0.0, END)
        self.output_txt.insert(0.0, result)

    def bttn_change_cont(self):
        if self.name_ent.get() and self.get_desc_cont():
            try:
                result = museum.item_dict[self.name_ent.get()].change_cont(
                    self.cont_ent.get())
                save_dict(museum.item_dict)
            except KeyError:
                result = f"Inget föremål med namn {self.name_ent.get()} hittades i samlingen."
        else:
            result = "Ange föremålsnamn och kontext."
        self.output_txt.delete(0.0, END)
        self.output_txt.insert(0.0, result)

    def bttn_manage(self):
        if self.name_ent.get():
            if not museum.item_dict[self.name_ent.get()].loaned:
                if self.cont_ent.get():
                    dest = self.cont_ent.get()
                    museum.item_dict[self.name_ent.get()].loaned = dest
                    result = f"\n{self.name_ent.get()} är nu på väg till {dest}."
                    save_dict(museum.item_dict)
                else:
                    result = "Föremålet är kvar i vår samling!"
            else:
                museum.item_dict[self.name_ent.get()].loaned = ""
                result = f"\nFöremålet har varit lånat, men är nu tillbaka i vår samling :)"
                save_dict(museum.item_dict)
        elif not self.name_ent.get():
            result = "Ange ett föremålsnamn. Skriv museumnamn i fältet för kontext. (Lämna fältet tomt om inte det ska lånas)"
        else:
            result = f"Inget föremål med namn {self.name_ent.get()} hittades i samlingen."
        self.output_txt.delete(0.0, END)
        self.output_txt.insert(0.0, result)

    def bttn_show(self):  # Tkinter operates in reverse for some reason? 
        nr = len(museum.item_dict) + 1
        self.output_txt.delete(0.0, END)
        if self.include.get():

            for item in reversed(museum.item_dict.values()):
                item.searched += 1
                nr -= 1
                self.output_txt.insert(0.0, f"\n{nr}. {str(item)}")
            self.output_txt.insert(
            0.0, f"Samlingen innehåller följande {len(museum.item_dict)} element:\n")
        
        else:
            n = 2
            for item in museum.item_dict.values():
                if item.loaned == "":
                    item.searched += 1
                    self.output_txt.insert(0.0, f"\n{n}. {str(item)}")
                    n -= 1
            self.output_txt.insert(0.0, "Just nu visas följande element:\n")

        save_dict(museum.item_dict)

    def clear(self):
        boxes = [self.name_ent, self.nr_ent, self.desc_ent, self.cont_ent]
        for box in boxes:
            box.delete(0, END)

 # ---------- SETTING UP THE MAIN WINDOW ---------


root = Tk()
root.title("Museets hjälpreda!")
root.geometry("900x600")
my_app = Application(root)
root.mainloop()

"""
TODO:   
        Lägg till bildfält
"""
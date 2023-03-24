from functions import *

def execute(choice: int) -> None:
    """
    Used to execute the option that the user chose
    :param choice: an int corresponding the the chosen option
    """
    if choice == 1:
        name = input("Namn: ")
        idnr = input("ID-nummer: ")
        beskr = input("Beskrivning: ")
        kontext = input("Kontext - (använd komma imellan om flera kontext): ").split(", ")

        item_dict[name] = Item(name,idnr,beskr,kontext)
        print(f"\n{name} har lagts till i samlingen!")

    elif choice == 2:
        name = input("Vilket föremål vill du ta bort?: ")
        try:
            del item_dict[name]
            print(f"{name} har blivit borttagen från samlingen!")
        except KeyError:
            print(f"Inget föremål med namn {name} hittades i samlingen.")
    
    elif choice == 3:
        try:
            val = int(input("\nDu kan söka på: \n1- Namn \
                            \n2- Kontext \
                            \n3- Beskrivning \
                            \neller 4 - visa hela samlingen. \
                            \n\nDitt val: "))    
            if val == 1:
                name = input("Name: ")
                try:
                    if (itm := item_dict[name]):
                        itm.antal += 1
                        print(itm)
                except KeyError:
                    print(f"Inget föremål med namn {name} hittades i samlingen.")
            elif val == 2:
                kon = input("Kontext: ")
                try:
                    fritext("k", kon, item_dict)
                except KeyError:
                    print(f"Inget föremål hittades under kontexten \"{kon}\".")
                    print(item_dict)
            elif val == 3:
                bes = input("Beskrivning: ")
                try:
                    fritext("d", bes, item_dict)
                except KeyError:
                    print(f"Inget föremål hittades under beskrivningen \"{bes}\".")
                    print(item_dict) 
            elif val == 4:
                nr = 1
                c = input("Inkludera utlånade föremål? y/n ~ ")
                if c == "y":
                    print(f"\nSamlingen innehåller följande {len(item_dict)} element:\n")
                    for item in item_dict.values():
                        item.antal += 1
                        print(f"{nr}. {str(item)}")
                        nr += 1
                elif c == "n":
                    print("\nJust nu visas följande element:\n")
                    for item in item_dict.values():
                        if item.lånat == "":
                            item.antal += 1
                            print(f"{nr}. {str(item)}")
                            nr += 1
                else:
                    print("Svara med ja (y/Y) eller nej (n/N)!")
        except ValueError:
            print("Svara med ett heltal mellan 1 och 4!")
    
    elif choice == 4:
        name = input("Vilket föremål vill du ändra beskrivningen på?: ")
        nb = input("Ny beskrivning: ")
        try:
            print(item_dict[name].byt_beskr(nb))
        except KeyError:
            print(f"Inget föremål med namn {name} hittades i samlingen.")
    elif choice == 5:
        name = input("Vilket föremål vill du ändra kontexten på?: ")
        nk = input("Ny kontext: ")
        try:
            print(item_dict[name].byt_kontext(nk))
        except KeyError:
            print(f"Inget föremål med namn {name} hittades i samlingen.")
    elif choice == 6:
        name = input("Vilket föremål vill du hantera?: ")
        try:
            if not item_dict[name].lånat:
                dest = input(f"\n{item_dict[name]} är här i museet! Var ska den lånas? (Tryck \'Enter\' om inte det ska lånas) : ")
                item_dict[name].lånat = dest
                print(f"\n{item_dict[name]} är nu på väg till {dest}.")
            else:
                print(f"\nFöremålet har varit lånat till {item_dict[name].lånat}! Nu är det tillbaka i vår samling :)")
                item_dict[name].lånat = ""
        except KeyError:
            print(f"Inget föremål med namn {name} hittades i samlingen.")
    elif choice == 7:
        save_dict(item_dict)
    else:
        print("Svara med ett heltal i intervallet 1-5.")

def main():
    while True:
        menu()
        choice = menu_choice()
        execute(choice)
        if choice == 7:
            break

item_dict = read_Item("dump")

if __name__ == "__main__":
    main()
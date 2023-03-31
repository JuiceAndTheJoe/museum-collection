from items import *
import sys
import pickle

# I/O & menyfunktioner

def read_Item(file_name: str) -> dict[str, Item]:
    """
        Läser in föremål från fil.

        Parameters
        ----------
        file_name
            Filnamn.
        
        Returns
        -------
        dict
            Dictionary innehållande filinnehållet.
        """
    try:
        with open(file_name, "rb") as f:
            return pickle.load(f)
    except IOError:
        return {}

def write_Item(Item: dict[str, Item], file_name: str) -> None:
    """
        Skriver föremål till fil.

        Parameters
        ----------
        Item
            Dictionary innehållande föremål
        file_name
            Destinationsfilnamn
        """
    try:
        with open(file_name, "wb") as f:
            pickle.dump(Item, f, protocol=pickle.HIGHEST_PROTOCOL)
            pass
    except Exception as e:
        print(f"Error appeared: {e}.\nExiting w/o saving...", file=sys.stderr)
        sys.exit(1)

def get_int_input(prompt_string: str) -> int:
    """
    Used to get an int from the user, asks again if input is
    not convertible to int

    Parameters
    ----------
    prompt_string
        The string explaining what to input
    
    Returns
    -------
    int
        The int that was asked for
    """
    while True:
        try:
            return int(input(prompt_string))
        except ValueError:
            print("Svara med ett heltal!\n")
        
def menu() -> None:
    """
    Used to display the menu:
    1 - Skapa nytt föremål
    2 - Ta bort föremål
    3 - Söka i samlingen
    4 - Byt beskrivning på föremål
    5 - Byt kontext på föremål
    6 - Spara och avsluta
    """
    print("\nMuseets hjälpreda! Vad vill du göra? \
          \n1 - Skapa nytt föremål \
          \n2 - Ta bort föremål \
          \n3 - Söka i samlingen \
          \n4 - Byt beskrivning på föremål \
          \n5 - Byt kontext på föremål \
          \n6 - Hantera lån \
          \n7 - Spara och avsluta")

def menu_choice() -> int:

    """
    Used to get input on what the user wants to do

    Returns
    -------
    int
        The chosen menu option
    """
    return get_int_input("\nDitt val: ")

# Objektfunktioner (hanterar sökning, ändring av egenskaper, etc)

def fritext(type: str, s: str, d: dict) -> list:
    """
    Used to search for partial descriptions/contexts of objects, 
    returns a list of objects that match the query.

    Parameters
    ----------
    type
        "k" or "d" - this principle can be applied to context or description search.
    s
        The query string 
    d
        A dictionary to look through
    """
    if type == "d":   # sök beskrivning
        all_besk = {}
        for obj in d.values():
            all_besk[obj] = [obj.namn, obj.beskr]   # all_besk innehåller objekt som key och namn och beskrivning av varje objekt som value
    
        matches = []
        for a in all_besk.values():
            if s in a[1]:                           # om någon del av beskrivningen matchar query
                matches.append(a[0])                # lägg till namnet i listan
        
        return matches
    
    elif type == "k": # sök kontext
        all_kont = {}
        for obj in d.values():
            all_kont[obj] = [obj.namn, obj.kontext] # all_kont innehåller objekt som key och namn och kontext av varje objekt som value
            # {adaosijdak : ['test', ["uno", "dos", "tres"]]}
    
        matches = []
        for value in all_kont.values():             
            for k in value[1]:                      # om någon av kontexten matchar query, lägg till objektnamnet i listan
                if s in k:
                    matches.append(value[0])

        return matches

    else:
        pass                                        # error hanteras utanför funktionen

def save_dict(dict: dict) -> None:
    if (itms := dict):
        write_Item(itms, "dump")

def hantera(name: str, item_dict: dict):
    try:
        if not item_dict[name].lånat:
            dest = input(f"\n{item_dict[name]} är här i museet! Var ska den lånas? (Tryck \'Enter\' om inte det ska lånas) : ")
            item_dict[name].lånat = dest
            return f"\n{item_dict[name]} är nu på väg till {dest}."
        else:
            item_dict[name].lånat = ""
            return f"\nFöremålet har varit lånat till {item_dict[name].lånat}! Nu är det tillbaka i vår samling :)"
    except KeyError:
        return f"Inget föremål med namn {name} hittades i samlingen."

"""
TODO: För över färdiga delar av koden i menyn, de som skapar, söker och tar bort föremål. 
Det gör det 
1. enklare att läsa 
2. enklare att anropa när GUI:n körs
"""
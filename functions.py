from items import *
import sys
import pickle

# I/O & menu funtions


def read_Item(file_name: str) -> dict[str, Item]:
    """
        Reads all items from a file.

        Parameters
        ----------
        file_name
            The file to load from (should be inside the current directory).

        Returns
        -------
        dict
            A dictionary that contains all items listed in the file.
        """
    try:
        with open(file_name, "rb") as f:
            return pickle.load(f)
    except IOError:
        return {}


def write_Item(Item: dict[str, Item], file_name: str) -> None:
    """
        Writes the collection to a file.

        Parameters
        ----------
        Item
            A dictionary containing the collection of items.
        file_name
            The destination file.
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
    not convertible to int.

    Parameters
    ----------
    prompt_string
        The string explaining what to input.

    Returns
    -------
    int
        The int that was asked for.
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


def fritext(type: str, search: str, d: dict) -> list:
    """
    Used to search for partial descriptions/contexts of objects,
    returns a list of objects that match the query.

    Parameters
    ----------
    type
        "k" or "d" - this principle can be applied to context or description search.
    search
        The query string
    d
        A dictionary to look through
    """
    if type == "d":   # description search
        all_desc = {}
        for obj in d.values():
            # all_desc contains instances of Item as keys and name and descriptions of each as values
            all_desc[obj] = [obj.name, obj.desc]

        matches = []
        for attributes in all_desc.values():
            if search in attributes[1]:                           # if any part of the description matches the query
                matches.append(attributes[0])                     # add the name to the list

        return matches

    elif type == "k":  # context search
        all_cont = {}
        for obj in d.values():
            # all_cont contains instances of Item as keys and name and contexts of each as values
            all_cont[obj] = [obj.name, obj.cont]
            # ex: {<place in memory> : ['test', ["uno", "dos", "tres"]]}

        matches = []
        for value in all_cont.values():
            # if any of the contexts match the query, add the name to the list
            for context in value[1]:
                if search in context:
                    matches.append(value[0])

        return matches

    else:
        pass                                        # errors are handled outside of this function


def save_dict(dict: dict) -> None:
    if (itms := dict):
        write_Item(itms, "dump")


def manage(name: str, item_dict: dict):
    try:
        if not item_dict[name].loaned:
            dest = input(
                f"\n{item_dict[name]} är här i museet! Var ska den lånas? (Tryck \'Enter\' om inte det ska lånas) : ")
            item_dict[name].loaned = dest
            print(f"\n{item_dict[name]} är nu på väg till {dest}.")
        else:
            print(
                f"\nFöremålet har varit loaned till {item_dict[name].loaned}! Nu är det tillbaka i vår samling :)")
            item_dict[name].loaned = ""
    except KeyError:
        print(f"Inget föremål med name {name} hittades i samlingen.")


"""
TODO: För över färdiga delar av koden i menyn, de som skapar, söker och tar bort föremål.
Det gör det
1. enklare att läsa
2. enklare att anropa när GUI:n körs
"""
class Item:

    """
    An item in the collection.

    Attributes
    ----------
    name : str
        The item's name.
    idnr: int
        The item's ID-number.
    desc : str
        Short description of the item.
    cont : list
        The item's historical contexts.
    searched : int
        The number of times the item has been searched.
    loaned : str
        What museum the item is currently loaned to. If empty (False), the item is not loaned.
    """

    def __init__(self, name: str, idnr: int, desc: str, cont: list) -> None:
        """
        Creates a new item

        Parameters
        ----------
        name
            The item's name.
        idnr
            The item's ID-number.
        desc
            Short description of the item.
        cont
            The item's historical contexts.
        """
        self.name = name
        self.idnr = idnr
        self.desc = desc
        self.cont = cont
        self.searched = 0
        self.loaned = ""

    def __str__(self) -> str:
        """
        Prints the item's attributes

        Returns
        str
            A nice string containing the item's attributes
        """
        cont = ""
        for c in self.cont:
            cont += (c + ', ')

        if not self.loaned:
            loan = ""
        else:
            loan = f"**För närvarande i {self.loaned}.**"

        return f"{self.name}, \"{self.desc}\", tillhör {cont}Id-nummer: {self.idnr} - [{self.searched} sökningar] {loan}\n"

    def change_desc(self, new_desc: str) -> str:
        """
        Changes the item's description.

        Parameters
        ----------
        new_desc
            The new description

        Returns
        -------
        str
            Confirmation saying the change has occured.
        """
        self.desc = new_desc
        return f"Uppdaterad beskrivning: {self.desc}\n"

    def change_cont(self, new_cont: list) -> str:
        """
        Changes the item's historical context.

        Parameters
        ----------
        new_cont
            The new context

        Returns
        -------
        str
            Confirmation saying the change has occured.
        """
        self.cont = new_cont.split(", ")
        return f"Uppdaterad historiskt sammanhang: {self.cont}\n"
class Item:

    """
    Ett föremål i museet.

    Attributes
    ----------
    namn : str
        Föremålets namn.
    idnr: int
        Föremålets identifikationsnummer.
    beskr : str
        Kort beskrivning av föremålet.
    kontext : list
        Föremålets historiska sammanhang.
    antal : int
        Antalet gånger föremålet har sökts.
    lånat : str
        Vilket museum föremålet är lånat till. Om tom sträng (False), är föremålet inte lånat.
    """

    def __init__(self, namn: str, idnr: int, beskr: str, kontext: list) -> None:
        
        """
        Skapar ett nytt föremål

        Parameters
        ----------
        namn
            Föremålets namn.
        idnr
            Föremålets identifikationsnummer.
        beskr
            Kort beskrivning av föremålet.
        kontext
            Föremålets historiska sammanhang.
        """
        self.namn = namn
        self.idnr = idnr
        self.beskr = beskr
        self.kontext = kontext
        self.antal = 0
        self.lånat = ""

    def __str__(self) -> str:
        """
        Föremålets information att skriva ut
        
        Returns
        str
            En fin sträng som redogör för föremålets egenskaper
        """
        kont = ""
        for k in self.kontext:
            kont += (k + ', ')
        
        if not self.lånat:
            loan = ""
        else:
            loan = f"**För närvarande i {self.lånat}.**"

        return f"{self.namn}, \"{self.beskr}\", tillhör {kont}Id-nummer: {self.idnr} - [{self.antal} sökningar] {loan}\n"
    
    def byt_beskr(self, new_beskr: str) -> str:
        """
        Byter föremålets beskriving.

        Parameters
        ----------
        new_beskr
            Nya beskrivningen
        
        Returns
        -------
        str
            Bekräftelse på uppdateringen.
        """
        self.beskr = new_beskr
        return f"Uppdaterad beskrivning: {self.beskr}\n"

    def byt_kontext(self, new_kontext: list) -> str:
        """
        Byter föremålets historiska sammanhang.

        Parameters
        ----------
        new_kontext
            Nya sammanhanget
        
        Returns
        -------
        str
            Bekräftelse på uppdateringen.
        """
        self.kontext = new_kontext.split(", ")
        return f"Uppdaterad historiskt sammanhang: {self.kontext}\n"

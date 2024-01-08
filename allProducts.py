#Defining Producten class:
class Producten:
    __prijs: float
    __naam: str
    
    def __init__(self, prijs, naam):
        self.__prijs = prijs
        self.__naam = naam

    #Setters:
    def set_prijs(self, prijs):
        self.__prijs = prijs
    def set_naam(self, naam):
        self.__naam = naam
    
    #getters:
    def get_prijs(self):
        return self.__prijs
    def get_naam(self):
        return self.__naam 

#Defining Diensten class: overerving van Producten
class Diensten(Producten):
    def __init__(self,prijs, naam):
        Producten.__init__(self, prijs, naam)

#Defining Goederen class: overerving van Producten
class Goederen(Producten):
    def __init__(self,prijs, naam):
        Producten.__init__(self, prijs, naam)
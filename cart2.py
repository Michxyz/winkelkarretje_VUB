from allProducts import Diensten
from allProducts import Goederen
import tkinter as tk
from tkinter import messagebox

# Sommige producten als voorbeeld:
producten_lijst = [
    # Goederen
    Goederen(prijs=100.00, naam="Winterbanden"),  
    Goederen(prijs=50.00, naam="Motorolie"),      
    Goederen(prijs=75.00, naam="Accu"),           
    Goederen(prijs=40.00, naam="Ruitenwissers"),  
    Goederen(prijs=30.00, naam="Luchtfilters"),   
    Goederen(prijs=20.00, naam="Koelvloeistof"),  
    Goederen(prijs=25.00, naam="Remblokken"),     

    # Diensten
    Diensten(prijs=150.00, naam="Onderhoud"),     
    Diensten(prijs=100.00, naam="Schoonmaak"),    
    Diensten(prijs=200.00, naam="Reparatie")      
]



class CartApplication(tk.Frame):
    def __init__(self, master=None, producten_lijst=None):
        super().__init__(master)
        
        self.producten_lijst = producten_lijst or []
        self.cart = {}  #Het winkelkarretje gaat een lege dict gebruiken om de producten en het aantal op te slaan: key -> product, value-> aantal
        self.master = master
        self.pack()
        self.create_widgets()
        
        
    
    #Methoden voor de druknoppen:   
    def product_toevoegen(self, product):
        #Als het product een instantie is van Diensten en het product al in het winkelkarretje zit, dan zal het product niet toegevoegd worden
        product_naam = product.get_naam()
       
        if isinstance(product, Diensten) and product_naam in self.cart:
            print(f"De dienst '{product_naam}' bevindt  zich al in het winkelkarretje")
            messagebox.showinfo(title= "info", message= f"De dienst '{product_naam}' zit al in het winkelkarretje")
            #return om de methode te stoppen:
            return
        #Als het product een instantie is van Goederen,of het product niet in het winkelkarretje zit, dan zal het product  toegevoegd worden of het aantal verhoogd worden:
        if product_naam in self.cart:
            self.cart[product_naam] += 1
        else:
            self.cart[product_naam] = 1

    def product_verwijderen(self, product):
        #Als het product in het winkelkarretje zit, verminderd het aantal  of wordt het product verwijderd als dit een instatie is van Diensten:
        if product in self.cart:
            if isinstance(product, Diensten) or self.cart[product] ==1:
                del self.cart[product]
            else:
                self.cart[product] -= 1
        else:
            messagebox.showinfo("Error", f"Het product '{product.get_naam()}' zit niet in het winkelkarretje")

    #Methode om objecten van de  widgets te creeren: 
    def create_widgets(self):
        self.label_producten = tk.Label(self, text="Lijst van beschikbare producten", fg="black")
        self.label_producten_cart = tk.Label(self, text="Producten in de cart", fg="green")
        self.button_product_toevoegen = tk.Button(self, text="add product", bg="#F7F9F9", command=self.add_to_cart)
        self.button_product_verwijderen = tk.Button(self, text="delete product", fg="red", command=self.delete_from_cart)

        #Listbox voor de beschikbare producten:
        self.listbox_producten = tk.Listbox(self)
        for item in self.producten_lijst:
            product_info = f"{item.get_naam()}:  {item.get_prijs()}€"
            self.listbox_producten.insert(tk.END, product_info)
        
        #Listbox voor het winkelkarretje:
        self.listbox_cart = tk.Listbox(self)

        #Plaatsen van de widgets:
        self.label_producten.grid(row=0, column=0,  padx=10, pady=10, ipadx=5, ipady=5)
        self.label_producten_cart.grid(row=0, column=2, padx=10, pady=10, ipadx=5, ipady=5)
        self.button_product_toevoegen.grid(row=2, column=1, padx=10, pady=10)
        self.button_product_verwijderen.grid(row=2, column=3, padx=10, pady=10)
        self.listbox_producten.grid(row=2, column=0, padx=10, pady=10)
        self.listbox_cart.grid(row=2, column=2, padx=10, pady=10)

    def add_to_cart(self):
        try:

            # Get de naam en de prijs van de geselecteerde product:
            selected_text = self.listbox_producten.get(self.listbox_producten.curselection())
            
            #get enkel de naam van de selected_text:
            selected_name = selected_text.split(": ")[0]

            # Vinden van de object van het product dat overeenkomt met de geselecteerde product:
            product = self.find_product_by_name(selected_name)

        # Check of het product is gevonden. Indien wel,  dit  toevoegen in het winkelkarretje:
            if product:
                self.product_toevoegen(product)
                self.update_cart_interface()  # Update de cart interface na het toeveogen van elk product
            else:
                messagebox.showinfo("error", f"Product {selected_text} niet gevonden")

        except Exception: #in het geval de user  een product probeert toe te voegen zonder dit ten eerst te seelcteren, dan prompt messagebox 
            messagebox.showwarning("Waarschuwing", "Selecteer a.u.b. een product om toe te voegen.")

    def find_product_by_name(self, name):
        for product in self.producten_lijst:
            if product.get_naam() == name:
                return product
        return None  #Als het product niet gevonden
    
    def update_cart_interface(self):
        # Clean de listbox van het winkelkarretje en update dit met de inhoud  van het winkelkarretje
        self.listbox_cart.delete(0, tk.END)
        for product_naam, qty in self.cart.items():
            self.listbox_cart.insert(tk.END, f"{product_naam} ({qty})")

    #Methode om artikelen van de winkelkarretje te verwijderen: 
    def delete_from_cart(self):

        try:
            #Verkrijgen van de geselecteerde index  van de artikel en de naam:
            selected_index = self.listbox_cart.curselection()[0]
            selected_text = self.listbox_cart.get(selected_index)

            #Verkrijgen van de naam van de product van de geselecteerde item. Text van het product in self.listbox_cart is van de vorm: "product naam, (aantal) " 
            product_naam = selected_text.split(" (")[0]

            #Update van het winkelkarretje::
            if product_naam in self.cart:
                if self.cart[product_naam] > 1:
                    self.cart[product_naam] -= 1
                else:
                    del self.cart[product_naam]
            
                #Update het interface van het winkelkarretje:
                self.update_cart_interface()
            else:
                messagebox.showinfo("Error", f"Het product '{product_naam()}' zit niet in het winkelkarretje")
        except IndexError:
            #Weergeven van een message box in het geval de user probeert een product te deleten zonder dit te selecteren:
            messagebox.showinfo("Delete Error", "Selecteer ten eerste een artikel van het winkelkarretje om dit te verwijderen")
        



if __name__=="__main__":
    root = tk.Tk()
    root.geometry("650x400")
    root.title("Winkelkarrtje app")
    app = CartApplication(master=root, producten_lijst=producten_lijst)
    app.mainloop()
import csv
import os
import locale
from time import sleep

# Funktion för att ladda data från en CSV-fil
def load_data(filename): 
    products = [] 
    
    with open(filename, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            try:
                id = int(row['id'])
                name = row['name']
                desc = row['desc']
                price = float(row['price'])
                quantity = int(row['quantity'])
                
                products.append({
                    "id": id,
                    "name": name,
                    "desc": desc,
                    "price": price,
                    "quantity": quantity
                })
            except KeyError as e:
                print(f"Missing column in CSV file: {e}")
                continue
    return products


# Funktion för att ta bort en produkt med hjälp av ID
def remove_product(products, id):
    temp_product = None

    for product in products:
        if product["id"] == id:  # Hittar produkten
            temp_product = product
            break  # Avslutar loopen när produkten hittas

    if temp_product:
        products.remove(temp_product)  # Tar bort produkten från listan
        return f"Product: {id} {temp_product['name']} was removed"
    else:
        return f"Product with id {id} not found"

# Funktion för att visa detaljer om en specifik produkt
def view_product(products, id):
    for product in products:
        if product["id"] == id:  # Jämför ID med produkterna
            return f"Visar produkt: {product['name']} {product['desc']}"    
    return "Produkten hittas inte"  # Om ingen match hittas

# Funktion för att lista alla produkter
def view_products(products):
    product_list = []
    for index, product in enumerate(products, 1):  # Numerisk indexering
        product_info = f"{index}) (#{product['id']}) {product['name']} \t {product['desc']} \t {locale.currency(product['price'], grouping=True)}"
        product_list.append(product_info)  # Skapar en sträng per produkt
    
    return "\n".join(product_list)  # Returnerar listan som en sträng

# Funktion för att lägga till en ny produkt
def add_product(products, name, desc, price, quantity):
    max_id = max(products, key=lambda x: x['id'])  # Hittar högsta ID
    id_value = max_id['id']
    id = id_value + 1  # Ökar ID med 1

    products.append(  # Lägg till ny produkt i listan
    {
        "id": id,
        "name": name,
        "desc": desc,
        "price": price,
        "quantity": quantity,
    })
 
    return f"lade till products:{id}"  # Bekräftelsemeddelande

# Sätter lokal för valuta och språk
locale.setlocale(locale.LC_ALL, 'sv_SE.UTF-8')  

# Rensar terminalen
os.system('cls' if os.name == 'nt' else 'clear')

# Laddar produktdata från CSV
products = load_data('db_products.csv')

# Huvudloopen för programmet
while True:
    try:
        os.system('cls' if os.name == 'nt' else 'clear')  # Rensar skärmen varje gång loopen startar

        print(view_products(products))  # Visa lista av produkter

        
        choice = input("Vill du (L)ägg till produkt, (V)isa eller (T)a bort en produkt? ").strip().upper()
    
        if choice == "L":  # Lägg till produkt
            name = input("Namn på produkt:")
            desc = input("Beskrivning:")
            price = float(input("pris:"))
            quantity = int(input("Antal: "))
            print(add_product(products, name, desc, price, quantity))  # Lägger till produkten

        elif choice in ["V", "T"]:  # Visa eller ta bort en produkt
            index = int(input("Enter product ID: "))  
            
            if choice == "V":  # Visa produkt
                if 1 <= index <= len(products):  # Kontrollerar att index är giltigt
                    selected_product = products[index - 1]  # Hämtar produkten från listan
                    id = selected_product['id']  # Hämtar ID för produkten
                    print(view_product(products, id))  # Visar produkten
                    done = input()
                else:
                    print("Ogiltig produkt")
                    sleep(0.3)

            elif choice == "T":  # Ta bort produkt
                if 1 <= index <= len(products):  # Kontroll av giltigt index
                    selected_product = products[index - 1]  # Hämtar produkten från listan
                    id = selected_product['id']  # Hämtar produktens ID
                    print(remove_product(products, id))  # Tar bort produkten
                    sleep(0.5)            
                else:
                    print("Ogiltig produkt")
                    sleep(0.3)
        
    except ValueError:  # Felhantering 
        print("Välj en produkt med siffor")
        sleep(0.5)
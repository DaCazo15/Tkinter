from wscrap import scrap

nombre, precio = scrap()
print('='*30)

mnd = input("Que moneda necesitas? ").upper()

if mnd in nombre:
    for new_mnd in nombre:
        if new_mnd == mnd:
            posit = nombre.index(new_mnd)
            print(f"Precio de [{new_mnd}]: {precio[posit]}")
else:
    print (f"Esta moneda [{mnd}] no esta disponible")



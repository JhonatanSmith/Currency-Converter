# Definición de los precios de los juegos en liras turcas

response = (input("¿desea ingresar algun juego? "))

names = []
price = []

while response.lower() =="si":
    # ingresa el nombre del juego
    name =  input("Ingrese el nombre del juego separado por guion bajo (_) ")
    if " " in name:
        print("Formato no válido! Separa los nombres con guion bajo (_).")
        continue  # Reiniciar el ciclo si el formato es incorrecto
    else: names.append(name)
    # ingresa el precio del juego
    try:
        game_price = float(input("Ingresa el valor del juego "))
        price.append(game_price)
    except ValueError:
        print("Precio no valido. Ingrese un numero valido ")
        
    response = (input("¿desea ingresar algun juego? "))

# Juegos ingresados por consola 
juegos_ingresados = dict(zip(names, price))

# juegos fijos
juegos_fijos = {
    #"final_fantasy": 2000,
    "dragons_dogma": 1879,
    #"ff_vii_rebirth": 1500,
    "baldurs_gate": 1800
}

# dictionario final
juegos = {**juegos_ingresados, **juegos_fijos}

print("Juegos a comprar:")
print(list(juegos.keys()))

# Tasas de cambio
un_lira_turca_dolares = 0.04
un_lira_turca_cop = 121.77

# Cálculo del total en liras turcas
total_turcas = sum(juegos.values())

# Cálculo del total en dólares
total_dolares = total_turcas * un_lira_turca_dolares

# Cálculo del total en pesos colombianos (COP)
total_cop = total_turcas * un_lira_turca_cop

# Impresión de los resultados
print("Total en lira turca:", total_turcas)
print("Total en dólares:", total_dolares)
print("Total en COP:", total_cop)
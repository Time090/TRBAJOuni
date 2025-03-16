import pandas as pd

def cargar_productos(archivo):
    try:
        df = pd.read_excel(archivo, index_col=False)  # Evita que pandas use la primera columna como índice
        df.columns = df.columns.str.strip()  # Elimina espacios extra en los nombres de columna
        columnas_existentes = set(df.columns)
        columnas_requeridas = {'ID', 'Nombre', 'Precio', 'Cantidad'}
        if not columnas_requeridas.issubset(columnas_existentes):
            print(f"Error: El archivo debe contener las columnas: ID, Nombre, Precio, Cantidad")
            print(f"Columnas encontradas en el archivo: {df.columns.tolist()}")
            return None
        return df
    except Exception as e:
        print(f"Error al cargar el archivo: {e}")
        return None

def mostrar_productos(df):
    print("Lista de productos disponibles:")
    print(df[['ID', 'Nombre', 'Precio']].to_string(index=False))  # Oculta el índice

def calcular_total(df):
    total = 0
    seleccionados = []
    while True:
        try:
            id_producto = input("Ingrese el ID del producto (o 'fin' para terminar): ")
            if id_producto.lower() == 'fin':
                break
            id_producto = int(id_producto)
            producto = df[df['ID'] == id_producto]
            if producto.empty:
                print("Producto no encontrado. Inténtelo de nuevo.")
                continue
            stock_disponible = producto.iloc[0]['Cantidad']
            if stock_disponible == 0:
                print(f"El producto {producto.iloc[0]['Nombre']} no lo tenemos disponible en este momento.")
                continue
            cantidad = int(input(f"Ingrese la cantidad de {producto.iloc[0]['Nombre']}: "))
            if cantidad > stock_disponible:
                print(f"Disculpe las molestias pero solo contamos con {stock_disponible} disponibles.")
                continue
            costo = cantidad * producto.iloc[0]['Precio']
            total += costo
            seleccionados.append((producto.iloc[0]['Nombre'], cantidad, costo))
        except ValueError:
            print("Entrada no válida. Intente de nuevo.")
    return seleccionados, total

def main():
    archivo = "productos_ferreteria.xlsx"
    df = cargar_productos(archivo)
    if df is None:
        return
    mostrar_productos(df)
    seleccionados, total = calcular_total(df)
    print("\nResumen de compra:")
    for nombre, cantidad, costo in seleccionados:
        print(f"{nombre} - Cantidad: {cantidad} - Costo: ${costo:.2f}")
    print(f"Total a pagar: ${total:.2f}")

if __name__ == "__main__":
    main()


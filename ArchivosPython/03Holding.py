# --- Importamos la librería necesaria ---
import pandas as pd

# --- Cargamos los datos necesarios ---
# operaciones.csv: historial de compras y ventas
# precios_actuales.csv: precios de mercado actualizados de cada acción
df_ops = pd.read_csv("operaciones.csv")
df_precios = pd.read_csv("precios_actuales.csv")

# --- Limpiamos nombres de columnas para evitar errores por espacios invisibles ---
df_ops.columns = df_ops.columns.str.strip()
df_precios.columns = df_precios.columns.str.strip()

# --- Aseguramos que las columnas numéricas sean del tipo correcto ---
df_ops["Cantidad"] = pd.to_numeric(df_ops["Cantidad"], errors="coerce")
df_ops["Precio Unitario"] = pd.to_numeric(df_ops["Precio Unitario"], errors="coerce")
df_ops["Comisiones"] = pd.to_numeric(df_ops["Comisiones"], errors="coerce")

# --- Eliminamos filas inválidas con valores nulos importantes ---
df_ops = df_ops.dropna(subset=["Cantidad", "Precio Unitario", "Comisiones", "Ticket", "Tipo"])

# --- Separamos las operaciones por tipo: compras vs. ventas ---
df_compras = df_ops[df_ops["Tipo"].str.lower() == "compra"]
df_ventas = df_ops[df_ops["Tipo"].str.lower() == "venta"]

# --- Inicializamos la lista donde se almacenará el resultado por cada acción ---
holdings = []

# --- Iteramos por cada ticket (acción) distinto que haya en las operaciones ---
for ticket in df_ops["Ticket"].unique():
    
    # --- Filtramos las compras de este ticket ---
    compras = df_compras[df_compras["Ticket"] == ticket]
    total_comprado = compras["Cantidad"].sum()
    
    # --- Calculamos el total invertido (incluyendo comisiones) ---
    total_invertido = (compras["Cantidad"] * compras["Precio Unitario"] + compras["Comisiones"]).sum()
    
    # --- Precio promedio de compra (ponderado) ---
    precio_promedio = total_invertido / total_comprado if total_comprado > 0 else 0

    # --- Filtramos las ventas de este ticket ---
    ventas = df_ventas[df_ventas["Ticket"] == ticket]
    total_vendido = ventas["Cantidad"].sum()

    # --- Calculamos cuántas acciones quedan actualmente ---
    cantidad_actual = total_comprado - total_vendido

    # --- Obtenemos el precio actual de esa acción desde el archivo de precios ---
    precio_actual_row = df_precios[df_precios["Ticket"] == ticket]
    if precio_actual_row.empty or pd.isna(precio_actual_row["Precio actual"].values[0]):
        precio_actual = 0
    else:
        precio_actual = precio_actual_row["Precio actual"].values[0]

    # --- Valor actual de la posición (cantidad * precio de mercado) ---
    valor_actual = cantidad_actual * precio_actual

    # --- Inversión viva: lo que quedó invertido (acciones actuales * precio promedio de compra) ---
    inversion_total_actual = cantidad_actual * precio_promedio

    # --- Ganancia bruta (lo que vale hoy menos lo invertido) ---
    ganancia_bruta = valor_actual - inversion_total_actual

    # --- ROI: retorno sobre la inversión actual (en porcentaje) ---
    roi = (ganancia_bruta / inversion_total_actual) * 100 if inversion_total_actual > 0 else 0

    # --- Guardamos el resultado en una lista de diccionarios ---
    holdings.append({
        "Ticket": ticket,
        "Cantidad actual": int(cantidad_actual),
        "Precio promedio": round(precio_promedio, 2),
        "Precio actual": round(precio_actual, 2),
        "Valor actual": round(valor_actual, 2),
        "Total invertido": round(inversion_total_actual, 2),
        "Ganancia bruta": round(ganancia_bruta, 2),
        "ROI (%)": round(roi, 2)
    })

# --- Convertimos la lista en un DataFrame final con todos los resultados ---
df_holdings = pd.DataFrame(holdings)

# --- Guardamos el DataFrame en un archivo CSV que usaremos en los siguientes pasos ---
df_holdings.to_csv("holdings.csv", index=False)

# --- Mostramos el resumen de la cartera en consola ---
print("\nResumen de Holdings:")
print(df_holdings)




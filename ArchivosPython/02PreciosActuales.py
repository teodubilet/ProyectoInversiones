# --- Importamos las librerías necesarias ---
import pandas as pd
import yfinance as yf  # Librería para obtener datos de Yahoo Finance

# --- Cargamos el archivo de operaciones generado en el paso anterior ---
df_ops = pd.read_csv("operaciones.csv")

# --- Eliminamos espacios en blanco en los nombres de las columnas ---
df_ops.columns = df_ops.columns.str.strip()

# --- Verificamos que exista la columna 'Ticket' ---
# Si no está, detenemos el script con un mensaje de error claro
if "Ticket" not in df_ops.columns:
    raise ValueError("La columna 'Ticket' no existe. Verificá tu archivo CSV.")

# --- Corrección manual de nombres de tickets que no coinciden con Yahoo Finance ---
# Por ejemplo, YPF cotiza como YPFD.BA
ticker_correcciones = {
    "YPF": "YPFD"
}

# --- Obtenemos la lista única de tickets desde el archivo de operaciones ---
# También eliminamos valores nulos para evitar errores
tickets = df_ops["Ticket"].dropna().unique()

# --- Creamos un diccionario donde guardaremos los precios actuales por ticket ---
precios_actuales = {}

# --- Iteramos sobre cada ticket para consultar su precio actual ---
for ticket in tickets:
    try:
        # Corregimos el nombre si es necesario (ej: YPF → YPFD)
        ticker_consulta = ticker_correcciones.get(ticket, ticket)
        
        # Creamos el objeto ticker de Yahoo Finance agregando ".BA" (mercado argentino)
        yf_ticket = yf.Ticker(ticker_consulta + ".BA")
        
        # Obtenemos el precio de cierre más reciente
        precio = yf_ticket.history(period="1d")["Close"].iloc[-1]
        
        # Guardamos el resultado en el diccionario
        precios_actuales[ticket] = precio
    
    except Exception as e:
        # Si hay un error (por ejemplo, ticket inválido), lo registramos
        print(f"Error con {ticket}: {e}")
        precios_actuales[ticket] = None

# --- Convertimos el diccionario a un DataFrame con columnas Ticket y Precio actual ---
df_precios = pd.DataFrame(list(precios_actuales.items()), columns=["Ticket", "Precio actual"])

# --- Guardamos los resultados en un archivo CSV para usar en los siguientes pasos ---
df_precios.to_csv("precios_actuales.csv", index=False)

# --- Mostramos los resultados por consola para verificar que se haya realizado correctamente ---
print("\nPrecios actuales:")
print(df_precios)


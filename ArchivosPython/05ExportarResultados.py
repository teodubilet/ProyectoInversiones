# --- Importamos las librerías necesarias ---
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# --- Configuración de nombres y credenciales ---
GOOGLE_SHEET_NAME = "PortfolioInversiones"       # Nombre del archivo de Google Sheets
CREDENCIALES_JSON = "credenciales.json"          # Archivo de credenciales de acceso

# --- Autenticación con la API de Google Sheets ---
# Definimos el alcance y autorizamos la conexión usando el archivo .json
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name(CREDENCIALES_JSON, scope)
client = gspread.authorize(creds)

# --- Abrimos el archivo de Google Sheets ---
sheet = client.open(GOOGLE_SHEET_NAME)

# --- Cargamos los archivos CSV generados previamente ---
df_precios = pd.read_csv("precios_actuales.csv")   # Contiene los precios actualizados desde Yahoo Finance
df_holdings = pd.read_csv("holdings.csv")          # Contiene el estado actual de la cartera por acción

# --- Definimos una función para subir un DataFrame a una hoja de cálculo ---
def actualizar_hoja(nombre_hoja, df):
    try:
        # Si la hoja ya existe, la vaciamos
        hoja = sheet.worksheet(nombre_hoja)
        hoja.clear()
    except:
        # Si no existe, la creamos
        hoja = sheet.add_worksheet(title=nombre_hoja, rows="100", cols="20")

    # Cargamos los datos (encabezado + contenido)
    hoja.update([df.columns.values.tolist()] + df.values.tolist())

# --- Subimos los datos a sus hojas correspondientes ---
actualizar_hoja("PreciosActuales", df_precios)
actualizar_hoja("Portfolio", df_holdings)

# --- Confirmación por consola ---
print("✅ Datos actualizados correctamente en Google Sheets.")


# Importamos las librerias que vamos a usar
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials  

# --- Configuración de autenticación y archivo ---
GOOGLE_SHEET_NAME = "PortfolioInversiones"         # Nombre del archivo 
OPERACIONES_HOJA = "Operaciones"                   # Nombre de la hoja dentro del archivo
CREDENCIALES_JSON = "credenciales.json"            # Archivo de credenciales que generamos desde Google Cloud

# --- Autenticación con Google Sheets API ---
# Definimos el alcance y autorizamos el acceso usando las credenciales
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name(CREDENCIALES_JSON, scope)
client = gspread.authorize(creds)

# --- Accedemos a la hoja "Operaciones" dentro del archivo de Google Sheets ---
sheet = client.open(GOOGLE_SHEET_NAME)
worksheet = sheet.worksheet(OPERACIONES_HOJA)

# --- Obtenemos todos los datos de la hoja como una lista de diccionarios () ---
datos = worksheet.get_all_records()

# --- Convertimos los datos a un DataFrame de pandas ---
df_ops = pd.DataFrame(datos)

# --- Guardamos el DataFrame en un archivo CSV local para usar en otros archivos ---
df_ops.to_csv("operaciones.csv", index=False)

# --- Mostramos los primeros registros por consola para verificar que se cargaron correctamente ---
print("✅ Datos cargados desde Google Sheets:")
print(df_ops.head())

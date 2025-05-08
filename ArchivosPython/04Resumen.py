# --- Importamos las librerías necesarias ---
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# --- Configuración de nombres y credenciales ---
GOOGLE_SHEET_NAME = "PortfolioInversiones"       # Nombre del archivo de Google Sheets
CREDENCIALES_JSON = "credenciales.json"          # Archivo de credenciales para autenticación

# --- Autenticación con Google Sheets API ---
# Definimos los permisos (scope) y autorizamos el acceso usando el archivo JSON
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name(CREDENCIALES_JSON, scope)
client = gspread.authorize(creds)

# --- Abrimos el archivo de Google Sheets ---
sheet = client.open(GOOGLE_SHEET_NAME)

# --- Cargamos el archivo CSV generado con los holdings actuales ---
df_holdings = pd.read_csv("holdings.csv")

# --- Calculamos los KPIs globales de la cartera ---
total_invertido = df_holdings["Total invertido"].sum()               # Suma total del capital invertido actual
valor_actual_total = df_holdings["Valor actual"].sum()               # Valor actual total de la cartera
ganancia_total = valor_actual_total - total_invertido                # Ganancia bruta total
roi_total = (ganancia_total / total_invertido) * 100 if total_invertido > 0 else 0  # ROI global en %

# --- Creamos un DataFrame con el resumen para subir a Google Sheets ---
df_resumen = pd.DataFrame({
    "Métrica": [
        "Total invertido",
        "Valor actual total",
        "Ganancia bruta total",
        "ROI global (%)"
    ],
    "Valor": [
        round(total_invertido, 2),
        round(valor_actual_total, 2),
        round(ganancia_total, 2),
        round(roi_total, 2)
    ]
})

# --- Subimos el resumen a la hoja "Resumen" ---
# Si ya existe, la vaciamos; si no existe, la creamos
try:
    hoja = sheet.worksheet("Resumen")
    hoja.clear()
except:
    hoja = sheet.add_worksheet(title="Resumen", rows="20", cols="5")

# --- Cargamos el nuevo contenido (encabezado + filas) ---
hoja.update([df_resumen.columns.values.tolist()] + df_resumen.values.tolist())

# --- Confirmamos por consola ---
print("✅ Resumen cargado correctamente en Google Sheets.")


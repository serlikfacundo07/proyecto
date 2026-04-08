import streamlit as st
import cv2
import numpy as np
import mysql.connector
from datetime import datetime

# --- CONFIGURACIÓN DE LA PÁGINA WEB ---
st.set_page_config(page_title="Dashboard Retail", layout="centered")

st.title("📊 Panel de Analítica Comercial")
st.write("Seleccioná una fecha en el calendario para visualizar las zonas calientes del local.")

# --- 1. EL CALENDARIO INTERACTIVO ---
# Crea un calendario en la web. Por defecto muestra el día de hoy.
fecha_seleccionada = st.date_input("Fecha a analizar:")

# --- 2. CONEXIÓN A LA BASE DE DATOS ---
# Usamos caché para que la web no se trabe conectándose a cada rato
@st.cache_resource
def init_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="proyecto"
    )

try:
    db = init_connection()
    cursor = db.cursor()
except Exception as e:
    st.error("No se pudo conectar a la base de datos. Verificá que XAMPP/MySQL esté encendido.")
    st.stop()

# --- 3. BOTÓN Y LÓGICA DE BÚSQUEDA ---
if st.button("Generar Mapa de Calor"):
    
    # Buscamos en SQL solo los datos del día seleccionado en el calendario
    consulta = "SELECT pos_x, pos_y FROM paradas WHERE DATE(fecha_hora) = %s"
    cursor.execute(consulta, (fecha_seleccionada,))
    paradas = cursor.fetchall()

    if len(paradas) > 0:
        st.success(f"¡Éxito! Se detectaron {len(paradas)} interacciones de clientes este día.")
        
        # --- 4. GENERACIÓN DEL MAPA TÉRMICO (CON IMPULSO BASE) ---
        ANCHO_VIDEO = 640
        ALTO_VIDEO = 480
        acumulador_calor = np.zeros((ALTO_VIDEO, ANCHO_VIDEO), dtype=np.float32)

        for (x, y) in paradas:
            # 1. Sumamos MUY poco por persona (5 puntos). 
            # Vas a necesitar más de 35 personas en el mismo lugar para que llegue a rojo.
            cv2.circle(acumulador_calor, (x, y), radius=15, color=5, thickness=-1)

        # 2. Desenfoque para mezclar los puntos
        acumulador_calor = cv2.GaussianBlur(acumulador_calor, (99, 99), 0)
        
        # 3. EL TRUCO MAGICO: El Impulso Base
        # Si un lugar tiene algo de calor (> 0.1), le sumamos 70 de base. 
        # Esto asegura que las zonas de "poco tráfico" se vean celestes y no azules invisibles.
        acumulador_calor = np.where(acumulador_calor > 0.1, acumulador_calor + 70, acumulador_calor)
        
        # 4. Limitamos y pintamos
        acumulador_limitado = np.clip(acumulador_calor, 0, 255).astype(np.uint8)
        mapa_color = cv2.applyColorMap(acumulador_limitado, cv2.COLORMAP_JET)

        # 5. Mezcla de imagen (Subí un poquito la visibilidad del calor a 0.5 para que resalte más)
        try:
            fondo = cv2.imread('fondo.jpg')
            # Forzamos a que la foto tenga el mismo tamaño que el mapa de calor
            fondo = cv2.resize(fondo, (ANCHO_VIDEO, ALTO_VIDEO))
            
        except Exception:
            # Si la foto no existe, fallamos a un fondo gris por seguridad
            st.warning("No se encontró 'foto_del_local_vacio.jpg'. Usando fondo gris.")
            fondo = np.full((ALTO_VIDEO, ANCHO_VIDEO, 3), 40, dtype=np.uint8)

        mascara = acumulador_limitado > 0
        mascara_3d = np.stack([mascara, mascara, mascara], axis=2)
        resultado_final = np.where(mascara_3d, cv2.addWeighted(fondo, 0.5, mapa_color, 0.5, 0), fondo)

        # --- 5. TRUCO CLAVE: Conversión de color ---
        # OpenCV trabaja en formato BGR (Azul-Verde-Rojo), pero la web usa RGB.
        # Tenemos que dar vuelta los colores antes de mandarlos a la página web.
        resultado_rgb = cv2.cvtColor(resultado_final, cv2.COLOR_BGR2RGB)

        # --- 6. MOSTRAR LA IMAGEN EN LA WEB ---
        st.image(resultado_rgb, caption=f"Mapa de calor correspondiente al {fecha_seleccionada}", use_container_width=True)
        
    else:
        # Si elijo un domingo y estaba cerrado, le aviso al usuario
        st.warning("No hay movimiento registrado para la fecha seleccionada.")
import cv2
import time
import math
import mysql.connector
from datetime import datetime
from ultralytics import YOLO

print("Cargando modelo YOLO...")
model = YOLO('yolov8n.pt') 

# --- USANDO LA CÁMARA DE LA NOTEBOOK ---
# cap = cv2.VideoCapture(0)
# --- PARA USAR DROIDCAM POR IP / WIFI (Descomentar y cambiar por la IP que te da la app) ---
cap = cv2.VideoCapture('http://192.168.100.129:4747/video')


# --- CONFIGURACIÓN DE BASE DE DATOS MYSQL ---
try:
    db = mysql.connector.connect(
        host="localhost",
        user="root",        # Reemplazá con tu usuario
        password="",        # Reemplazá con tu contraseña
        database="proyecto"   # Reemplazá con el nombre de tu base de datos
    )
    cursor = db.cursor()
    # Creamos la tabla automáticamente si no existe
    cursor.execute('''CREATE TABLE IF NOT EXISTS paradas (
        id INT AUTO_INCREMENT PRIMARY KEY,
        pos_x INT,
        pos_y INT,
        fecha_hora DATETIME
    )''')
    db.commit()
    print("Conectado a la base de datos MySQL.")
except mysql.connector.Error as err:
    print(f"Error conectando a MySQL: {err}")
    db = None

# --- PARÁMETROS DE DETECCIÓN DE QUIETUD ---
STILLNESS_RADIUS = 50  # Tolerancia en píxeles para considerar que NO se movió
STILLNESS_TIME = 15    # Segundos que debe estar quieto
tracked_persons = {}   # Diccionario para guardar el historial de cada persona

print("Iniciando cámara y detección...")

frame_count = 0
last_resultados = None

while True:
    # Leemos cada frame de la cámara
    ret, frame = cap.read()
    if not ret:
        print("Error al leer de la cámara.")
        break
        
    frame_count += 1
            
    # Procesamos con YOLO 1 de cada 3 frames para mejorar el rendimiento
    if frame_count % 3 == 0:
        # Cambiamos model() por model.track() para que YOLO les asigne un ID a las personas
        last_resultados = model.track(frame, persist=True, classes=0, imgsz=320, verbose=False)    
        
    if last_resultados is not None:
        r = last_resultados[0]
        frame = r.plot(img=frame)
        
        # Verificamos si detectó personas y si el tracker les asignó un ID
        if r.boxes is not None and r.boxes.id is not None:
            boxes = r.boxes.xyxy.cpu().numpy()
            ids = r.boxes.id.cpu().numpy()
            current_ids = []
            
            for box, obj_id in zip(boxes, ids):
                current_ids.append(obj_id)
                x1, y1, x2, y2 = box
                cx, cy = int((x1 + x2) / 2), int(y2) # Usamos la base de los pies como centro Y
                
                if obj_id not in tracked_persons:
                    tracked_persons[obj_id] = {'start_pos': (cx, cy), 'start_time': time.time(), 'last_time': time.time(), 'saved': False}
                else:
                    person = tracked_persons[obj_id]
                    px, py = person['start_pos']
                    dist = math.hypot(cx - px, cy - py)
                    
                    if dist < STILLNESS_RADIUS: # Sigue en el mismo lugar
                        person['last_time'] = time.time()
                        tiempo_quieto = person['last_time'] - person['start_time']
                        
                        # Si superó el tiempo estipulado (15 segs) y no se guardó todavía
                        if tiempo_quieto >= STILLNESS_TIME and not person['saved']:
                            if db is not None:
                                now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                                try:
                                    cursor.execute("INSERT INTO paradas (pos_x, pos_y, fecha_hora) VALUES (%s, %s, %s)", (cx, cy, now))
                                    db.commit()
                                    print(f"¡Persona ID {int(obj_id)} se detuvo! Guardado en DB en coord ({cx}, {cy})")
                                except mysql.connector.Error as err:
                                    print(f"Error al guardar en DB: {err}")
                            person['saved'] = True
                    else:
                        # Se movió, reiniciamos el contador de tiempo y su nueva posición
                        person['start_pos'] = (cx, cy)
                        person['start_time'] = time.time()
                        person['last_time'] = time.time()
                        person['saved'] = False
                        
            # Limpiar memoria de personas que salieron de la cámara (no vistas por más de 2 segundos)
            ahora = time.time()
            for obj_id in list(tracked_persons.keys()):
                if obj_id not in current_ids and (ahora - tracked_persons[obj_id]['last_time'] > 2.0):
                    del tracked_persons[obj_id]
    
    # Mostramos el frame resultante
    cv2.imshow('Analitica Retail - Deteccion', frame)
    
    # Salimos del bucle si se presiona la tecla 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Liberamos los recursos al finalizar
cap.release()
cv2.destroyAllWindows()

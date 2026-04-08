# 📷 Sistema de Detección y Seguimiento con IA

*(Escribí acá una breve descripción de tu proyecto. Ejemplo: Este proyecto es una solución integral de software y hardware diseñada para el monitoreo y seguimiento de personas/objetos, utilizando visión computacional y modelos de inteligencia artificial, conectado a una base de datos relacional).*

## 🛠️ Tecnologías Utilizadas
* **Lenguaje:** Python
* **Inteligencia Artificial:** YOLOv8 (Ultralytics)
* **Visión Computacional:** OpenCV
* **Tracking:** LAP
* **Base de Datos:** MySQL
* **Interfaz web:** Streamlit *(borrá esto si no lo usás)*

## 📋 Requisitos Previos
Antes de ejecutar este proyecto en una computadora nueva, asegurate de tener instalado:
1. Python (versión 3.8 o superior).
2. Git.
3. Un servidor MySQL local (como XAMPP o MySQL Workbench) o remoto funcionando.

---

## 🚀 Instalación y Configuración Paso a Paso

### 1. Clonar el repositorio
Abrí la terminal, ubicate en la carpeta donde quieras guardar el proyecto y descargalo:
```bash
git clone [https://github.com/TU_USUARIO/TU_REPOSITORIO.git](https://github.com/TU_USUARIO/TU_REPOSITORIO.git)
cd TU_REPOSITORIO

2. Crear el entorno virtual
Es fundamental crear un entorno virtual para aislar las librerías del proyecto y no generar conflictos con otras instalaciones de Python.

En Windows:

Bash
python -m venv venv
En Linux / Mac:

Bash
python3 -m venv venv
3. Activar el entorno virtual
En Windows (PowerShell):

Bash
.\venv\Scripts\activate
(Nota: Si Windows arroja un error de ejecución de scripts, abrí PowerShell como Administrador, ejecutá Set-ExecutionPolicy RemoteSigned -Scope CurrentUser, escribí 'S' para confirmar y volvé a intentar).

En Linux / Mac:

Bash
source venv/bin/activate
4. Instalar las dependencias
Una vez que veas el indicador (venv) en tu terminal, instalá todas las librerías necesarias ejecutando:

Bash
pip install -r requirements.txt

▶️ Ejecución
Una vez que el entorno está activado y las dependencias instaladas, iniciá el script principal:

Bash
python index.py
(Nota: Si la interfaz gráfica la estás levantando con Streamlit, el comando de ejecución es streamlit run index.py)

# EQ Clone - Instrucciones de Uso

## 1. Instalación de Dependencias

Asegúrate de tener Python instalado. Luego, abre una terminal en esta carpeta y ejecuta:

```bash
pip install -r requirements.txt
```

> **Nota:** Si tienes problemas cargando archivos MP3, es posible que necesites instalar [FFmpeg](https://ffmpeg.org/download.html) y agregarlo a tu PATH del sistema.

## 2. Ejecutar la Aplicación

### Opción A (Fácil - Windows)
Simplemente haz doble clic en el archivo `run_app.bat` que he creado en la carpeta. Esto instalará las dependencias y abrirá la app automáticamente.

### Opción B (Manual)
Si prefieres usar la terminal:

```bash
# 1. Instalar dependencias
py -m pip install -r requirements.txt

# 2. Correr la app
py -m streamlit run app.py
```

Esto abrirá automáticamente una pestaña en tu navegador web (usualmente en `http://localhost:8501`).

## 3. Cómo Usar

1.  **Cargar Audios:**
    *   Arrastra tu archivo de **Referencia** (el audio cuyo tono quieres copiar) al panel izquierdo.
    *   Arrastra tu archivo **Target** (el audio que quieres corregir) al panel derecho.
2.  **Ajustar Parámetros (Sidebar):**
    *   **Amount:** Define qué tan fuerte será el efecto (100% es una copia exacta del perfil espectral).
    *   **Safe Range:** Protege las frecuencias muy graves o muy agudas para evitar ruido o "barro".
    *   **Smoothing:** Suaviza la curva de EQ para un sonido más natural.
3.  **Procesar:**
    *   Haz clic en el botón **"⚡ Analizar y Generar"**.
4.  **Resultados:**
    *   Verás un gráfico comparando los espectros.
    *   **NUEVO:** Podrás escuchar una **Pre-escucha** del audio Target con el efecto aplicado.
    *   Finalmente, descarga el archivo `.wav` (Impulse Response) para usarlo en tu software de edición favorito (DAW) con un plugin de convolución (como Fruity Convolver, IRLoader, etc.).

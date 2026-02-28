Rol: Eres un Ingeniero Senior de Audio DSP y Desarrollador Full-Stack experto en Python.

Objetivo: Crear una aplicación web interactiva usando la librería Streamlit que realice "EQ Matching" (Clonación de Ecualización) entre una pista de referencia y una pista objetivo. La aplicación no debe procesar el archivo completo para descarga, sino generar un archivo Impulse Response (.wav) para ser usado en plugins de convolución (VST).

Stack Tecnológico:

Python 3.9+

Streamlit (Interfaz Web)

Librosa (Procesamiento de Audio)

Scipy (Filtros y suavizado)

Numpy (Cálculo matricial)

Soundfile (Exportación de audio)

Matplotlib (Visualización de datos)

Requerimientos Funcionales y Flujo Lógico (DSP):

Ingesta de Audio:

Permitir subir dos archivos: Referencia y Target (WAV/MP3).

Cargar ambos audios en mono para el análisis espectral.

CRÍTICO: Normalizar la tasa de muestreo (Sample Rate) para que coincidan.

Headroom: Aplicar automáticamente una ganancia de -1.0 dB a las señales cargadas antes de procesar para evitar clipping interno.

Análisis Espectral:

Calcular la STFT (Short-Time Fourier Transform).

Obtener el promedio de magnitud espectral (Spectral Envelope).

Aplicar suavizado usando scipy.signal.savgol_filter (window_length=51, polyorder=3) para obtener curvas musicales y no ruidosas.

Cálculo del Filtro de Igualación (Matching):

Calcular el ratio: Curva_EQ = (Espectro_Ref / Espectro_Target).

Control de Amount (Cantidad): Implementar un parámetro ajustable por el usuario (0.0 a 1.0). La fórmula debe ser Curva_Final = Curva_EQ ** Amount (uso de exponentes para escalar dB linealmente).

Safe Range (Rango Seguro): Implementar dos controles de corte de frecuencia (Min Freq y Max Freq).

Frecuencias < Min Freq: La curva de EQ debe ser forzada a 1.0 (sin cambios).

Frecuencias > Max Freq: La curva de EQ debe ser forzada a 1.0.

Esto evita distorsión en sub-graves y ruido en agudos extremos.

Generación del Impulse Response (IR):

No proceses el audio "Target" completo. En su lugar, genera un Impulso de Dirac (un array de ceros con un 1.0 en el inicio).

Aplica la curva de EQ calculada (con Amount y Safe Range) a este impulso mediante convolución o filtrado en frecuencia (ISTFT).

El resultado es un archivo .wav corto que contiene la "huella" de la EQ.

Interfaz Gráfica (UI con Streamlit):

Sidebar: Controles deslizantes para:

Amount (0% a 100%, default 100%).

Safe Range Low (20Hz a 500Hz, default 40Hz).

Safe Range High (10kHz a 20kHz, default 18kHz).

Smoothing (Opcional: ajustar la intensidad del suavizado).

Área Principal:

Uploaders de archivos.

Botón "Analizar y Generar".

Visualizador: Un gráfico de Matplotlib interactivo o estático que muestre 3 curvas:

Referencia (Verde).

Target Original (Rojo punteado).

Target Estimado/Clonado (Azul).

Sombrear en gris las zonas excluidas por el "Safe Range".

Descarga: Un botón para descargar el archivo Impulse_Response.wav generado.

Manejo de Errores:

Manejar la excepción si los archivos tienen duraciones muy diferentes o formatos corruptos.

Asegurar que no haya división por cero en el cálculo espectral (añadir epsilon).

Asegurar que el IR exportado esté normalizado para no saturar al cargarlo en un DAW.

Salida Esperada:
Genera un único script de Python (app.py) bien documentado, modular (funciones separadas para carga, cálculo, ploteo) y listo para ejecutarse con el comando streamlit run app.py.
GARDI: Generador Automatizado de Recursos Didácticos Inclusivos
GARDI es una herramienta de Inteligencia Artificial diseñada para el sector educativo. Permite a los docentes generar material visual original bajo demanda y, simultáneamente, crea descripciones automáticas (Alt-Text) para garantizar que el contenido sea accesible para estudiantes con discapacidad visual.

Flujo de Trabajo
El sistema integra tres microservicios de IA en un solo pipeline automatizado:

Fragmento de código

graph TD;
    A[Docente: Ingresa Prompt] -->|Texto| B(Replicate API);
    B -->|Genera Imagen| C[Stable Diffusion 3.5];
    C -->|Imagen| D(Hugging Face Pipeline);
    D -->|Modelo BLIP| E[Descripción Automática Alt-Text];
    E -->|Output| F[Material Didáctico Accesible];
    G[Estudiante: Feedback] -->|Texto| H(Hugging Face Sentiment);
    H -->|Análisis| I[Reporte de Calidad];
Tecnologías y Modelos Utilizados
Este proyecto implementa una arquitectura híbrida (Nube + Local) para optimizar costos y latencia:



Generación de Imágenes: Replicate API

Modelo: stability-ai/stable-diffusion-3.5-large.

Función: Creación de imágenes de alta fidelidad a partir de texto.

Accesibilidad Visual (Image Captioning): Hugging Face

Modelo: Salesforce/blip-image-captioning-base.

Función: Visión por computadora para describir el contenido de la imagen.

Análisis de Feedback (NLP): Hugging Face

Modelo: tabularisai/multilingual-sentiment-analysis.

Función: Clasificación de comentarios de estudiantes (Positivo/Negativo/Neutro).

Requisitos Previos
Cuenta en Google Colab (recomendado para uso de GPU T4 gratuita).

Python 3.8+.

API Token de Replicate (Necesario para la generación de imágenes).

Instalación
Clonar el repositorio:

Bash

git clone https://github.com/TU_USUARIO/GARDI.git
cd GARDI
Instalar dependencias: Ejecuta el siguiente comando en tu terminal o celda de Colab:

Bash

pip install replicate transformers torch pillow requests
Uso de la Herramienta
1. Configuración de Credenciales
Debes exportar tu token de Replicate como variable de entorno antes de ejecutar el script.

Python

import os
# Token de ejemplo basado en la configuración del proyecto
os.environ["REPLICATE_API_TOKEN"] = "r8_3b9YTVSzL5mcHEzcWi9Qnca5A8D1BLG1IpEko"
2. Ejecución del Script Principal
El script solicitará un "prompt" (tema) al usuario para iniciar el proceso.

Python

python main.py
3. Ejemplo de Interacción
Entrada (Docente):

"Un sistema solar realista con el sol brillando al fondo"

Salida del Sistema:


Imagen: [Se descarga y muestra la imagen generada automáticamente].


Descripción Accesible (BLIP): "a solar system with planets and the sun in the background".


Validación: Si un estudiante comenta "Me ayuda mucho a entender", el sistema retorna: Sentimiento: POSITIVE.

Comparativa de Rendimiento
El proyecto justifica la elección de modelos especializados (Hugging Face) frente a modelos masivos (LLMs) basándose en las siguientes pruebas de eficiencia realizadas durante el desarrollo :


Plataforma	Tarea	Tiempo de Respuesta	Uso de Recursos
Hugging Face (BLIP/BERT)	Análisis y Descripción	< 1 segundo (Óptimo)	Bajo (CPU)
ModelScope (Qwen-LLM)	Inferencia General	~240 segundos (Ineficiente)	Alto (GPU VRAM)

EXPORTAR A HOJAS DE CÁLCULO

Licencia
Este proyecto es de uso educativo desarrollado para el Caso Integrador de Inteligencia Artificial.
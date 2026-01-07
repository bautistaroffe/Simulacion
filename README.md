# Simulación de Biblioteca Universitaria con Múltiples Líneas de Espera

## Descripción General

Este proyecto implementa un **modelo de simulación de eventos discretos** que representa el funcionamiento de una **biblioteca universitaria** con múltiples líneas de espera (colas), en la cual los estudiantes acceden a distintos servicios atendidos por personal con diferentes capacidades y restricciones operativas.

El objetivo principal del sistema es **analizar el comportamiento de las colas**, los **tiempos de espera**, la **ocupación de los servidores** y el impacto de **interrupciones de servicio**, permitiendo evaluar el desempeño del sistema bajo distintos escenarios y parámetros de entrada.

El proyecto fue desarrollado como trabajo práctico de la materia **Simulación**, y sigue un enfoque clásico de simulación con **reloj de eventos**, **variables de estado**, **eventos de llegada y fin de atención**, y **recolección de métricas estadísticas**.

---

## Alcance del Sistema

El sistema simula el flujo de estudiantes dentro de una biblioteca universitaria que cuenta con **cinco tipos de servicios**, cada uno con su propia línea de espera, servidores y tasas de atención:

- Préstamo de libros  
- Devolución de libros  
- Consulta en sala  
- Acceso a computadoras  
- Información general  

Cada servicio se modela de forma independiente, pero todos interactúan dentro del mismo entorno de simulación y comparten el reloj global del sistema.

---

## Parámetros de Entrada

### Configuración General
- **N**: Número total de iteraciones de la simulación.
- **mostrar_desde**: Iteración inicial a partir de la cual se muestran resultados parciales.
- **mostrar_hasta**: Iteración final para visualización.
- **Umbral para probabilidad en cola**: Valor X para calcular la probabilidad de que la cola supere cierta cantidad de personas.
- **Interrupción de servicio**: Interrupción global de una hora cada 4 horas de simulación.

### Líneas de Espera
Para cada tipo de servicio se definen:
- Tasa de llegada (distribución exponencial).
- Tasa de atención (distribución exponencial).
- Cantidad de servidores disponibles.

---

## Especificación del Modelo (Enunciado)

Los estudiantes llegan a la biblioteca siguiendo una **distribución exponencial**, con las siguientes tasas de llegada:

- Préstamo de libros: 20 estudiantes/hora  
- Devolución de libros: 15 estudiantes/hora  
- Consulta en sala: 10 estudiantes/hora  
- Acceso a computadoras: 8 estudiantes/hora  
- Información general: 25 estudiantes/hora  

### Configuración de Servicios

- **Préstamo de Libros**
  - 3 bibliotecarios
  - Tasa de atención: 10 estudiantes/hora por servidor

- **Devolución de Libros**
  - 2 bibliotecarios
  - Tasa de atención: 12 estudiantes/hora por servidor

- **Consulta en Sala**
  - 2 asistentes
  - Tasa de atención: 8 estudiantes/hora por servidor

- **Acceso a Computadoras**
  - 1 responsable de TI
  - Tasa de atención: 5 estudiantes/hora
  - Restricción: máximo 6 computadoras disponibles

- **Información General**
  - 2 bibliotecarios
  - Tasa de atención: 15 estudiantes/hora por servidor

---

## Supuestos del Modelo

- Los tiempos entre llegadas y los tiempos de atención siguen **distribuciones exponenciales** con tasas conocidas.
- Cada tipo de servicio posee su **propia cola independiente**.
- Los servidores pueden encontrarse en estado **Libre** u **Ocupado**.
- Las computadoras son un recurso limitado (máximo 6).
- Las interrupciones afectan temporalmente la atención de los servicios.

---

## Objetos, Estados y Eventos Modelados

### Objetos

- **Estudiante (E)**
  - Estados: `Espera`, `Siendo Atendido`

- **Servidor (S)**
  - Estados: `Libre`, `Ocupado`

### Eventos

- Llegada de estudiante (distribución exponencial)
- Fin de atención (distribución exponencial)
- Llegada de interrupción
- Fin de interrupción

---

## Variables de Estado Controladas

- Reloj de simulación
- Estado de cada servidor
- Cantidad de personas en cola por servicio
- Tiempo restante de atención por servidor
- Cantidad de computadoras ocupadas
- Total de estudiantes atendidos
- Acumulación de tiempos de espera
- Acumulación de ocupación de servidores

El **vector de estado** completo puede consultarse en el siguiente enlace:
https://docs.google.com/spreadsheets/d/1d0-bGxgkkrQv5oB-L5XL73bEHFpCURwgqTt-P0xtFIw/edit

---

## Métricas y Resultados de Salida

El sistema calcula, entre otras, las siguientes métricas:

- Tiempo promedio de espera por servicio
- Porcentaje de ocupación de cada servidor
- Servicio con menor tiempo promedio de espera
- Probabilidad de que la cola supere un umbral X
- Impacto de interrupciones sobre los tiempos de atención

---

## Consignas Analizadas

1. ¿Cuál es el tiempo promedio en cola de cada servicio?
2. ¿Cómo afecta al servidor de devolución una interrupción de una hora cada 4 horas?
3. ¿Cuál es la probabilidad de que haya más de X personas esperando en la cola del servicio de información general?

---

## Arquitectura del Proyecto

simulacion/
├── api.py # Definición de la aplicación FastAPI
├── main.py # Punto de entrada alternativo
├── core/ # Lógica central de simulación
├── utils/ # Utilidades y funciones auxiliares
├── config/ # Configuración de parámetros
├── resultados/ # Resultados y salidas de la simulación
├── frontend/ # Interfaz web (Vite)
├── requirements.txt # Dependencias backend
└── README.md


---

## Cómo Ejecutar el Proyecto

### Backend (FastAPI)


cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python -m uvicorn api:app --reload`


El backend se ejecuta en:

http://127.0.0.1:8000


Documentación automática:

http://127.0.0.1:8000/docs

Frontend (Vite)
cd frontend
npm install
npm run dev

Tech Stack
Backend

Python 3

FastAPI

Uvicorn

Frontend

Vite

JavaScript / React (según configuración)

Librerías Principales

FastAPI: framework web para la API

Uvicorn: servidor ASGI

NumPy: soporte para cálculos numéricos

Pydantic: validación de datos

Starlette: base ASGI utilizada por FastAPI

Estado del Proyecto

✔ Simulación funcional
✔ Métricas implementadas
✔ Arquitectura modular
✔ Preparado para extensión y análisis de escenarios
# simulador_api.py
from fastapi import FastAPI
from core.simulador import Simulador  # Tu clase existente
import json
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Configurar orígenes permitidos

origins = [
    "http://localhost:5173",  # o el puerto de tu Vite/React app
    "http://127.0.0.1:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # o ["*"] para permitir todo durante pruebas
    allow_credentials=True,
    allow_methods=["*"],  # <- ¡esto permite OPTIONS también!
    allow_headers=["*"],
)

# Cargar configuración por defecto
# Ejecutar con
@app.get("/")
def home():
    return {"mensaje": "Bienvenido a la API del simulador"}

@app.post("/simular")
def ejecutar_simulacion(config: dict):
    simulador = Simulador(config)
    simulador.ejecutar()
    metricas = simulador.calcular_metricas()
    prob_cola_info_mayor_a_3 = simulador.calcular_probabilidad_cola_superior("informacion", 3)

    return {
        "vector_estado": simulador.get_vector_estado(config["desde"], config["hasta"]),
        "metricas": metricas,
        "probabilidad_cola_info_mayor_a_3": prob_cola_info_mayor_a_3

    }
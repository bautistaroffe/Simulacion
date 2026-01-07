CONFIG = {
    "N": 10000,# Número total de eventos a simular
    "duracion_maxima": 12 * 60,
    "interrupciones": [
        {
            "servicio": "devolucion",
            "cada": 240,
            "duracion": 60
        }
    ],
    "servicios": {
        "prestamo": {
            "tasa_llegada": 20,       # estudiantes por hora
            "servidores": 3,
            "tasa_atencion": 10       # cada bibliotecario atiende a 10/hora
        },
        "devolucion": {
            "tasa_llegada": 15,
            "servidores": 2,
            "tasa_atencion": 12,

        },
        "consulta": {
            "tasa_llegada": 10,
            "servidores": 2,
            "tasa_atencion": 8
        },
        "computadoras": {
            "tasa_llegada": 8,
            "servidores": 6,          # una persona pero 6 equipos disponibles
            "tasa_atencion": 5
        },
        "informacion": {
            "tasa_llegada": 25,
            "servidores": 2,
            "tasa_atencion": 15
        },
        # Este es el nuevo servicio del punto 7
        "nuevo_servicio": {
            "tasa_llegada": None,     # no tiene llegada externa, viene desde otros
            "servidores": 1,
            "tasa_atencion": 7
        },


    }
}


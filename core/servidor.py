import numpy as np
import random

class Servidor:
    def __init__(self, nombre, cantidad_servidores, tasa_servicio, tasa_llegada=None):
        self.nombre = nombre
        self.cantidad = cantidad_servidores
        self.tasa_servicio = tasa_servicio
        self.tasa_llegada = tasa_llegada  # puede ser None si no genera llegadas

        self.acumulador_cola = 0

        #self.ocupados = 0
        self.cola = []
        self.total_espera = 0.0
        self.total_atendidos = 0
        self.tiempo_ocupado = 0.0
        self.historia_cola = []
        self.actualizaciones_cola = 0
        self.en_interrupcion = False
        self.servidores = [
            {"ocupado": False, "tiempo_ocupado": 0.0, "atendidos": 0, "tiempo_fin_atencion":0}
            for _ in range(cantidad_servidores)
        ]

    def tiempo_servicio(self):
        """Devuelve un tiempo de atención aleatorio (exponencial)"""
        " -1/tasa * LN(1-RND) "

        rnd = np.random.uniform(0, 1)
        return (-1 / self.tasa_servicio) * np.log(1 - rnd) * 60, rnd

    def tiempo_llegada(self):
        """Devuelve un tiempo de llegada aleatorio (exponencial), si aplica"""
        rnd = np.random.uniform(0, 1)
        if self.tasa_llegada is not None:
            tiempo = (-1 / self.tasa_llegada) * np.log(1 - rnd) * 60
            return tiempo, rnd
        return None

    def registrar_ocupacion(self, tiempo, idx=None):
        if idx is not None:
            self.servidores[idx]["tiempo_ocupado"] += tiempo


    def registrar_espera(self, tiempo):
        self.total_espera += tiempo

    def registrar_estado_cola(self):
        self.historia_cola.append(len(self.cola))

    def agregar_a_cola(self, cliente_id, hora_llegada):
        self.cola.append((cliente_id, hora_llegada))
        self.acumulador_cola += 1  # 👈 acumulás una persona nueva
        self.registrar_estado_cola()
        self.actualizaciones_cola += 1

    def sacar_de_cola(self):
        self.actualizaciones_cola += 1
        if self.cola:
            return self.cola.pop(0)
        return None

    def asignar_servidor(self):
        for idx, servidor in enumerate(self.servidores):
            if not servidor["ocupado"]:
                servidor["ocupado"] = True
                return idx
        return None  # si no hay disponibles

    def liberar_servidor(self, idx, duracion):
        self.servidores[idx]["ocupado"] = False
        self.servidores[idx]["atendidos"] += 1


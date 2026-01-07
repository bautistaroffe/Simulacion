import heapq
from .eventos import Evento
from .servidor import Servidor
import itertools
import random

class Simulador:
    def __init__(self, config):
        self.config = config
        self.reloj = 0.0
        self.eventos = []
        self.servicios = {}
        self.clientes = {}
        self.contador_eventos = 0
        self.id_generator = itertools.count(1)
        self.vector_estado = []
        self.interrupciones = config.get("interrupciones", [])

        self.inicializar_servicios()
        self.inicializar_llegadas()
        self.inicializar_interrupciones()

    def inicializar_servicios(self):
        for nombre, datos in self.config["servicios"].items():
            self.servicios[nombre] = Servidor(
                nombre=nombre,
                cantidad_servidores=datos["servidores"],
                tasa_servicio=datos["tasa_atencion"],
                tasa_llegada=datos.get("tasa_llegada")
            )

    def calcular_probabilidad_cola_superior(self, servicio_objetivo, umbral):
        historia = self.servicios[servicio_objetivo].historia_cola
        if not historia:
            return 0
        veces_mayor = sum(1 for x in historia if x > umbral)
        return veces_mayor / len(historia)

    def inicializar_llegadas(self):
        for nombre, servidor in self.servicios.items():
            if servidor.tasa_llegada is not None:
                t_llegada, rnd = servidor.tiempo_llegada()
                evento = Evento("llegada", self.reloj + t_llegada, None, nombre, rnd, t_llegada)
                heapq.heappush(self.eventos, evento)

    def inicializar_interrupciones(self):
        duracion_maxima = self.config.get("duracion_maxima", 12 * 60)
        for interrupcion in self.interrupciones:
            servicio = interrupcion["servicio"]
            cada = interrupcion["cada"]
            duracion = interrupcion["duracion"]
            tiempo = cada
            while tiempo < duracion_maxima:
                evento_inicio = Evento("interrupcion", tiempo, None, servicio, None, 0)
                evento_fin = Evento("fin_interrupcion", tiempo + duracion, None, servicio, None, 0)
                heapq.heappush(self.eventos, evento_inicio)
                heapq.heappush(self.eventos, evento_fin)
                tiempo += cada

    def ejecutar(self):
        print(self.eventos)
        N = self.config["N"]

        # ⏱ Inicialización
        self.reloj = 0.0

        evento_inicio = Evento("inicio", self.reloj, None, None, None, 0)
        self.guardar_estado(evento_inicio)  # ← luego guardamos el estado, con esas llegadas ya programadas

        #  Bucle principal
        while self.contador_eventos < N and self.eventos:
            evento = heapq.heappop(self.eventos)
            self.reloj = evento.tiempo
            self.contador_eventos += 1

            procesado = True

            if evento.tipo == "llegada":
                procesado = self.procesar_llegada(evento)
            elif evento.tipo == "salida":
                self.procesar_salida(evento)
            elif evento.tipo == "interrupcion":
                self.procesar_interrupcion(evento)
            elif evento.tipo == "fin_interrupcion":
                self.procesar_fin_interrupcion(evento)

            if procesado:
                self.guardar_estado(evento)

    def procesar_llegada(self, evento):
        servicio = self.servicios[evento.servicio]
        # Si el servicio está interrumpido, reprogramar la llegada una hora después
        if servicio.en_interrupcion:
            nuevo_evento = Evento(
                "llegada",
                self.reloj + 60,
                evento.cliente_id,
                servicio.nombre,
                evento.rnd,
                evento.duracion
            )
            heapq.heappush(self.eventos, nuevo_evento)
            return False
        if evento.cliente_id is None:
            evento.cliente_id = next(self.id_generator)

        self.clientes[evento.cliente_id] = {"llegada": self.reloj}
        idx = servicio.asignar_servidor()
        if idx is not None and not servicio.en_interrupcion:
            duracion, rnd = servicio.tiempo_servicio()
            evento.rnd_servicio=rnd
            evento.duracion_servicio=duracion
            # Guardamos la duracion en el servidor, pero NO sumamos a tiempo_ocupado todavía
            servicio.servidores[idx]["duracion_actual"] = duracion
            servicio.servidores[idx]["tiempo_fin_atencion"] = self.reloj + duracion

            evento_salida = Evento("salida", self.reloj + duracion, evento.cliente_id , servicio.nombre, rnd, duracion)
            evento_salida.servidor_idx = idx
            heapq.heappush(self.eventos, evento_salida)


        else:
            servicio.agregar_a_cola(evento.cliente_id, self.reloj)

        if servicio.tasa_llegada is not None and not servicio.en_interrupcion:
            t_llegada, rnd = servicio.tiempo_llegada()
            evento.tiempo_entre_llegadas=t_llegada
            nuevo_evento = Evento("llegada", self.reloj + t_llegada, None , servicio.nombre, rnd, t_llegada)
            heapq.heappush(self.eventos, nuevo_evento)
        return True

    def procesar_salida(self, evento):
        servicio = self.servicios[evento.servicio]
        servicio.total_atendidos += 1

        # Liberar el servidor que terminó
        if evento.servidor_idx is not None:
            # Sumamos a tiempo_ocupado recién ahora
            duracion_usada = servicio.servidores[evento.servidor_idx].get("duracion_actual", 0.0)
            servicio.servidores[evento.servidor_idx]["tiempo_ocupado"] += duracion_usada
            servicio.servidores[evento.servidor_idx]["ocupado"] = False
            servicio.servidores[evento.servidor_idx]["atendidos"] += 1
            servicio.servidores[evento.servidor_idx]["duracion_actual"] = 0.0
            servicio.servidores[evento.servidor_idx]["tiempo_fin_atencion"] = None


        # Si hay cola, atender al siguiente
        if servicio.cola and not servicio.en_interrupcion:
            cliente_id, hora_llegada = servicio.sacar_de_cola()
            espera = self.reloj - hora_llegada
            servicio.registrar_espera(espera)

            idx = servicio.asignar_servidor()
            if idx is not None:
                duracion, rnd = servicio.tiempo_servicio()
                servicio.servidores[idx]["duracion_actual"] = duracion  # guardamos la duración
                servicio.servidores[idx]["tiempo_fin_atencion"] = self.reloj + duracion
                nuevo_evento = Evento("salida", self.reloj + duracion, cliente_id, servicio.nombre, rnd, duracion)
                nuevo_evento.servidor_idx = idx
                heapq.heappush(self.eventos, nuevo_evento)

        # Punto 7 - Envío al nuevo servicio (35%)
        if self.config.get("usar_nuevo_servicio", False) and evento.servicio != "nuevo_servicio":
            if random.random() < 0.35:
                nuevo_id = evento.cliente_id
                nuevo_evento = Evento(
                    tipo="llegada",
                    tiempo=self.reloj,
                    cliente_id=nuevo_id,
                    servicio="nuevo_servicio",
                    rnd=None,
                    duracion=0
                )
                heapq.heappush(self.eventos, nuevo_evento)

    def procesar_interrupcion(self, evento):
        self.servicios[evento.servicio].en_interrupcion = True

    def procesar_fin_interrupcion(self, evento):
        self.servicios[evento.servicio].en_interrupcion = False

    def guardar_estado(self, evento):
        tipo_evento_descriptivo = ""
        if evento.tipo == "llegada":
            tipo_evento_descriptivo = f"Llegada cliente {evento.cliente_id}"
        elif evento.tipo == "salida":
            tipo_evento_descriptivo = f"Salida cliente {evento.cliente_id}"
        elif evento.tipo == "interrupcion":
            tipo_evento_descriptivo = f"Llegada interrupción {evento.servicio}"
        elif evento.tipo == "fin_interrupcion":
            tipo_evento_descriptivo = f"Fin interrupción {evento.servicio}"
        elif evento.tipo == "inicio":
            tipo_evento_descriptivo = "Inicialización"

        estado = {
            "evento_numero": self.contador_eventos,
            "descripcion_evento": tipo_evento_descriptivo,
            "reloj": self.reloj,
            "tipo_evento": evento.tipo,
            "cliente_id": evento.cliente_id,
            "servicio": evento.servicio,
            "rnd": evento.rnd
        }
        # 👇 Solo mostrar si el cliente fue atendido en este evento (no si entró en la cola)
        mostrar_atencion = (
                evento.tipo == "llegada"
                and hasattr(evento, "duracion_servicio")
                and evento.duracion_servicio is not None
                and evento.duracion_servicio > 0
        )

        estado["tiempo_atencion"] = evento.duracion_servicio if mostrar_atencion else None
        estado["rnd_servicio"] = evento.rnd_servicio if mostrar_atencion else None
        estado["fin_servicio"] = self.reloj + evento.duracion_servicio if mostrar_atencion else None

        # 📌 Estado de cada servicio
        for nombre, s in self.servicios.items():
            # Estado de cada servidor
            estado[f"{nombre}_servidores_estado"] = [
                "ocupado" if servidor["ocupado"] else "libre"
                for servidor in s.servidores
            ]

            # Acumulador de ocupación por servidor
            estado[f"{nombre}_acum_ocupacion_por_servidor"] = [
                servidor["tiempo_ocupado"] for servidor in s.servidores
            ]

            # Estado de la cola actual
            estado[f"{nombre}_cola"] = len(s.cola)

            # Acumulador de cola (suma del historial)
            estado[f"{nombre}_acum_cola"] = sum(s.historia_cola)

            estado[f"{nombre}_modif_cola"] = len(s.historia_cola)

            estado[f"{nombre}_fin_atencion_por_servidor"] = [
                servidor.get("tiempo_fin_atencion") for servidor in s.servidores
            ]

            # Clientes atendidos por servidor
            estado[f"{nombre}_clientes_atendidos"] = s.total_atendidos

            estado[f"{nombre}_acum_espera"] = s.total_espera


        # 📅 Próxima llegada por servicio
        for nombre in self.servicios:
            llegadas = [ev for ev in self.eventos if ev.tipo == "llegada" and ev.servicio == nombre]
            if llegadas:
                proxima = min(llegadas, key=lambda e: e.tiempo)
                estado[f"proxima_llegada_{nombre}"] = proxima.tiempo
            else:
                estado[f"proxima_llegada_{nombre}"] = "-"
                    # Si el evento es una llegada, guardamos el tiempo entre llegadas para ese servicio
            
            #Calculo el tiempo de llegada para el servicio del evento, al resto lo defino como null
            clave_tiempo_llegada = f"tiempo_entre_llegadas_{nombre}"
            if evento.tipo == "llegada" and evento.servicio == nombre:
                estado[clave_tiempo_llegada] = evento.tiempo_entre_llegadas
            else:
                estado[clave_tiempo_llegada] = None

        self.vector_estado.append(estado)

    def calcular_metricas(self):
        esperas = {}
        metricas_por_servicio = {}

        for nombre, servicio in self.servicios.items():
            atendidos = servicio.total_atendidos
            espera_prom = servicio.total_espera / atendidos if atendidos > 0 else 0
            promedio_cola = sum(servicio.historia_cola) / len(servicio.historia_cola) if servicio.historia_cola else 0


            metricas_por_servicio[nombre] = {
                "clientes_atendidos": atendidos,
                "tiempo_espera_promedio": espera_prom,
                "promedio_gente_en_cola": promedio_cola
            }

            # Métricas por servidor individual
            servidores_individuales = []
            for i, servidor in enumerate(servicio.servidores):
                ocupacion = servidor["tiempo_ocupado"] / self.reloj if self.reloj > 0 else 0
                servidores_individuales.append({
                    "servidor": i + 1,
                    "clientes_atendidos": servidor["atendidos"],
                    "tiempo_ocupado": servidor["tiempo_ocupado"],
                    "porcentaje_ocupacion": ocupacion * 100
                })

            metricas_por_servicio[nombre]["servidores"] = servidores_individuales

            # Si tiene interrupción definida, agregarla para mostrar en el front
            for inter in self.interrupciones:
                if inter["servicio"] == nombre:
                    metricas_por_servicio[nombre]["interrupciones"] = {
                        "cada": inter["cada"],
                        "duracion": inter["duracion"]
                    }

            esperas[nombre] = espera_prom

            # Consigna 6 - probabilidad de cola en 'informacion'
            if nombre == "informacion":
                umbral = self.config.get("umbral_cola_info", 3)
                prob = self.calcular_probabilidad_cola_superior(nombre, umbral)
                metricas_por_servicio[nombre]["probabilidad_cola_mayor_a"] = prob
                metricas_por_servicio[nombre]["umbral_cola"] = umbral

        # Excluir nuevo_servicio si no está habilitado
        usar_nuevo = self.config.get("usar_nuevo_servicio", False)
        esperas_filtradas = {
            nombre: espera for nombre, espera in esperas.items()
            if usar_nuevo or nombre != "nuevo_servicio"
        }

        servicio_mas_rapido = min(esperas_filtradas, key=esperas_filtradas.get) if esperas_filtradas else None
        menor_espera = esperas_filtradas[servicio_mas_rapido] if servicio_mas_rapido else None

        return {
            "por_servicio": metricas_por_servicio,
            "servicio_mas_rapido": servicio_mas_rapido,
            "menor_tiempo_espera": menor_espera
        }

    def get_vector_estado(self, desde, hasta):
        desde_idx = max(desde - 1, 0)
        hasta_idx = max(hasta, 0)
        if desde > hasta:
            raise ValueError("'desde' debe ser menor o igual a 'hasta'")
        return self.vector_estado[desde_idx:hasta_idx]



class Evento:
    def __init__(self, tipo, tiempo, cliente_id, servicio, rnd, duracion):
        """
        tipo: 'llegada' o 'salida'
        tiempo: instante en que ocurre el evento (float)
        cliente_id: identificador del estudiante
        servicio: nombre del servicio relacionado al evento
        duracion: tiempo que tarda en ocurrir el evento (Tiempo de llegada o Duracion de servicio)
        """
        self.tipo = tipo
        self.tiempo = tiempo
        self.cliente_id = cliente_id
        self.servicio = servicio
        self.rnd = rnd
        self.duracion= duracion
        self.tiempo_entre_llegadas=0
        self.servidor_idx = None  # índice del servidor que atiende (si aplica)
        self.rnd_servicio=0
        self.duracion_servicio=0



    def __lt__(self, otro):
        """
        Para que los eventos puedan ordenarse en una heap (por tiempo).
        """
        return self.tiempo < otro.tiempo

    def __repr__(self):
        return f"<Evento {self.tipo.upper()} | t={self.tiempo:.2f} | Cliente={self.cliente_id} | Servicio={self.servicio}>"


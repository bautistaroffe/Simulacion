# Simulador de Biblioteca Universitaria

## Resumen

Este proyecto implementa una simulacion de eventos discretos para analizar la operacion de una biblioteca universitaria con multiples lineas de espera. El sistema permite estudiar como se comportan distintos servicios frente a tasas de llegada y atencion configurables, medir tiempos de espera, observar ocupacion de servidores y evaluar escenarios con interrupciones o derivaciones a un servicio adicional.

La solucion tiene dos formas de uso:

- `main.py`: ejecuta la simulacion desde consola con la configuracion por defecto.
- `api.py` + `frontend/simulador-frontend`: expone una API HTTP y una interfaz web para parametrizar la corrida y visualizar resultados.

## Problema Que Resuelve

El proyecto busca responder preguntas tipicas de analisis de colas dentro de una biblioteca:

- cuanto espera en promedio un usuario en cada servicio;
- que nivel de ocupacion tienen los servidores;
- que servicio ofrece la menor espera promedio;
- como impacta una interrupcion programada sobre un servicio;
- cual es la probabilidad de que la cola de informacion supere un umbral dado;
- que sucede si parte de los usuarios se deriva a un servicio adicional al finalizar una atencion.

Esto permite comparar escenarios operativos sin intervenir el sistema real.

## Funcionalidad

El simulador modela los siguientes servicios:

- `prestamo`
- `devolucion`
- `consulta`
- `computadoras`
- `informacion`
- `nuevo_servicio` opcional

Cada servicio define:

- tasa de llegada por hora;
- cantidad de servidores;
- tasa de atencion por hora.

### Reglas de simulacion

- Las llegadas externas se generan con distribucion exponencial.
- Los tiempos de servicio tambien se generan con distribucion exponencial.
- Cada servicio mantiene su propia cola y su propio conjunto de servidores.
- El reloj avanza al proximo evento pendiente usando una cola de prioridad (`heapq`).
- Los eventos soportados son `inicio`, `llegada`, `salida`, `interrupcion` y `fin_interrupcion`.
- Las interrupciones se programan por configuracion. En el escenario cargado por defecto, `devolucion` se interrumpe cada 240 minutos durante 60 minutos.
- Si un servicio esta interrumpido, una llegada a ese servicio se reprograma 60 minutos despues.
- Si `usar_nuevo_servicio` esta habilitado, cada salida de un servicio distinto de `nuevo_servicio` tiene 35% de probabilidad de generar una nueva llegada inmediata a `nuevo_servicio`.

### Resultados que produce

La simulacion genera dos tipos principales de salida:

- `vector_estado`: fotografia del estado del sistema en cada evento. Incluye reloj, evento procesado, proximas llegadas, estado de servidores, colas, acumuladores y tiempos de fin de atencion.
- `metricas`: resumen por servicio con clientes atendidos, espera promedio, promedio en cola, detalle por servidor, configuracion de interrupciones y probabilidad de cola superior al umbral para `informacion`.

Ademas, calcula el servicio con menor tiempo promedio de espera.

## Arquitectura

La arquitectura esta separada en tres bloques: configuracion, motor de simulacion y capa de presentacion.

```text
simulacion/
├── api.py
├── main.py
├── config/
│   └── parametros.py
├── core/
│   ├── eventos.py
│   ├── servidor.py
│   ├── simulador.py
│   └── consignas.py
├── frontend/
│   └── simulador-frontend/
│       ├── package.json
│       └── src/
│           ├── App.jsx
│           └── components/
├── resultados/
└── requirements.txt
```

### 1. Configuracion

[`config/parametros.py`](/C:/Users/roffe/OneDrive/Desktop/portfolio/proyectos/simulacion/config/parametros.py) define la configuracion por defecto del escenario:

- cantidad maxima de eventos (`N`);
- duracion maxima usada para programar interrupciones;
- servicios y sus parametros;
- interrupciones predefinidas.

### 2. Nucleo de simulacion

[`core/simulador.py`](/C:/Users/roffe/OneDrive/Desktop/portfolio/proyectos/simulacion/core/simulador.py) concentra la logica principal.

Responsabilidades:

- construir los servicios a partir de la configuracion;
- inicializar llegadas e interrupciones;
- mantener el reloj y la agenda de eventos;
- procesar llegadas, salidas e interrupciones;
- almacenar el vector de estado;
- calcular metricas agregadas y parciales.

[`core/servidor.py`](/C:/Users/roffe/OneDrive/Desktop/portfolio/proyectos/simulacion/core/servidor.py) representa cada linea de servicio. Administra:

- servidores libres u ocupados;
- cola de espera;
- tiempos de servicio y llegada;
- acumuladores de espera y ocupacion;
- historial de cola.

[`core/eventos.py`](/C:/Users/roffe/OneDrive/Desktop/portfolio/proyectos/simulacion/core/eventos.py) define la estructura de los eventos y su criterio de ordenamiento temporal.

### 3. Capa de presentacion

[`api.py`](/C:/Users/roffe/OneDrive/Desktop/portfolio/proyectos/simulacion/api.py) expone una API FastAPI con CORS habilitado para `http://localhost:5173` y `http://127.0.0.1:5173`.

Endpoints:

- `GET /`: mensaje simple de bienvenida.
- `POST /simular`: recibe una configuracion JSON, ejecuta la simulacion y devuelve `vector_estado`, `metricas` y la probabilidad de que la cola de informacion supere 3 personas.

[`frontend/simulador-frontend/src/components/SimuladorForm.jsx`](/C:/Users/roffe/OneDrive/Desktop/portfolio/proyectos/simulacion/frontend/simulador-frontend/src/components/SimuladorForm.jsx) contiene la vista principal del frontend React.

La interfaz permite:

- editar parametros generales;
- activar o desactivar interrupciones;
- activar o desactivar el nuevo servicio;
- definir el umbral de cola para informacion;
- ejecutar la simulacion contra la API;
- visualizar tarjetas de metricas y una tabla con el vector de estado.

## Flujo Interno

1. Se cargan los servicios y sus servidores desde la configuracion.
2. Se agenda la primera llegada de cada servicio con llegada externa.
3. Se agendan los eventos de interrupcion y fin de interrupcion.
4. En cada iteracion se procesa el evento mas cercano en el tiempo.
5. Cada evento actualiza el estado global y puede programar nuevos eventos.
6. Despues de cada evento procesado se guarda una fila del vector de estado.
7. Al finalizar, se calculan metricas agregadas y se expone el rango solicitado del vector.

## Ejecucion

### Requisitos

- Python 3.10 o superior recomendado
- Node.js 18 o superior recomendado
- `pip` y `npm`

### Backend por consola

Desde la raiz del proyecto:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python main.py
```

Esto ejecuta la simulacion usando la configuracion de [`config/parametros.py`](/C:/Users/roffe/OneDrive/Desktop/portfolio/proyectos/simulacion/config/parametros.py) y muestra el resumen por servicio en la terminal.

### Backend como API

Desde la raiz del proyecto:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn api:app --reload
```

La API queda disponible en:

- `http://127.0.0.1:8000`
- `http://127.0.0.1:8000/docs`

### Frontend

En otra terminal:

```powershell
cd frontend\simulador-frontend
npm install
npm run dev
```

La aplicacion web queda disponible normalmente en:

- `http://localhost:5173`

El frontend consume directamente `http://localhost:8000/simular`, por lo que el backend debe estar levantado antes de ejecutar una simulacion desde la interfaz.

## Configuracion de Entrada

La API espera un objeto JSON con esta estructura general:

```json
{
  "N": 10000,
  "desde": 1,
  "hasta": 301,
  "duracion_maxima": 720,
  "umbral_cola_info": 3,
  "usar_nuevo_servicio": true,
  "interrupciones": [
    {
      "servicio": "devolucion",
      "cada": 240,
      "duracion": 60
    }
  ],
  "servicios": {
    "prestamo": { "tasa_llegada": 20, "servidores": 3, "tasa_atencion": 10 },
    "devolucion": { "tasa_llegada": 15, "servidores": 2, "tasa_atencion": 12 },
    "consulta": { "tasa_llegada": 10, "servidores": 2, "tasa_atencion": 8 },
    "computadoras": { "tasa_llegada": 8, "servidores": 6, "tasa_atencion": 5 },
    "informacion": { "tasa_llegada": 25, "servidores": 2, "tasa_atencion": 15 },
    "nuevo_servicio": { "tasa_llegada": null, "servidores": 1, "tasa_atencion": 7 }
  }
}
```

Notas:

- `desde` y `hasta` controlan el rango del vector de estado devuelto por la API.
- `nuevo_servicio` no genera llegadas externas; solo recibe clientes derivados.
- si `desde > hasta`, el simulador lanza una excepcion.
- la API no usa modelos Pydantic para validar el payload, por lo que la estructura debe enviarse correctamente.

## Observaciones Tecnicas

- El proyecto no incluye una suite automatizada de tests.
- `core/consignas.py` y `utils/` no participan hoy en el flujo principal.
- `resultados/` contiene archivos auxiliares, pero la simulacion actual devuelve los resultados en memoria y por HTTP.

## Stack

- Python
- FastAPI
- Uvicorn
- NumPy
- React
- Vite
- Axios
- Tailwind CSS

import React, { useState } from "react";
import axios from "axios";
import TablaSimulacion from "./TablaSimulacion";
import CardEstadisticasServicio from "./CardStat";
import CardMenorTiempoEspera from "./MenorTiempo";

export default function SimuladorForm() {
  const [config, setConfig] = useState({
    N: 10000,
    desde: 1,
    hasta: 301,
    servicios: {
      prestamo: { tasa_llegada: 20, servidores: 3, tasa_atencion: 10 },
      devolucion: { tasa_llegada: 15, servidores: 2, tasa_atencion: 12 },
      consulta: { tasa_llegada: 10, servidores: 2, tasa_atencion: 8 },
      computadoras: { tasa_llegada: 8, servidores: 6, tasa_atencion: 5 },
      informacion: { tasa_llegada: 25, servidores: 2, tasa_atencion: 15 },
      nuevo_servicio: { tasa_llegada: null, servidores: 1, tasa_atencion: 7 },
    },
  });
  const [usarInterrupcion, setUsarInterrupcion] = useState(false);
  const [umbralColaInfo, setUmbralColaInfo] = useState(3);
  const [response, setResponse] = useState(null);

  const handleChange = (servicio, campo, valor) => {
    setConfig((prev) => ({
      ...prev,
      servicios: {
        ...prev.servicios,
        [servicio]: {
          ...prev.servicios[servicio],
          [campo]: valor === "" ? null : Number(valor),
        },
      },
    }));
  };
const [usarNuevoServicio, setUsarNuevoServicio] = useState(true);

const handleSubmit = async (e) => {
  e.preventDefault();

  const configConInterrupciones = {
    ...config,
    duracion_maxima: 720, // 12 horas en minutos
    umbral_cola_info: umbralColaInfo,
    usar_nuevo_servicio: usarNuevoServicio
  };



  if (usarInterrupcion) {
    configConInterrupciones.interrupciones = [
      {
        servicio: "devolucion",
        cada: 240, // cada 4 horas
        duracion: 60 // duración de 1 hora
      }
    ];
  }

  try {
    const res = await axios.post("http://localhost:8000/simular", configConInterrupciones);
    console.log("VECTOR DE ESTADO:", res.data.vector_estado);

    setResponse(res.data);
  } catch (err) {
    setResponse({ error: err.message });
  }
};


  return (
    <div className="flex h-screen bg-gray-100">
      <aside className="w-full max-w-xs bg-white border-r shadow-lg flex flex-col h-screen">
        <div className="sticky top-0 bg-gray-100 z-10 p-4 border-b">
          <h1 className="text-xl font-bold text-gray-800">Simulador de Biblioteca</h1>
        </div>

        <form onSubmit={handleSubmit} className="flex-grow overflow-y-auto p-4 space-y-6">
          <div className="space-y-4 p-4 bg-white rounded shadow">
            <h2 className="text-lg font-semibold text-gray-700 border-b pb-2">Parámetros Generales</h2>
            <div className="space-y-3">
              <label className="block text-sm font-medium text-gray-700">
                Número de eventos:
                <input
                    type="number"
                    value={config.N}
                    onChange={(e) => setConfig({...config, N: Number(e.target.value)})}
                    className="mt-1 block w-full border rounded px-3 py-2 focus:outline-none focus:ring focus:border-blue-500"
                />
              </label>
              <label className="block text-sm font-medium text-gray-700">
                Mostrar desde:
                <input
                    type="number"
                    value={config.desde}
                    onChange={(e) => setConfig({...config, desde: Number(e.target.value)})}
                    className="mt-1 block w-full border rounded px-3 py-2 focus:outline-none focus:ring focus:border-blue-500"
                />
              </label>
              <label className="block text-sm font-medium text-gray-700">
                Mostrar hasta:
                <input
                    type="number"
                    value={config.hasta}
                    onChange={(e) => setConfig({...config, hasta: Number(e.target.value)})}
                    className="mt-1 block w-full border rounded px-3 py-2 focus:outline-none focus:ring focus:border-blue-500"
                />
              </label>
              <label className="flex items-center gap-2 text-sm font-medium text-gray-700">
                <input
                    type="checkbox"
                    checked={usarNuevoServicio}
                    onChange={(e) => setUsarNuevoServicio(e.target.checked)}
                    className="accent-slate-700"
                />
                Habilitar nuevo servicio al finalizar atenciones (35%)
              </label>

              <label className="block text-sm font-medium text-gray-700">
                Umbral para probabilidad en cola (información):
                <input
                    type="number"
                    min={1}
                    max={50}
                    value={umbralColaInfo}
                    onChange={(e) => {
                      const valor = Number(e.target.value);
                      setUmbralColaInfo(Math.max(1, valor)); // mínimo 1
                    }}
                    className="mt-1 block w-full border rounded px-3 py-2 focus:outline-none focus:ring focus:border-blue-500"
                />
              </label>
              <label className="flex items-center gap-2 text-sm font-medium text-gray-700">
                <input
                    type="checkbox"
                    checked={usarInterrupcion}
                    onChange={(e) => setUsarInterrupcion(e.target.checked)}
                    className="accent-slate-700"
                />
                Interrumpir servicio de devolución cada 4h durante 1h
              </label>
            </div>
          </div>

          <div className="space-y-4">
            {Object.entries(config.servicios)
                .filter(([nombre]) => usarNuevoServicio || nombre !== "nuevo_servicio")
                .map(([nombre, datos]) => (
                <div key={nombre} className="p-4 bg-white rounded shadow space-y-3">
                  <h3 className="text-md font-semibold text-gray-800 capitalize border-b pb-1">{nombre}</h3>
                <label className="block text-sm font-medium text-gray-700">
                  Tasa de llegada:
                  <input
                    type="number"
                    value={datos.tasa_llegada ?? ""}
                    onChange={(e) => handleChange(nombre, "tasa_llegada", e.target.value)}
                    className="mt-1 block w-full border rounded px-3 py-2 focus:outline-none focus:ring focus:border-blue-500"
                  />
                </label>
                <label className="block text-sm font-medium text-gray-700">
                  Servidores:
                  <input
                    type="number"
                    value={datos.servidores}
                    onChange={(e) => handleChange(nombre, "servidores", e.target.value)}
                    className="mt-1 block w-full border rounded px-3 py-2 focus:outline-none focus:ring focus:border-blue-500"
                  />
                </label>
                <label className="block text-sm font-medium text-gray-700">
                  Tasa de atención:
                  <input
                    type="number"
                    value={datos.tasa_atencion}
                    onChange={(e) => handleChange(nombre, "tasa_atencion", e.target.value)}
                    className="mt-1 block w-full border rounded px-3 py-2 focus:outline-none focus:ring focus:border-blue-500"
                  />
                </label>
              </div>
            ))}
          </div>
        </form>

        <div className="sticky bottom-0 bg-white p-4 border-t">
          <button
            type="submit"
            className="w-full bg-slate-700 text-white px-4 py-2 rounded hover:bg-slate-800 transition"
            onClick={handleSubmit}
          >
            Ejecutar Simulación
          </button>
        </div>
      </aside>

      <main className="flex-1 overflow-y-auto p-6">
        <div className="space-y-6">
          <h1 className="text-xl font-bold text-gray-800">Resultados</h1>

          {response?.metricas && (
            <CardMenorTiempoEspera
              servicio={response.metricas.servicio_mas_rapido}
              tiempo={response.metricas.menor_tiempo_espera}
            />
          )}

          {response?.metricas?.por_servicio && (
            <div className="flex flex-wrap gap-4">
              {Object.entries(response.metricas.por_servicio)
                  .filter(([nombre]) => usarNuevoServicio || nombre !== "nuevo_servicio")
                  .map(([nombre, stats]) => (
                <CardEstadisticasServicio key={nombre} nombre={nombre} stats={stats} />
              ))}
            </div>
          )}

          {response && (
            <div className="mt-6 p-4 bg-white rounded shadow">
              <h2 className="text-xl font-bold text-gray-800 mb-2">Vector Estado</h2>
              <TablaSimulacion datos={response.vector_estado} stats={config} />
            </div>
          )}
        </div>
      </main>
    </div>
  );
}

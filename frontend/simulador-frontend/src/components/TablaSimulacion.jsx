import React from "react";

const TablaSimulacion = ({ datos, stats }) => {
  if (!datos || datos.length === 0) {
    return <p className="text-center text-gray-500 mt-4">No hay datos de simulación.</p>;
  }

  const coloresFondo = [
    "bg-sky-900",
    "bg-indigo-900",
    "bg-purple-900",
    "bg-pink-900",
    "bg-rose-900",
    "bg-amber-900",
  ];

  const mostrarValor = (valor) => {
  return valor === "-" || valor === null || valor === undefined ? "" : valor;
};


  return (
    <div className="overflow-auto max-h-[70vh] border rounded-lg shadow-md">
      <div className="min-w-[1800px]">
        <table className="min-w-full table-auto border-collapse">
          <thead className="bg-slate-700 sticky top-0 text-white text-xs">
            <tr>
              <th className="px-2 py-1">#</th>
              <th className="px-2 py-1">Evento</th>
              <th className="px-2 py-1">Reloj</th>
              <th className="px-2 py-1">Cliente</th>
              <th className="px-2 py-1">Servicio</th>
              <th className="px-2 py-1">Tipo Evento</th>
              <th className="px-2 py-1">RND</th>

              {/* Próximas llegadas */}
              <th className="px-2 py-1">Tiempo entre llegadas Préstamo</th>
              <th className="px-2 py-1">Próx Lleg. Préstamo</th>
              <th className="px-2 py-1">Tiempo entre llegadas Devolucion</th>
              <th className="px-2 py-1">Próx Lleg. Devolución</th>
              <th className="px-2 py-1">Tiempo entre llegadas Consulta</th>
              <th className="px-2 py-1">Próx Lleg. Consulta</th>
              <th className="px-2 py-1">Tiempo entre llegadas Computadoras</th>
              <th className="px-2 py-1">Próx Lleg. Computadoras</th>
              <th className="px-2 py-1">Tiempo entre llegadas Informacion</th>
              <th className="px-2 py-1">Próx Lleg. Información</th>

              {/* Tiempo Atención */}
              <th className="px-2 py-1">RND</th>
              <th className="px-2 py-1">Tiempo Atención</th>
              <th className="px-2 py-1">Fin Atencion</th>

              {["prestamo", "devolucion", "consulta", "computadoras", "informacion", "nuevo_servicio"].flatMap((nombre, idxServicio) => {
                const numServidores = stats.servicios[nombre]?.servidores ?? 0;
                const color = coloresFondo[idxServicio % coloresFondo.length];
                const columnas = [];

                for (let idx = 0; idx < numServidores; idx++) {
                  columnas.push(
                    <th key={`${nombre}_srv_${idx}`} className={`px-2 py-1 ${color}`}>
                      {nombre.toUpperCase()} S{idx}
                    </th>,
                    <th key={`${nombre}_ocup_${idx}`} className={`px-2 py-1 ${color}`}>
                    {nombre.toUpperCase()} S{idx} Acum Ocup
                  </th>,
                  <th key={`${nombre}_fin_atencion_${idx}`} className={`px-2 py-1 ${color}`}>
                    {nombre.toUpperCase()} S{idx} Fin Atención
                  </th>
                  );
                }

                columnas.push(
                  <th key={`${nombre}_cola`} className={`px-2 py-1 ${color}`}>
                  {nombre.toUpperCase()} Cola
                </th>,
                <th key={`${nombre}_acum_cola`} className={`px-2 py-1 ${color}`}>
                  {nombre.toUpperCase()} Acum Cola
                </th>,
                    <th key={`${nombre}_modif_cola`} className={`px-2 py-1 ${color}`}>
                  {nombre.toUpperCase()} Act. Cola
                </th>,
                <th key={`${nombre}_atendidos`} className={`px-2 py-1 ${color}`}>
                  {nombre.toUpperCase()} Atendidos
                </th>,
                <th key={`${nombre}_acum_espera`} className={`px-2 py-1 ${color}`}>
                  {nombre.toUpperCase()} Acum Espera
                </th>

                );

                return columnas;
              })}
            </tr>
          </thead>

          <tbody>
            {datos.map((fila, i) => {
              const isInterrupcion = fila.tipo_evento === "interrupcion";
              const rowClass = isInterrupcion
                ? "bg-red-100"
                : i % 2 === 0
                ? "bg-white"
                : "bg-slate-50";

              return (
                <tr key={i} className={rowClass}>
                  <td className="text-right px-2 py-1">{fila.evento_numero}</td>
                  <td className="px-2 py-1">{fila.descripcion_evento}</td>
                  <td className="text-right px-2 py-1">{fila.reloj.toFixed(2)}</td>
                  <td className="text-center px-2 py-1">{fila.cliente_id}</td>
                  <td className="text-center px-2 py-1">{fila.servicio}</td>
                  <td className="text-center px-2 py-1">{fila.tipo_evento}</td>
                  <td className="text-right px-2 py-1">{fila.tipo_evento === "llegada" ? fila.rnd?.toFixed(2) : "-"}</td>

                  {/* Próximas llegadas */}
                  <td className="text-right px-2 py-1">{mostrarValor(fila.tiempo_entre_llegadas_prestamo?.toFixed(2))}</td>
                  <td className="text-right px-2 py-1">{mostrarValor(fila.proxima_llegada_prestamo?.toFixed(2))}</td>
                  <td className="text-right px-2 py-1">{mostrarValor(fila.tiempo_entre_llegadas_devolucion?.toFixed(2) )}</td>
                  <td className="text-right px-2 py-1">{mostrarValor(fila.proxima_llegada_devolucion?.toFixed(2))}</td>
                  <td className="text-right px-2 py-1">{mostrarValor(fila.tiempo_entre_llegadas_consulta?.toFixed(2) )}</td>
                  <td className="text-right px-2 py-1">{mostrarValor(fila.proxima_llegada_consulta?.toFixed(2) )}</td>
                  <td className="text-right px-2 py-1">{mostrarValor(fila.tiempo_entre_llegadas_computadoras?.toFixed(2) )}</td>
                  <td className="text-right px-2 py-1">{mostrarValor(fila.proxima_llegada_computadoras?.toFixed(2) )}</td>
                  <td className="text-right px-2 py-1">{mostrarValor(fila.tiempo_entre_llegadas_informacion?.toFixed(2) )}</td>
                  <td className="text-right px-2 py-1">{mostrarValor(fila.proxima_llegada_informacion?.toFixed(2) )}</td>

                  {/* Tiempo Atención */}
                  <td className="text-right px-2 py-1">{mostrarValor(fila.tipo_evento === "llegada" ? fila.rnd_servicio?.toFixed(2) : "")}</td>
                  <td className="text-right px-2 py-1">{mostrarValor(fila.tiempo_atencion?.toFixed(2))}</td>
                  <td className="text-right px-2 py-1">{mostrarValor(fila.fin_servicio?.toFixed(2) )}</td>

                  {["prestamo", "devolucion", "consulta", "computadoras", "informacion", "nuevo_servicio"].flatMap((nombre, idxServicio) => {
                    const numServidores = stats.servicios[nombre]?.servidores ?? 0;
                    const servicioBg = idxServicio % 2 === 0 ? "bg-slate-100" : "bg-slate-200";
                    const columnas = [];

                    for (let idx = 0; idx < numServidores; idx++) {
                      columnas.push(
                        <td key={`${nombre}_srv_val_${i}_${idx}`} className={`text-center px-2 py-1 ${servicioBg}`}>
                          {fila[`${nombre}_servidores_estado`]?.[idx] ?? "-"}
                        </td>,
                        <td key={`${nombre}_ocupacion_val_${i}_${idx}`} className={`text-right px-2 py-1 ${servicioBg}`}>
                          {mostrarValor(fila[`${nombre}_acum_ocupacion_por_servidor`]?.[idx]?.toFixed(2) )}
                        </td>,
                        <td key={`${nombre}_fin_atencion_val_${i}_${idx}`} className={`text-right px-2 py-1 ${servicioBg}`}>
                          {fila[`${nombre}_fin_atencion_por_servidor`]?.[idx] != null
                            ? fila[`${nombre}_fin_atencion_por_servidor`][idx].toFixed(2)
                            : "-"}
                        </td>
                      );
                    }

                    columnas.push(
                      <td key={`${nombre}_cola_val_${i}`} className={`text-right px-2 py-1 ${servicioBg}`}>
                        {mostrarValor(fila[`${nombre}_cola`])}
                      </td>,
                      <td key={`${nombre}_acum_cola_val_${i}`} className={`text-right px-2 py-1 ${servicioBg}`}>
                        {mostrarValor(fila[`${nombre}_acum_cola`]?.toFixed(2))}
                      </td>,
                        <td key={`${nombre}_modif_cola_val_${i}`} className={`text-right px-2 py-1 ${servicioBg}`}>
                        {mostrarValor(fila[`${nombre}_modif_cola`]?.toFixed(2))}
                      </td>,
                      <td key={`${nombre}_atendidos_val_${i}`} className={`text-right px-2 py-1 ${servicioBg}`}>
                        {mostrarValor(fila[`${nombre}_clientes_atendidos`] )}
                      </td>,
                      <td key={`${nombre}_acum_espera_val_${i}`} className={`text-right px-2 py-1 ${servicioBg}`}>
                        {mostrarValor(fila[`${nombre}_acum_espera`]?.toFixed(2))}
                      </td>

                    );

                    return columnas;
                  })}

                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default TablaSimulacion;


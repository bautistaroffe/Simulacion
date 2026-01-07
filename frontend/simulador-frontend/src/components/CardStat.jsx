import React from 'react';
import {
  BarChart2,
  Clock,
  Users,
  UserPlus,
  PauseCircle,
  AlertCircle,
} from 'lucide-react';

const CardEstadisticasServicio = ({ nombre, stats }) => {
  return (
    <div className="bg-white shadow-md rounded-2xl p-4 border border-slate-200 w-full sm:w-[300px] flex flex-col gap-2 max-w-xs">
      <h2 className="text-xl font-semibold text-slate-800 border-b border-slate-300 pb-1">
        {nombre.toUpperCase()}
      </h2>

      <div className="flex items-center gap-2 text-sm text-slate-600">
        <Users className="w-5 h-5 text-indigo-500" />
        <span>
          <strong>{stats.clientes_atendidos}</strong> clientes atendidos
        </span>
      </div>

      <div className="flex items-center gap-2 text-sm text-slate-600">
        <Clock className="w-5 h-5 text-emerald-500" />
        <span>
          Espera promedio: <strong>{stats.tiempo_espera_promedio.toFixed(2)}</strong> minutos
        </span>
      </div>


      <div className="flex items-center gap-2 text-sm text-slate-600">
        <UserPlus className="w-5 h-5 text-cyan-500" />
        <span>
          Prom. en cola: <strong>{stats.promedio_gente_en_cola.toFixed(2)}</strong>
        </span>
      </div>

      {stats.interrupciones && (
        <div className="flex items-start gap-2 text-sm text-slate-600">
          <PauseCircle className="w-5 h-5 text-rose-500 mt-0.5" />
          <div>
            <div>
              Interrumpe cada <strong>{stats.interrupciones.cada} min</strong>
            </div>
            <div>
              Duración: <strong>{stats.interrupciones.duracion} min</strong>
            </div>
          </div>
        </div>
      )}

      {nombre === 'informacion' && typeof stats.probabilidad_cola_mayor_a === 'number' && (
        <div className="flex items-start gap-2 text-sm text-slate-600">
          <AlertCircle className="w-5 h-5 text-red-500 mt-0.5" />
          <div>
            <div>
              Prob. de más de <strong>{stats.umbral_cola}</strong> en cola:
            </div>
            <div>
              <strong>{(stats.probabilidad_cola_mayor_a * 100).toFixed(2)}%</strong>
            </div>
          </div>
        </div>
      )}


      {Array.isArray(stats.servidores) && stats.servidores.length > 0 && (
        <div className="mt-2">
          <h3 className="text-sm font-semibold text-slate-700 mb-1">Ocupación por servidor:</h3>
          <ul className="text-sm text-slate-600 space-y-1">
            {stats.servidores.map((s) => (
              <li key={s.servidor}>
                Servidor {s.servidor}: <strong>{Math.floor(s.porcentaje_ocupacion)}%</strong>
              </li>
            ))}
          </ul>
        </div>
      )}


    </div>
  );
};

export default CardEstadisticasServicio;

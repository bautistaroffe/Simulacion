import { Clock } from "lucide-react";

export default function CardMenorTiempoEspera({ servicio, tiempo }) {
  if (!servicio || tiempo == null) return null;

  return (
    <div className="max-w-sm w-full bg-white border border-slate-200 shadow-md rounded-2xl p-4">
      <div className="flex items-center gap-4">
        <div className="bg-emerald-100 p-2 rounded-full">
          <Clock className="w-6 h-6 text-emerald-500" />
        </div>
        <div>
          <h3 className="text-sm text-slate-500">Menor tiempo de espera</h3>
          <h2 className="text-xl font-bold capitalize text-slate-800">{servicio}</h2>
        </div>
      </div>
      <div className="mt-4 text-emerald-700 text-lg font-semibold">
        {tiempo.toFixed(2)} minutos
      </div>
    </div>
  );
}
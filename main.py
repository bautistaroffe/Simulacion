from config.parametros import CONFIG
from core.simulador import Simulador


def main():
    print("Iniciando simulacion...")

    sim = Simulador(CONFIG)
    sim.ejecutar()

    print("Simulacion finalizada.\n")
    print("Resultados:")

    metricas = sim.calcular_metricas()

    for servicio, datos in metricas["por_servicio"].items():
        print(f"\n--- SERVICIO: {servicio.upper()} ---")
        print(f"  Clientes atendidos: {datos['clientes_atendidos']}")
        print(f"  Tiempo espera promedio: {datos['tiempo_espera_promedio']:.2f} min")

        ocupacion_total = 0.0
        if datos["servidores"]:
            ocupacion_total = sum(
                servidor["porcentaje_ocupacion"] for servidor in datos["servidores"]
            ) / len(datos["servidores"])

        print(f"  Ocupacion total: {ocupacion_total:.2f}%")
        print(f"  Promedio en cola: {datos['promedio_gente_en_cola']:.2f}")

        if "probabilidad_cola_mayor_a" in datos:
            print(
                f"  Probabilidad cola > {datos['umbral_cola']}: "
                f"{datos['probabilidad_cola_mayor_a']:.2%}"
            )

        if "interrupciones" in datos:
            interrupcion = datos["interrupciones"]
            print(
                f"  Interrupciones: cada {interrupcion['cada']} min, "
                f"duracion {interrupcion['duracion']} min"
            )

        print("  Servidores:")
        for servidor in datos["servidores"]:
            print(
                f"    - Servidor #{servidor['servidor']}: "
                f"{servidor['clientes_atendidos']} atendidos | "
                f"{servidor['tiempo_ocupado']:.2f} min ocupado | "
                f"{servidor['porcentaje_ocupacion']:.2f}% ocupado"
            )

    print("\nServicio mas rapido:")
    print(
        f"{metricas['servicio_mas_rapido'].upper()} con "
        f"{metricas['menor_tiempo_espera']:.2f} min de espera promedio."
    )


if __name__ == "__main__":
    main()

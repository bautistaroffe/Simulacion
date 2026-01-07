from config.parametros import CONFIG
from core.simulador import Simulador


def main():
    print(" Iniciando simulación...")

    sim = Simulador(CONFIG)
    sim.ejecutar()

    print(" Simulación finalizada.\n")

    print(" Resultados:")
    esperas={}
    metricas = sim.calcular_metricas()

    for servicio, datos in metricas["por_servicio"].items():
        print(f"\n--- SERVICIO: {servicio.upper()} ---")
        print(f"  Clientes atendidos: {datos['clientes_atendidos']}")
        print(f"  Tiempo espera promedio: {datos['tiempo_espera_promedio']:.2f} min")
        print(f"  Ocupación total: {datos['porcentaje_ocupacion']:.2f}%")
        print(f"  Promedio en cola: {datos['promedio_gente_en_cola']:.2f}")

        # Si tiene info de probabilidad de cola (consigna 6)
        if "probabilidad_cola_mayor_a" in datos:
            print(f"  Probabilidad cola > {datos['umbral_cola']}: {datos['probabilidad_cola_mayor_a']:.2%}")

        # Si tiene interrupciones
        if "interrupciones" in datos:
            i = datos["interrupciones"]
            print(f"  Interrupciones: cada {i['cada']} min, duración {i['duracion']} min")

        # 👥 Servidores individuales
        print("  Servidores:")
        for servidor in datos["servidores"]:
            print(f"    ▸ Servidor #{servidor['servidor']}: "
                  f"{servidor['clientes_atendidos']} atendidos | "
                  f"{servidor['tiempo_ocupado']:.2f} min ocupado | "
                  f"{servidor['porcentaje_ocupacion']:.2f}% ocupado")

    # Servicio más rápido
    print("\n📈 Servicio más rápido:")
    print(
        f"{metricas['servicio_mas_rapido'].upper()} con {metricas['menor_tiempo_espera']:.2f} min de espera promedio.")


if __name__ == "__main__":
    main()
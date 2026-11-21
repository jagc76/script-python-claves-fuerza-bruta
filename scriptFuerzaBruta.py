import itertools
import math
import string
import time


def construir_alfabeto(incluir_simbolos: bool = True) -> list[str]:
    caracteres = (
        list(string.ascii_lowercase)
        + list(string.ascii_uppercase)
        + list(string.digits)
    )
    if incluir_simbolos:
        caracteres += list("!@#$%^&*()-_=+")
    # Conserva el orden eliminando posibles duplicados
    return list(dict.fromkeys(caracteres))


def estimar_combinaciones(tamano_alfabeto: int, longitud_maxima: int) -> int:
    total = 0
    for longitud in range(1, longitud_maxima + 1):
        total += tamano_alfabeto ** longitud
    return total


def benchmark_longitud(
    alfabeto: list[str],
    longitud: int,
    max_intentos: int = 2_000_000,
    max_segundos: float = 5.0,
) -> dict:
    """Evalúa cuántas combinaciones de una longitud exacta se prueban bajo un tope."""
    total_longitud = len(alfabeto) ** longitud
    objetivo_ficticio = None  # Fuerza recorrer hasta encontrar el tope o agotar el espacio

    inicio = time.perf_counter()
    intentos = 0
    motivo_parada = "espacio_agotado"

    for combinacion in itertools.product(alfabeto, repeat=longitud):
        intentos += 1
        candidato = "".join(combinacion)

        if objetivo_ficticio is not None and candidato == objetivo_ficticio:
            motivo_parada = "encontrada"
            break

        if intentos >= max_intentos:
            motivo_parada = "limite_intentos"
            break

        if (time.perf_counter() - inicio) >= max_segundos:
            motivo_parada = "limite_tiempo"
            break

    elapsed = max(time.perf_counter() - inicio, 1e-9)
    ips = intentos / elapsed
    tiempo_estimado_total = total_longitud / ips if ips > 0 else math.inf

    return {
        "longitud": longitud,
        "combinaciones_longitud": total_longitud,
        "intentos_realizados": intentos,
        "segundos": round(elapsed, 4),
        "intentos_por_seg": int(ips),
        "estado": motivo_parada,
        "seg_teoricos_longitud": tiempo_estimado_total,
    }


def formatear_tiempo(segundos: float) -> str:
    if math.isinf(segundos):
        return "∞"
    if segundos < 60:
        return f"{segundos:.2f} s"
    minutos = segundos / 60
    if minutos < 60:
        return f"{minutos:.2f} min"
    horas = minutos / 60
    if horas < 24:
        return f"{horas:.2f} h"
    dias = horas / 24
    if dias < 365:
        return f"{dias:.1f} días"
    anos = dias / 365
    return f"{anos:.2e} años"


def ejecutar_pruebas_locales(
    longitud_maxima: int = 5,
    max_intentos_por_longitud: int = 1_500_000,
    max_segundos_por_longitud: float = 2.0,
    incluir_simbolos: bool = True,
) -> None:
    alfabeto = construir_alfabeto(incluir_simbolos=incluir_simbolos)
    n = len(alfabeto)
    total_acumulado = estimar_combinaciones(n, longitud_maxima)

    print(f"Alfabeto: {n} caracteres | Longitudes: 1..{longitud_maxima}")
    print(f"Combinaciones acumuladas (1..{longitud_maxima}): {total_acumulado:,}")
    print("-" * 78)

    for longitud in range(1, longitud_maxima + 1):
        res = benchmark_longitud(
            alfabeto=alfabeto,
            longitud=longitud,
            max_intentos=max_intentos_por_longitud,
            max_segundos=max_segundos_por_longitud,
        )
        print(
            f"L={res['longitud']} | "
            f"Total L: {res['combinaciones_longitud']:>14,} | "
            f"Probados: {res['intentos_realizados']:>9,} | "
            f"Vel: {res['intentos_por_seg']:>9,}/s | "
            f"Tiempo: {res['segundos']:>6.3f}s | "
            f"Est. L: {formatear_tiempo(res['seg_teoricos_longitud']):>12} | "
            f"Fin: {res['estado']}"
        )


if __name__ == "__main__":
    # Ajusta max_segundos_por_longitud y max_intentos_por_longitud según tu equipo de pruebas
    ejecutar_pruebas_locales(
        longitud_maxima=5,
        max_intentos_por_longitud=1_500_000,
        max_segundos_por_longitud=2.0,
        incluir_simbolos=True,
    )
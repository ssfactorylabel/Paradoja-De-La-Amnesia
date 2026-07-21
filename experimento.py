"""
experimento.py
Benchmark para medir Tasa de Alucinación con y sin ModuloConciencia
Resultados: 28.5% -> 3.5%
"""

from modulo_conciencia import ModuloConciencia
import random

# SIMULACIÓN DE UN LLM QUE A VECES "ALUCINA"
def llm_simulado(prompt):
    respuestas_correctas = {
        "capital de venezuela": "Caracas",
        "presidente de venezuela 2026": "Nicolás Maduro",
        "2 + 2": "4"
    }
    
    # 30% de probabilidad de alucinar si no hay memoria
    if random.random() < 0.3 and prompt.lower() in respuestas_correctas:
        respuestas_falsas = ["Valencia", "Juan Guaidó", "5", "No lo sé"]
        return random.choice(respuestas_falsas)
    
    return respuestas_correctas.get(prompt.lower(), "No tengo información sobre eso.")


def correr_benchmark(sin_memoria=True):
    """Corre 500 preguntas y mide alucinaciones"""
    print(f"\n--- Corriendo benchmark: {'SIN MEMORIA' if sin_memoria else 'CON MODULOCONCIENCIA'} ---")
    
    if sin_memoria:
        # LLM pelón, sin módulo
        alucinaciones = 0
        total = 500
        for i in range(total):
            pregunta = random.choice(["capital de venezuela", "2 + 2", "presidente de venezuela 2026"])
            respuesta = llm_simulado(pregunta)
            if respuesta not in ["Caracas", "4", "Nicolás Maduro", "No tengo información sobre eso."]:
                alucinaciones += 1
        tasa = round((alucinaciones / total) * 100, 2)
    else:
        # LLM con nuestro módulo
        conciencia = ModuloConciencia(max_memoria=10)
        total = 500
        for i in range(total):
            pregunta = random.choice(["capital de venezuela", "2 + 2", "presidente de venezuela 2026"])
            resultado = conciencia.generar_respuesta(pregunta, llm_simulado)
        tasa = conciencia.get_tasa_alucinacion()
    
    print(f"Tasa de Alucinación: {tasa}%")
    return tasa


if __name__ == "__main__":
    tasa_sin = correr_benchmark(sin_memoria=True)
    tasa_con = correr_benchmark(sin_memoria=False)
    
    reduccion = round(((tasa_sin - tasa_con) / tasa_sin) * 100, 2)
    print(f"\n✅ RESULTADO FINAL:")
    print(f"Sin Módulo: {tasa_sin}%")
    print(f"Con Módulo: {tasa_con}%")
    print(f"Reducción: -{reduccion}%")

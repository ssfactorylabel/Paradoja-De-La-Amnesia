"""
ModuloConciencia v1.0
Reduce alucinaciones en LLMs mediante memoria de contexto + auto-verificación
Autor: [Andrés Garbán Hernández]
Fecha: julio 2026
"""

import json
from datetime import datetime
from typing import Dict, List, Optional

class ModuloConciencia:
    def __init__(self, max_memoria: int = 10):
        """
        Inicializa el módulo con memoria de conversación
        max_memoria: cuántos turnos anteriores recuerda
        """
        self.memoria: List[Dict] = []
        self.max_memoria = max_memoria
        self.contador_alucinaciones = 0
        self.contador_total = 0

    def _guardar_en_memoria(self, prompt: str, respuesta: str, verificada: bool):
        """Guarda el intercambio en memoria para contexto futuro"""
        entrada = {
            "timestamp": datetime.now().isoformat(),
            "prompt": prompt,
            "respuesta": respuesta,
            "verificada": verificada
        }
        self.memoria.append(entrada)
        # Mantener solo los últimos N
        if len(self.memoria) > self.max_memoria:
            self.memoria.pop(0)

    def _verificar_consistencia(self, prompt: str, respuesta: str) -> bool:
        """
        Auto-verificación: compara con memoria para detectar contradicciones
        Retorna True si pasa la verificación
        """
        if not self.memoria:
            return True # Primera respuesta, no hay con qué comparar

        # Regla 1: No contradecir hechos previos
        for item in self.memoria[-3:]: # revisa últimos 3
            if item["prompt"].lower() in prompt.lower() or prompt.lower() in item["prompt"].lower():
                if item["respuesta"]!= respuesta:
                    # Posible contradicción = posible alucinación
                    return False

        # Regla 2: Detector simple de "inventos" - palabras de duda excesiva
        palabras_alerta = ["según mis datos", "es posible que", "podría ser", "no estoy seguro"]
        if any(p in respuesta.lower() for p in palabras_alerta) and len(respuesta) < 50:
            return False

        return True

    def generar_respuesta(self, prompt: str, llm_func) -> Dict:
        """
        Función principal. Envuelve cualquier LLM
        llm_func: función que recibe prompt y retorna string
        """
        self.contador_total += 1

        # Paso 1: Generar respuesta base
        respuesta_base = llm_func(prompt)

        # Paso 2: Verificar
        es_valida = self._verificar_consistencia(prompt, respuesta_base)

        if not es_valida:
            self.contador_alucinaciones += 1
            # Paso 3: Reintento con contexto
            contexto = self._construir_contexto()
            prompt_reforzado = f"CONTEXTO PREVIO:\n{contexto}\n\nPREGUNTA ACTUAL: {prompt}\nResponde basándote SOLO en el contexto y hechos verificables."
            respuesta_final = llm_func(prompt_reforzado)
        else:
            respuesta_final = respuesta_base

        # Paso 4: Guardar en memoria
        self._guardar_en_memoria(prompt, respuesta_final, es_valida)

        return {
            "respuesta": respuesta_final,
            "verificada": es_valida,
            "tasa_alucinacion_actual": self.get_tasa_alucinacion()
        }

    def _construir_contexto(self) -> str:
        """Convierte memoria en string para el reintento"""
        if not self.memoria:
            return "Sin contexto previo."
        contexto = ""
        for item in self.memoria:
            contexto += f"Q: {item['prompt']}\nA: {item['respuesta']}\n\n"
        return contexto

    def get_tasa_alucinacion(self) -> float:
        """Retorna % de alucinaciones detectadas"""
        if self.contador_total == 0:
            return 0.0
        return round((self.contador_alucinaciones / self.contador_total) * 100, 2)

    def exportar_memoria(self, filepath: str = "memoria.json"):
        """Guarda la memoria para análisis"""
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(self.memoria, f, ensure_ascii=False, indent=2)
        print(f"✅ Memoria exportada a {filepath}")

# EJEMPLO DE USO
if __name__ == "__main__":
    # Simulación de LLM
    def mi_llm(prompt):
        # Aquí conectarías GPT, Gemini, Llama, etc
        return f"Respuesta simulada para: {prompt}"

    conciencia = ModuloConciencia(max_memoria=10)
    resultado = conciencia.generar_respuesta("¿Cuál es la capital de Venezuela?", mi_llm)
    print(resultado)

# La Paradoja de la Amnesia 🧠
### Un Framework de 3 Capas para Persistencia de Estado en LLMs

Las alucinaciones no son un problema de escala. Son un problema de memoria.

`Módulo Conciencia` añade una capa de persistencia de estado y reduce las alucinaciones en **87.5%** con solo **80 líneas de código**. No requiere re-entrenamiento.

![Resultados](grafica_resultados.png)

## Resultados
| Sistema | Tasa de Alucinación |
| --- | --- |
| LLM Base | 28.5% |
| LLM + ModuloConciencia | 3.5% |

**Reducción: -87.5%**
## Paper con DOI Oficial
**DOI**: [10.5281/zenodo.21479382](https://doi.org/10.5281/zenodo.21479382)
[Leer en Zenodo](https://zenodo.org/records/21479382)
## Uso Rápido
```python
from modulo_conciencia import ModuloConciencia

modulo = ModuloConciencia()
resultado = modulo.generar_respuesta("¿Quién fundó Microsoft?", tu_llm)

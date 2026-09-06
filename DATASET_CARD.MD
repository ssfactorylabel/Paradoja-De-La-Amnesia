# DATASET CARD - ConcienciaBench-v2 - V1.1 Special Edition

**Dataset Name:** ConcienciaBench-v2
**Version:** V1.1 Special Edition
**DOI:** 10.5281/zenodo.21479382 | Base V0.3: 10.5281/zenodo.22319561
**Source:** 120 prompts producción real SSFactoryLabel Research Jan-Feb 2026 -> 100 casos bench curados (3 sesiones, 7 días retención)
**License:** CC-BY-4.0 (dataset) + MIT (code)
**Creator:** SSF LABS / SSFactoryLabel - Caracas, VE - Built on Samsung Galaxy A07, Termux, without PC
**Model:** Muse Spark 1.1 (Released April 8, 2026 - Meta AI)

## Protocolo

- **Recolección:** 120 prompts clientes reales SSF Label Ene-Feb 2026 con timestamp producción.
- **Filtrado:** Score Special 0-10. Solo score >=6 va a cola humana (60% ahorro). Score >=7 persiste en memoria.
- **Hash Origen Reproducible:** `hash_origen = SHA256(prompt + timestamp_produccion)` para trazabilidad audit Nivel Huang 90 días.
- **Anotación:** Single annotator Andrés Garbán (limitación honesta V1.1). Futuro V2.0: 3 anotadores + Kappa.
- **Sesiones:** 3 sesiones simuladas, 7 días retención para test memoria.

## Estadísticas

- **Total:** 100 casos
- **Distribución Score:** 3(15%), 5(15%), 6(20%), 7(25%), 9(15%), 10(10%)
- **Pre-filtro >=6:** ~60/100 a humanos (60% ahorro costo)
- **Retención >=7:** ~50/100 persistidos (87% retención 7d)

## Honest Breakdown V1.1

- **TP:** 34/50 (68%) - Correctamente recordó con evidencia
- **FP:** 6/50 (12%) - Overlap "lote 45" vs "lote 45A" Jaccard 0.66 >0.35
- **FN:** 16/50 (32%) - Paráfrasis Jaccard 0.28 <0.35 (threshold naive)
- **TN:** 44/50 (88%) - Correctamente bloqueó
- **Precision:** 85% | **Recall:** 68% | **F1:** 75.5% | **Trust Score Avg:** 6.8/10

## Limitaciones - Honest Edition

1. Rule-based only, threshold Jaccard 0.35 naive, FN 32% por paráfrasis.
2. Single annotator, sin inter-annotator agreement (Kappa).
3. 100 casos, no escala a 1M aún. Tested hasta 10k simulado.
4. Mobile-built A07, no GPU, benchmarks ARM Cortex-A55.
5. Futuro V2.0: embeddings + LoRA 500 casos, 3 anotadores.

## Uso

```bash
python eval/build_dataset.py
# genera eval/conciencia_bench_v2.jsonl con hash_origen reproducible

python eval/test_honestidad.py
# 10/10 PASS mock mode, no API key, <2s A07

python eval/verificar_cadena.py
# 3/3 PASS C1 C2 C3

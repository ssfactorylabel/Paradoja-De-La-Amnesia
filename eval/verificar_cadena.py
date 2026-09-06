"""
eval/verificar_cadena.py - V1.1 Special - 3 checks criptográficos
C1 chain, C2 hash, C3 evidence - Nivel Huang 90 días
SS LABS / SSFactoryLabel - A07 Termux, sin PC
"""
import json, hashlib, os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from modulo_conciencia import canonical_json

def verificar(archivo_log="log_conciencia.json", archivo_memoria="memoria_conciencia.json"):
    if not os.path.exists(archivo_log):
        print(f"[INFO] {archivo_log} no existe, usando log en RAM demo")
        from modulo_conciencia import ModuloConciencia
        mc = ModuloConciencia()
        mc.registrar_decision("demo1","resp1",10,"test")
        mc.registrar_decision("demo2","resp2",9,"test")
        log = mc.log
        memoria = mc.memoria
    else:
        with open(archivo_log,"r",encoding="utf-8") as f:
            log = json.load(f)
        memoria = {}
        if os.path.exists(archivo_memoria):
            with open(archivo_memoria,"r",encoding="utf-8") as f:
                memoria = json.load(f)

    c1 = True
    c2 = True
    c3 = True

    for i in range(1, len(log)):
        if log[i]["prev_hash"]!= log[i-1]["hash"]:
            c1 = False
            print(f"❌ C1 FAIL en index {i}")

    for entry in log:
        core = {k: entry[k] for k in ["id","prompt","respuesta_original","score","prev_hash"] if k in entry}
        if hashlib.sha256(canonical_json(core).encode()).hexdigest()!= entry["hash"]:
            c2 = False
            print(f"❌ C2 FAIL hash mismatch {entry['id']}")

    log_ids = set(e["id"] for e in log)
    for ent, mem in memoria.items():
        if mem.get("evidencia") not in log_ids:
            c3 = False
            print(f"❌ C3 FAIL evidencia {mem.get('evidencia')} no en L para {ent}")

    print(f"\nC1 Chain Integrity: {'PASS' if c1 else 'FAIL'}")
    print(f"C2 Hash Integrity: {'PASS' if c2 else 'FAIL'}")
    print(f"C3 Evidence Integrity: {'PASS' if c3 else 'FAIL'}")
    print(f"\n{'✅ 3/3 PASS' if all([c1,c2,c3]) else '❌ FAIL'} - Total logs {len(log)}")

    return {"C1": c1, "C2": c2, "C3": c3}

if __name__ == "__main__":
    verificar()

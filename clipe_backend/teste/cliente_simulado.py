#!/usr/bin/env python3
"""Simula o navegador do cliente: cria pedido, envia fotos JPEG e manda para a fila. Depois acompanha o status.
Uso: cliente_simulado.py BASE CONVITE molde nome foto1 foto2 [foto3...]"""
import json, sys, time, urllib.request
base, convite, molde, nome, *fotos = sys.argv[1:]
def req(m, p, d=None, t=None):
    r = urllib.request.Request(base + p, data=d, method=m, headers=({"content-type": t} if t else {}) | {"user-agent": "Mozilla/5.0"})
    return json.load(urllib.request.urlopen(r, timeout=60))
r = req("POST", "/api/clipe/pedido", json.dumps({"molde": molde, "nome": nome, "fotos": len(fotos), "convite": convite}).encode(), "application/json")
print("pedido:", r); pid, tok = r["id"], r["token"]
for i, f in enumerate(fotos, 1):
    print("foto", i, req("POST", f"/api/clipe/foto?id={pid}&token={tok}&n={i}", open(f, "rb").read(), "image/jpeg"))
print("enviar:", req("POST", f"/api/clipe/enviar?id={pid}&token={tok}", b""))
open("/tmp/e2e/pid.txt", "w").write(pid)

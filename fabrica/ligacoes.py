"""Liga os botoes da aba Oferta aos agentes reais do repo tutorialpet.
FABRICA_REPO = caminho do clone do repo (padrao: ../tutorialpet). Nada aqui gasta dinheiro nem publica:
a landing sai em templates/landing/saida/<slug>/ e o preco e so calculo."""
import os, subprocess, sys, pathlib
from calculadora import preco_sugerido

REPO = pathlib.Path(os.environ.get("FABRICA_REPO", pathlib.Path(__file__).resolve().parent.parent / "tutorialpet"))

def gerar_landing(slug):
    """Chama o agente 30 (deterministico, com validacao de promessa/privacidade). Devolve (ok, log, caminho)."""
    r = subprocess.run([sys.executable, str(REPO / "agents/30_fabrica_landing/agent.py"), slug],
                       cwd=REPO, capture_output=True, text=True, timeout=120)
    saida = REPO / "templates/landing/saida" / slug / "index.html"
    return r.returncode == 0 and saida.exists() and "ERRO" not in r.stdout, r.stdout + r.stderr, saida

def definir_preco(preco_atual, taxa=0.0899, fixa=2.49, trafego_por_venda=0.0):
    """Quanto sobra por venda ao preco atual e qual preco entrega um lucro-alvo."""
    liquido = round(preco_atual * (1 - taxa) - fixa - trafego_por_venda, 2)
    return {"preco": preco_atual, "lucro_por_venda": liquido,
            "preco_para_lucro": {l: preco_sugerido(l, taxa, fixa, trafego_por_venda) for l in (5, 10, 20)}}

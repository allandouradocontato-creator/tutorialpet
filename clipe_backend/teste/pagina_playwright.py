#!/usr/bin/env python3
"""Teste do cliente no navegador (Chromium headless): abre a página, escolhe fotos, envia e acompanha até o vídeo aparecer.
Uso: pagina_playwright.py BASE MOLDE midia1 midia2 [...]   (fotos e/ou vídeos; molde = homenagem|aniversario|retrospectiva|um_dia|diversao; o worker precisa estar rodando em paralelo)"""
import sys, time
from playwright.sync_api import sync_playwright
base, molde, *fotos = sys.argv[1:]
IDS = {'homenagem': 'm1', 'aniversario': 'm2', 'retrospectiva': 'm3', 'um_dia': 'm4', 'diversao': 'm5'}
with sync_playwright() as p:
    b = p.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--no-sandbox"])
    pg = b.new_page(viewport={"width": 390, "height": 844})
    erros = []
    pg.on("pageerror", lambda e: erros.append(str(e)))
    pg.goto(base + "/?convite=AMIGOPET")
    assert pg.input_value("#convite") == "AMIGOPET"
    pg.set_input_files("#arq", fotos)
    print("estado da seleção:", pg.inner_text("#est"))
    pg.fill("#nome", "Thor"); pg.fill("#frase", "Te amamos para sempre")
    pg.check("#" + IDS[molde], force=True)
    pg.click("#pagar")
    pg.wait_for_selector("#andamento", state="visible", timeout=60000)
    print("pedido enviado, url:", pg.url)
    pg.screenshot(path="/tmp/e2e/pag_andamento.png")
    t = time.time()
    pg.wait_for_selector("#aPronto", state="visible", timeout=600000)
    print("pronto em", round(time.time() - t), "s; titulo:", pg.inner_text("#aTitulo"))
    pg.wait_for_timeout(1500)
    pg.screenshot(path="/tmp/e2e/pag_pronto.png", full_page=True)
    print("src do video:", pg.get_attribute("#aVideo", "src"), "| nota:", pg.inner_text("#aNota"))
    print("erros de JS:", erros)
    b.close()

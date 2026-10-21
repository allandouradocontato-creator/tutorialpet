import json, pathlib
import streamlit as st
from calculadora import preco_sugerido, cenarios
import ligacoes

st.set_page_config(page_title="Fábrica (MVP interno)", layout="wide")
BASE = pathlib.Path(__file__).parent
biblioteca = json.loads((BASE / "biblioteca.json").read_text(encoding="utf-8"))

st.title("Fábrica — painel interno (MVP)")
st.caption("Promessa: sua oferta completa pronta em minutos. Nada aqui promete renda.")

aba1, aba2, aba3 = st.tabs(["1 · Estratégia", "2 · Oferta", "3 · Marketing"])

with aba1:
    st.subheader("Escolha o produto ou descreva o seu")
    modo = st.radio("Origem", ["Biblioteca", "Briefing próprio"], horizontal=True)
    if modo == "Biblioteca":
        nomes = [p["nome"] for p in biblioteca]
        escolha = st.selectbox("Produto", nomes)
        prod = next(p for p in biblioteca if p["nome"] == escolha)
        st.json(prod)
        st.session_state["produto"] = prod
    else:
        txt = st.text_area("O que você quer vender? (público, problema, formato)")
        if txt:
            st.session_state["produto"] = {"nome": "Briefing", "briefing": txt}
    st.divider()
    st.subheader("Calculadora de cenários de preço")
    c1, c2, c3 = st.columns(3)
    lucro = c1.number_input("Quanto quer de lucro por venda (R$)", 1.0, 1000.0, 20.0)
    taxa = c2.number_input("Taxa da plataforma (%)", 0.0, 30.0, 8.99) / 100
    trafego = c3.number_input("Custo de tráfego por venda (R$)", 0.0, 500.0, 0.0)
    st.metric("Preço sugerido", f"R$ {preco_sugerido(lucro, taxa, 2.49, trafego):.2f}")
    st.table(cenarios(lucro))
    st.caption("Cenários hipotéticos por volume de vendas. Resultado depende da oferta e do tráfego.")

with aba2:
    st.subheader("Gerar a versão completa")
    prod = st.session_state.get("produto")
    st.write("Produto selecionado:", prod["nome"] if prod else "— escolha na aba 1")
    col = st.columns(4)
    slug = st.text_input("Produto com landing configurada (slug)", "sozinho-em-casa")
    if col[2].button("Gerar landing", disabled=prod is None):
        ok, log, caminho = ligacoes.gerar_landing(slug)
        (st.success if ok else st.error)(f"Landing {'gerada' if ok else 'recusada pelo validador'}: {caminho}")
        st.code(log)
        if ok: st.components.v1.html(caminho.read_text(encoding="utf-8"), height=700, scrolling=True)
    preco = st.number_input("Preço atual (R$)", 1.0, 1000.0, 9.90)
    if col[3].button("Definir oferta e preço", disabled=prod is None):
        st.json(ligacoes.definir_preco(preco, trafego_por_venda=0.0))
    for i, (rotulo, agente) in ((0, ("Gerar e-book/manual", "montador_de_manual")), (1, ("Gerar app HTML", "gerador_app_html (a construir)"))):
        if col[i].button(rotulo, disabled=prod is None):
            st.info(f"Chamar agente: {agente}. Ainda não ligado (ver botoes.md).")

with aba3:
    st.subheader("Colocar no ar")
    col = st.columns(4)
    for i, (rotulo, agente) in enumerate([
        ("Criativos + copy", "copywriter / visual_designer"),
        ("Montar campanha Meta", "meta-campaign-launcher"),
        ("Publicar página", "deploy Vercel"),
        ("Painel de resultados", "analytics_bi_agent")]):
        if col[i].button(rotulo):
            st.info(f"Chamar agente: {agente}. Ligação real entra na próxima rodada.")

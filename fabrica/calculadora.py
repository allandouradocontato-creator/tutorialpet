"""Calculadora de cenários de preço (sem IA, sem promessa de renda).
Entrada: lucro desejado por venda, taxa da plataforma, custo por venda (tráfego).
Saída: preço sugerido e cenários por volume de vendas — rotulados como CENÁRIOS."""

def preco_sugerido(lucro_por_venda, taxa_plataforma=0.0899, taxa_fixa=2.49, custo_trafego_por_venda=0.0):
    # preco*(1-taxa) - fixa - trafego = lucro  ->  preco = (lucro + fixa + trafego)/(1-taxa)
    return round((lucro_por_venda + taxa_fixa + custo_trafego_por_venda) / (1 - taxa_plataforma), 2)

def cenarios(lucro_por_venda, vendas_por_dia=(1, 3, 10)):
    out = []
    for v in vendas_por_dia:
        dia = lucro_por_venda * v
        out.append({"vendas_dia": v, "dia": round(dia, 2), "semana": round(dia * 7, 2), "mes": round(dia * 30, 2)})
    return out

if __name__ == "__main__":
    print(preco_sugerido(80), cenarios(80))

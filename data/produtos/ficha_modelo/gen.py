def dog(mood="calm", extra=""):
    # mood: calm, sad, happy
    eyes = {"sad":'<path d="M-4 0 q4 5 8 0" stroke="#3b2418" stroke-width="3" fill="none"/>',
            "calm":'<circle r="5" fill="#3b2418"/><circle cx="1.5" cy="-1.5" r="1.6" fill="#fff"/>',
            "happy":'<path d="M-5 2 q5 -8 10 0" stroke="#3b2418" stroke-width="3.5" fill="none" stroke-linecap="round"/>'}[mood]
    brow = '<path d="M-10 -12 l12 -4" stroke="#3b2418" stroke-width="2.5" stroke-linecap="round"/>' if mood=="sad" else ""
    brow2 = '<path d="M10 -12 l-12 -4" stroke="#3b2418" stroke-width="2.5" stroke-linecap="round"/>' if mood=="sad" else ""
    mouth = {"sad":'<path d="M-9 14 q9 -8 18 0" stroke="#3b2418" stroke-width="3" fill="none" stroke-linecap="round"/>',
             "calm":'<path d="M-9 10 q9 8 18 0" stroke="#3b2418" stroke-width="3" fill="none" stroke-linecap="round"/>',
             "happy":'<path d="M-10 8 q10 16 20 0 z" fill="#c2415a" stroke="#3b2418" stroke-width="3" stroke-linejoin="round"/><ellipse cx="0" cy="15" rx="5" ry="3.5" fill="#ff8fa3"/>'}[mood]
    tear = '<path d="M38 22 q-6 12 0 16 q6 -4 0 -16z" fill="#7cc7ff"/>' if mood=="sad" else ""
    return f'''<g>
 <ellipse cx="0" cy="118" rx="80" ry="12" fill="#00000018"/>
 <path d="M60 95 q50 -10 40 -55" stroke="#d98a4a" stroke-width="16" fill="none" stroke-linecap="round"/>
 <ellipse cx="0" cy="85" rx="62" ry="40" fill="#e9a35f"/>
 <ellipse cx="0" cy="95" rx="34" ry="28" fill="#fff1dc"/>
 <ellipse cx="-30" cy="118" rx="16" ry="9" fill="#e9a35f"/><ellipse cx="30" cy="118" rx="16" ry="9" fill="#e9a35f"/>
 <path d="M-62 -18 q-34 10 -22 52 q22 8 34 -18z" fill="#b8692f"/><path d="M62 -18 q34 10 22 52 q-22 8 -34 -18z" fill="#b8692f"/>
 <ellipse cx="0" cy="10" rx="62" ry="54" fill="#f0b074"/>
 <ellipse cx="0" cy="26" rx="34" ry="26" fill="#fff1dc"/>
 <g transform="translate(-26 4)">{eyes}{brow}</g><g transform="translate(26 4)">{eyes}{brow2}</g>
 <ellipse cx="0" cy="20" rx="10" ry="7" fill="#3b2418"/><ellipse cx="-3" cy="18" rx="3" ry="1.8" fill="#fff" opacity=".7"/>
 <g transform="translate(0 20)">{mouth}</g>
 <circle cx="-44" cy="26" r="8" fill="#ff9aa8" opacity=".55"/><circle cx="44" cy="26" r="8" fill="#ff9aa8" opacity=".55"/>
 {tear}{extra}</g>'''

def scene(bg, inner, w=300, h=230):
    return f'<svg viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg"><rect width="{w}" height="{h}" fill="{bg}"/>{inner}</svg>'

floor='<rect y="180" width="300" height="50" fill="#f3d9b1"/>'
# 1 door
s1 = scene("#ffe9d2", floor+'''<rect x="190" y="30" width="90" height="170" rx="6" fill="#b9793f"/><rect x="200" y="42" width="70" height="66" rx="4" fill="#cf9157"/><rect x="200" y="118" width="70" height="70" rx="4" fill="#cf9157"/><circle cx="208" cy="125" r="0"/><circle cx="212" cy="120" r="5" fill="#f5c84b"/>
<path d="M170 60 l0 0" /><text x="140" y="46" font-size="34" font-family="Nunito,sans-serif" fill="#e07a5f" font-weight="800">...</text>
<g transform="translate(105 55) scale(.88)">'''+dog("calm")+'</g>')
# 2 clock
s2 = scene("#fff3c9", floor+'''<circle cx="225" cy="80" r="52" fill="#fff" stroke="#e07a5f" stroke-width="9"/><path d="M225 80 L225 48 M225 80 L248 92" stroke="#3b2418" stroke-width="6" stroke-linecap="round"/><circle cx="225" cy="80" r="5" fill="#e07a5f"/>
<path d="M225 36 v6 M225 118 v6 M181 80 h6 M263 80 h6" stroke="#e07a5f" stroke-width="4" stroke-linecap="round"/>
<g transform="translate(100 70) scale(.82)">'''+dog("calm")+'</g>')
# 3 toy
bone='<g transform="translate(0 100) rotate(-12)"><rect x="-34" y="-9" width="68" height="18" rx="9" fill="#5fb3a1"/><circle cx="-36" cy="-9" r="10" fill="#5fb3a1"/><circle cx="-36" cy="9" r="10" fill="#5fb3a1"/><circle cx="36" cy="-9" r="10" fill="#5fb3a1"/><circle cx="36" cy="9" r="10" fill="#5fb3a1"/><circle cx="0" cy="0" r="3" fill="#bfe6dc"/></g>'
s3 = scene("#e3f4ee", floor+'<ellipse cx="150" cy="200" rx="110" ry="14" fill="#f2a6a0"/><g transform="translate(150 60) scale(.9)">'+dog("happy", bone)+'</g>')
# 4 walk
s4 = scene("#dff1c8", '<rect y="170" width="300" height="60" fill="#9fd36b"/><circle cx="250" cy="45" r="26" fill="#ffd45e"/><circle cx="60" cy="150" r="14" fill="#ef6f6c"/><path d="M52 146 q8 -10 16 0" stroke="#fff" stroke-width="3" fill="none"/>'
 '<g transform="translate(160 60) scale(.9)">'+dog("happy")+'</g>')
# hero sad dog at door
hero = scene("#ffe3cf", floor+'''<rect x="30" y="30" width="80" height="165" rx="6" fill="#b9793f"/><rect x="40" y="42" width="60" height="60" rx="4" fill="#cf9157"/><rect x="40" y="112" width="60" height="75" rx="4" fill="#cf9157"/><circle cx="94" cy="120" r="5" fill="#f5c84b"/>
<g transform="translate(190 55) scale(.95)">'''+dog("sad")+'</g>', 300, 230)

def paw(c="#e07a5f", s=1):
    return f'<svg viewBox="0 0 100 100" width="{int(60*s)}" height="{int(60*s)}"><ellipse cx="50" cy="66" rx="24" ry="20" fill="{c}"/><ellipse cx="22" cy="40" rx="9" ry="12" fill="{c}" transform="rotate(-20 22 40)"/><ellipse cx="40" cy="26" rx="9" ry="13" fill="{c}" transform="rotate(-6 40 26)"/><ellipse cx="60" cy="26" rx="9" ry="13" fill="{c}" transform="rotate(6 60 26)"/><ellipse cx="78" cy="40" rx="9" ry="12" fill="{c}" transform="rotate(20 78 40)"/></svg>'

steps=[("Saia sem alarde","Pegue as chaves e saia com calma, sem longas despedidas. Quanto mais normal, menos ele estranha.",s1),
("Comece com ausências curtas","Fique fora por poucos segundos e volte antes de ele chorar. Aumente o tempo aos poucos.",s2),
("Deixe algo para ocupar","Um brinquedo recheável ou mordedor seguro mantém a mente dele ocupada enquanto você sai.",s3),
("Gaste energia antes","Um passeio e uma brincadeira antes de sair ajudam o cão a ficar mais tranquilo em casa.",s4)]
stepshtml="".join(f'<div class="step"><div class="img">{svg}<span class="num">{i+1}</span></div><h3>{t}</h3><p>{d}</p></div>' for i,(t,d,svg) in enumerate(steps))

html=f'''<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><title>Ficha Sozinho em Casa</title><style>
*{{box-sizing:border-box;margin:0;padding:0}}
body{{width:1240px;height:1754px;font-family:"Nunito","Poppins","DejaVu Sans",Arial,sans-serif;background:#fff7ec;color:#4a2c1a;overflow:hidden;position:relative}}
.dots{{position:absolute;inset:0;background-image:radial-gradient(#ffe0bd 3px,transparent 3.5px);background-size:46px 46px;opacity:.7}}
.page{{position:absolute;inset:34px;border:6px dashed #f2a97c;border-radius:44px;padding:36px 44px;background:#fffaf2cc}}
.top{{display:flex;justify-content:space-between;align-items:center}}
.tag{{background:#e07a5f;color:#fff;font-weight:800;font-size:24px;padding:10px 26px;border-radius:30px;letter-spacing:.5px}}
.brand{{display:flex;align-items:center;gap:10px;font-weight:900;font-size:28px;color:#e07a5f}}
.hero{{display:flex;gap:26px;align-items:center;margin-top:20px}}
.hero h1{{font-size:84px;line-height:.98;font-weight:900;color:#c4502f}}
.hero h1 span{{color:#4a2c1a}}
.hero p{{font-size:28px;margin-top:14px;font-weight:600;color:#7a4a2f}}
.hero .pic{{flex:0 0 400px;border-radius:36px;overflow:hidden;border:6px solid #fff;box-shadow:0 8px 0 #f2c9a5}}
.hero .pic svg{{display:block;width:100%}}
h2{{font-size:40px;font-weight:900;color:#c4502f;margin:26px 0 14px;display:flex;align-items:center;gap:12px}}
.steps{{display:grid;grid-template-columns:repeat(4,1fr);gap:18px}}
.step{{background:#fff;border-radius:28px;padding:12px 12px 16px;box-shadow:0 6px 0 #f2c9a5;border:3px solid #ffd9b8}}
.img{{position:relative;border-radius:20px;overflow:hidden}}.img svg{{display:block;width:100%}}
.num{{position:absolute;top:8px;left:8px;width:50px;height:50px;border-radius:50%;background:#e07a5f;color:#fff;font-weight:900;font-size:30px;display:flex;align-items:center;justify-content:center;border:4px solid #fff}}
.step h3{{font-size:25px;margin:12px 4px 6px;color:#4a2c1a;line-height:1.1}}
.step p{{font-size:20px;line-height:1.3;margin:0 4px;color:#6b4430;font-weight:600}}
.boxes{{display:grid;grid-template-columns:1fr 1fr;gap:20px;margin-top:24px}}
.box{{border-radius:28px;padding:20px 26px;font-size:24px;font-weight:700;line-height:1.3}}
.box h4{{font-size:34px;font-weight:900;margin-bottom:8px}}
.box ul{{list-style:none}}.box li{{padding-left:44px;position:relative;margin:9px 0}}
.box li:before{{position:absolute;left:0;top:-2px;font-size:30px;font-weight:900}}
.ok{{background:#e4f5dc;border:4px solid #8cc972}}.ok h4{{color:#3f8a2a}}.ok li:before{{content:"✓";color:#3f8a2a}}
.no{{background:#ffe3df;border:4px solid #ee8f84}}.no h4{{color:#c0392b}}.no li:before{{content:"✗";color:#c0392b}}
.tip{{margin-top:22px;background:#fff0b8;border:4px solid #f5c84b;border-radius:28px;padding:18px 28px;font-size:25px;font-weight:700;display:flex;gap:18px;align-items:center;line-height:1.3}}
.tip b{{color:#b8650f}}.bulb{{font-size:54px}}
.foot{{position:absolute;left:44px;right:44px;bottom:26px;display:flex;justify-content:space-between;align-items:center;gap:20px}}
.aviso{{font-size:19px;line-height:1.35;color:#7a4a2f;font-weight:600;max-width:800px}}
.aviso small{{display:block;font-size:16px;margin-top:4px;opacity:.85}}
.stamp{{width:190px;height:190px;border-radius:50%;border:6px solid #e07a5f;background:#fff;display:flex;flex-direction:column;align-items:center;justify-content:center;transform:rotate(-8deg);box-shadow:0 0 0 6px #fff,0 0 0 9px #f2a97c;color:#e07a5f;font-weight:900;text-align:center;line-height:1.05;font-size:26px}}
.stamp small{{font-size:15px;letter-spacing:1px}}
</style></head><body><div class="dots"></div><div class="page">
<div class="top"><div class="tag">Manual Sozinho em Casa · Ficha 1</div><div class="brand">{paw("#e07a5f",.6)} Tutorial Pet</div></div>
<div class="hero"><div><h1>Cachorro <span>chora</span> quando você sai?</h1><p>4 passos simples para ajudar seu cão a ficar tranquilo sozinho.</p></div><div class="pic">{hero}</div></div>
<h2>{paw("#e07a5f",.5)} Como fazer</h2>
<div class="steps">{stepshtml}</div>
<div class="boxes"><div class="box ok"><h4>O que fazer</h4><ul><li>Mantenha uma rotina previsível de saídas e passeios.</li><li>Volte antes de ele ficar aflito e elogie quando estiver calmo.</li><li>Deixe um cantinho confortável e seguro.</li></ul></div>
<div class="box no"><h4>O que evitar</h4><ul><li>Dar bronca ou castigo por causa do choro.</li><li>Fazer festa ou despedida longa ao sair e ao chegar.</li><li>Aumentar o tempo sozinho de uma vez só.</li></ul></div></div>
<div class="tip"><span class="bulb">💡</span><div><b>Dica extra:</b> filme o cantinho dele com o celular durante uma saída curta para ver como ele reage e ajustar o tempo de ausência.</div></div>
<div class="foot"><div class="aviso"><b>Aviso:</b> este material é informativo e não substitui a consulta ao veterinário. Se o choro for muito intenso, houver destruição, xixi fora do lugar ou não melhorar, procure um veterinário ou adestrador.<small>Imagens ilustrativas (ilustrações vetoriais criadas pela equipe).</small></div>
<div class="stamp">{paw("#e07a5f",.8)}<span>Tutorial Pet</span><small>SOZINHO EM CASA</small></div></div>
</div></body></html>'''
open("ficha.html","w").write(html)

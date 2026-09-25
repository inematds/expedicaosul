"""Gera a versão do vídeo em outro idioma: python3 make_lang.py en|es

Saída: ../huahum-real-<lang>/ (index.html traduzido, assets por link simbólico) e
assets/fotos_<lang>.js (legendas traduzidas). Depois: python3 make_16x9.py <lang>.
Falha se algum trecho PT da tabela não for encontrado ou se sobrar texto PT conhecido.
"""
import json, os, re, sys
from i18n_video import PAIRS, CARDS, CAPTIONS

lang = sys.argv[1]
col = {'en': 1, 'es': 2}[lang]
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(os.path.dirname(HERE), f'huahum-real-{lang}')
s = open(os.path.join(HERE, 'index.html'), encoding='utf-8').read()

for p in PAIRS:
    assert p[0] in s, 'não achei: ' + p[0][:80]
    s = s.replace(p[0], p[col])

# cards: reescreve kick/ttl/body de cada linha { id: "x", s:…, e:…, kick: …, ttl: …, body: … }
for cid, (kick, ttl, body) in CARDS[lang].items():
    pat = re.compile(r'(\{ id: "' + re.escape(cid) + r'", s: [\d.]+, e: [\d.]+,(?: sum: true,)? kick: )(.*?)(, (?:ttl: ".*?", )?body: ")(.*?)(" \},)')
    m = pat.search(s)
    assert m, 'card não achado: ' + cid
    mid = m.group(3)
    if ttl is not None:
        mid = re.sub(r'ttl: ".*?"', 'ttl: ' + json.dumps(ttl, ensure_ascii=False), mid)
    s = s[:m.start()] + m.group(1) + kick + mid + body + m.group(5) + s[m.end():]

if lang == 'en':  # "ADVENTURE" é mais larga que "AVENTURA" no cartaz 9:16
    s = s.replace('    </style>', '      .big h1 { font-size: 262px; }\n    </style>', 1)
if lang == 'es':  # "NUESTRA AVENTURA" no topo 9:16 encostava na marca à direita (16:9 volta a 96px)
    s = s.replace('    </style>', '      #sec { font-size: 86px; }\n    </style>', 1)

# legendas das fotos
src = open(os.path.join(HERE, 'assets', 'fotos.js'), encoding='utf-8').read()
fotos = json.loads(src[src.index('['):src.rindex(']') + 1])
for f in fotos:
    assert f['cap'] in CAPTIONS, 'legenda sem tradução: ' + f['cap']
    f['cap'] = CAPTIONS[f['cap']][col - 1]
open(os.path.join(HERE, 'assets', f'fotos_{lang}.js'), 'w', encoding='utf-8').write(
    f'// Gerado por make_lang.py {lang} — não editar à mão.\nwindow.FOTOS = ' + json.dumps(fotos, ensure_ascii=False, indent=1) + ';\n')

# checagem: palavras PT típicas que não deveriam sobrar no texto visível
vis = re.sub(r'<style>.*?</style>', '', s, flags=re.S)
vis = re.sub(r'/\*.*?\*/|//[^\n]*', '', vis, flags=re.S)
suspeitos = [w for w in ['NOSSO', 'NOSSA', 'Nosso', 'FRONTEIRA', 'ESTRADA', 'QUILÔMETRO', 'PONTE', 'Árvores', 'ÁRVORES', 'Saída', 'Polícia', 'volta a San', 'carros', 'PLANEJADO', 'Planejado', 'pela água', 'turma']
             if re.search(r'[>"`\']' + '[^<"`\']*' + re.escape(w), vis)]
if suspeitos:
    print('ATENÇÃO — possível PT restante:', suspeitos)

os.makedirs(OUT, exist_ok=True)
open(os.path.join(OUT, 'index.html'), 'w', encoding='utf-8').write(s)
for f in ('package.json', 'hyperframes.json', 'meta.json'):
    t = open(os.path.join(HERE, f), encoding='utf-8').read().replace('"huahum-real"', f'"huahum-real-{lang}"')
    open(os.path.join(OUT, f), 'w', encoding='utf-8').write(t)
link = os.path.join(OUT, 'assets')
if not os.path.islink(link):
    os.symlink('../huahum-real/assets', link)
print('ok', OUT)

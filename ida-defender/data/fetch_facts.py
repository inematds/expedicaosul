"""Baixa extratos da Wikipedia. Uso: python3 fetch_facts.py pages.json  (lista de [lang, título])"""
import json, sys, os, time, urllib.parse
from geo_util import get
os.makedirs('facts', exist_ok=True)
for lang, t in json.load(open(sys.argv[1])):
    fn = f"facts/{lang}_{t.replace(' ','_').replace('/','-')}.json"
    if os.path.exists(fn): continue
    u = f"https://{lang}.wikipedia.org/w/api.php?action=query&prop=extracts&explaintext=1&redirects=1&format=json&titles=" + urllib.parse.quote(t)
    d = None
    for a in range(5):
        try: d = json.loads(get(u)); break
        except Exception: time.sleep(8)
    for pid, p in d['query']['pages'].items():
        if pid == '-1': print(lang, t, 'MISSING'); continue
        json.dump(p, open(fn, 'w'), ensure_ascii=False); print(lang, t, len(p.get('extract', '')))
    time.sleep(2.5)

[PT](README.md) · **EN** · [ES](README.es.md)

# Expedição Sul — route animations

[![Expedição Sul](guia/assets/banner.jpg)](https://inematds.github.io/expedicaosul/guia/en/)

Three road trips across the Andes, the pampas, and Uruguay’s coast—turned into **map animations**:
real satellite, the vehicle moving on the actual road, a dashboard with km, altitude, country, and road, and underneath
a **logbook** with real photos and a verified fact about each place you pass through. Each trip comes out in
**9:16** (Reels/Shorts/WhatsApp) and **16:9** (YouTube/TV), 60 fps in the master.

Made with [HyperFrames](https://hyperframes.heygen.com) (HTML → video) and Claude Code, on September 24, 2026.

## 📖 Usage guide

Full guide (the 8 videos + how the route engine works + step-by-step): **https://inematds.github.io/expedicaosul/guia/en/**

---

## The videos

| Trip | Vehicle | Distance | Duration | 9:16 | 16:9 |
|---|---|---|---|---|---|
| **Hua Hum: our plan × our adventure** — the plan and what actually happened (road cut off, border closed), with the trip photos | VW Taos + Land Rover Defender 110 | 54.3 km planned · ≈85 km driven | 174 s | [watch](videos/huahum-plan-and-adventure-9x16-en.mp4) | [watch](videos/huahum-plan-and-adventure-16x9-en.mp4) |
| **Hua Hum** — San Martín de los Andes (AR) ▸ Pirihueico (CL) | Hyundai Tucson + Land Rover Defender 110 | 54.3 km | 74.4 s | [watch](videos/trajeto-hua-hum-9x16.mp4) | [watch](videos/trajeto-hua-hum-16x9.mp4) |
| **The return trip** — San Martín de los Andes ▸ Canela (RS) | Defender 110 | 2,797 km | 113.6 s | [watch](videos/volta-defender-9x16.mp4) | [watch](videos/volta-defender-16x9.mp4) |
| **The outbound trip** — Canela ▸ San Martín de los Andes | Defender 110 | 2,882 km | 95.7 s | [watch](videos/ida-defender-9x16.mp4) | [watch](videos/ida-defender-16x9.mp4) |

<table>
<tr>
<td align="center"><b>Hua Hum</b><br><video src="videos/trajeto-hua-hum-9x16.mp4" poster="videos/trajeto-hua-hum-9x16.jpg" width="240" controls preload="none"></video></td>
<td align="center"><b>The return trip</b><br><video src="videos/volta-defender-9x16.mp4" poster="videos/volta-defender-9x16.jpg" width="240" controls preload="none"></video></td>
<td align="center"><b>The outbound trip</b><br><video src="videos/ida-defender-9x16.mp4" poster="videos/ida-defender-9x16.jpg" width="240" controls preload="none"></video></td>
</tr>
</table>

> The files in this repository are the web version (30 fps, ~43 MB). The 60 fps masters (300+ MB) are outside git.

### Hua Hum (54.3 km, 1 border)
San Martín de los Andes → Lago Lácar → highest point of the day (1,038 m, km 16.5, on the RP48 gravel road) → Playa de Yuco →
Lago Nonthué → Puerto Hua Hum → **Paso Hua Hum** (AR ▸ CL border, km 43.7) → Ruta CH-203 → Puerto Pirehueico.

### The return trip (2,797 km, 3 countries)
San Martín de los Andes → descent from the Andes via RN 237/RN 22 → Río Colorado ("goodbye, Patagonia") → Bahía Blanca →
Azul → Moreno → Buenos Aires → **Colonia Express ferry across the Río de la Plata (51 km, 1h15)** → Colonia del Sacramento →
Paso de los Toros → **Fronteira da Paz** (Rivera/Sant'Ana do Livramento) → BR-158/BR-290 → Porto Alegre → Canela.

### The outbound trip (2,882 km, 3 countries)
Canela → BR-471 via Taim → **Chuí/Chuy** (BR ▸ UY) → La Paloma → Pueblo Garzón (the old train station) →
Punta del Este → San Carlos → Colonia → **ferry to Buenos Aires** → Moreno → RN 5 → Santa Rosa → Río Colorado in
25 de Mayo ("hello, Patagonia") → San Martín de los Andes.

---

## How it was made

A single **route animation engine** (HTML + GSAP, rendered by HyperFrames) reads three data files and draws
everything from **one single clock**—car position, camera, traveled line, pins, HUD, altitude track, and data cards
all come from the same time function, so nothing falls out of sync.

| Layer | Source |
|---|---|
| Route (road) | OSRM, by legs between the Google Maps link’s stops |
| Ferry | the OSM line for **Colonia Express** (Buenos Aires ↔ Colonia), with the duration marked in OSM |
| Satellite | Esri World Imagery — overview (z7), corridor (z8) and high-res cutouts (z10/z12) at each stop; each cutout only appears when it covers the whole frame |
| Lakes (Hua Hum) | repainted with OSM water polygons (removes mosaic reflection blotches) |
| Borders | OSM (admin_level=2) in border cities; Natural Earth at the continental scale |
| Altitude | SRTM 30 m via OpenTopoData (altitude track, HUD and data cards) |
| Card facts | Wikipedia (ES/PT/EN), each sentence with the saved source in `*/data/facts/` |
| Photos | Wikimedia Commons, checked by category/location, with author and license |
| Vehicles and ferry seen from above | generated in local flux2-klein and cropped (chroma key) |
| Tracks | generated (Lyria 3 Pro) and **analyzed** (BPM, groove entry, silence): the car sets off when the beat hits, the ferry crosses during the calm segment, and the border stamp drops on the music’s return |

### Structure

```
trajeto-hua-hum/        vídeo Hua Hum (motor v1, dois carros) + data/ (scripts e dados)
trajeto-hua-hum-16x9/   variante 16:9
huahum-real/            Hua Hum "nosso plano × nossa aventura": 3 quadros (mapa geral fixo, detalhado, fotos da viagem),
                        agenda por carro com ida/volta; data/fotos.txt → build_fotos.py; make_16x9.py próprio
huahum-real-16x9/       variante 16:9 (gerada por huahum-real/make_16x9.py)
volta-defender/         motor genérico de rota longa + assets/trip.js da volta
volta-defender-16x9/    variante 16:9 (assets por link simbólico)
ida-defender/           mesmo motor + assets/trip.js da ida
ida-defender-16x9/
make_16x9.py            gera a variante 16:9 trocando só os blocos de layout
render_share.sh         render 60 fps + versão de compartilhar (-14 LUFS)
tg_encode.sh            versão ≤ 44 MB (Telegram / web)
videos/                 os 8 vídeos (versão web) + capas
FALHAS.md               changelog de falhas corrigidas
```

### New trip with the engine

1. `data/`: OSRM routes by legs + `build_route2.py trip.json` (single route, ferry, border, altitude, stops).
2. `build_tiles.py route_full.json ../assets` (satellite), `photos_search.py` / `photos_get.py` (photos + credits), `fetch_facts.py` (facts).
3. Write `assets/trip.js`: arrival/departure schedule per stop (synced to the music — `beat.py` measures BPM and phase), cards, border stamps, labels.
4. `npx hyperframes check` → `python3 make_16x9.py <proj> <proj>-16x9` → `render_share.sh`.

---

## Production statistics

Measured in Claude Code session logs (tokens per call), not estimated. Cost in **API dollar equivalent** from the official table
(Opus 5.5: US$ 4 input / 20 output / 0.20 cache read / 8 cache write 1 h, per million tokens;
Haiku 4.5: 1 / 5 / 0.10 / 2). If you use Claude Code via subscription you don’t pay this per-use value—use it for comparison.

### Cost and time per video

| Video | Agent active time | Calls | AI cost (US$) | Magnific credits | Local render |
|---|---|---|---|---|---|
| Hua Hum 9:16 | 55 min | 89 | **13.12** | 190 | 3 × ~1m50 |
| Hua Hum 16:9 | ~5 min | 8 | **1.07** | — | 1m44 |
| The return trip (9:16 + 16:9) | 38.5 min | 53 + 5 subagents | **15.18** | 180 | 4 × ~2m40 |
| The outbound trip (9:16 + 16:9) | 24.4 min | 37 + 4 subagents | **6.85** | 160 | 2 × ~2m15 |
| **Total** | **~2h03** | **187 + 9** | **36.22** | **530** | ~24 min |

Cost breakdown: main agent (Opus 5.5) US$ 30.97 · reviewer (3 queries, Opus 5.5) US$ 4.32 ·
subagents (Haiku 4.5, mechanical tasks: download satellite and photos, generate sprite, render) US$ 0.93.
Zero cost: local image generation (flux2-klein, ~2 min of GPU) and all renders (HyperFrames local).
Magnific credits: 3 tracks × 160 + effects (whoosh, border stamp, ship horn).

### Cache volume (tokens)

| Video | Read from cache | Written to cache (1 h) | Input without cache | Output | Cache hit |
|---|---|---|---|---|---|
| Hua Hum 9:16 | 24.64 M | 383k | 538k (reviewer) | 136k + 14k (reviewer) | 98.5% |
| Hua Hum 16:9 | 3.33 M | 20k | — | 12k | 99.4% |
| The return trip | 29.59 M + 1.27 M (subag.) | 588k + 319k (subag.) | 439k (reviewer) | 105k + 15k | 98.0% |
| The outbound trip | 23.20 M + 0.63 M (subag.) | 112k + 224k (subag.) | — | 48k + 4k | 99.5% |

Reading the numbers:
- **98–99.5% of the input came from cache** — that’s what keeps the cost low despite ~85 M tokens read.
- **The reviewer is expensive per call**: it sends the whole conversation without cache (~300–540k tokens per query).
- **16:9 costs almost nothing** (US$ 1.07 in Hua Hum; for the return trip and the outbound trip it’s just layout swap + render).
- **The outbound trip cost less than half the return trip**: the return trip paid for building the generic engine, the outbound trip only reused it.
- A long pause knocks the cache down (1 h validity): a question asked 8 h later re-recorded ~760k tokens (US$ 7.41).

---

## Credits

**Map and data:** Esri World Imagery (Esri, Maxar, Earthstar Geographics) · © OpenStreetMap contributors (ODbL) ·
Natural Earth · OSRM · SRTM 30 m via OpenTopoData · Wikipedia (ES/PT/EN).

**Photos (Wikimedia Commons):**
- Hua Hum — Albasmalko (public domain) · Marco Antonio Correa Flores (CC BY-SA 4.0) · Falk2 (CC BY-SA 4.0) · Gervacio Rosales (CC BY 3.0) · Manueldutruel (CC BY-SA 4.0).
- The return trip — Albasmalko · Alvaro Errandonea (CC BY 3.0) · Juan Corral / Municipalidad de Bahía Blanca (CC BY 2.5 AR) · Elquache (CC BY-SA 3.0) · Walteriot (CC BY-SA 3.0) · NASA JSC Earth Sciences (public domain) · Roxyuru (CC BY-SA 3.0) · Diego Delso (CC BY-SA 3.0) · bullit (CC BY 3.0) · Zeroth (CC BY-SA 4.0) · Mx. Granger (CC0) · Fernando da Rosa (CC BY-SA 3.0) · Ricardo André Frantz (CC BY-SA 3.0) · Cristine Denardi Huff (CC BY-SA 4.0) · Rosanetur (CC BY 2.0) · Fernando Schultz Aldado (public domain).
- The outbound trip — Rosanetur · Fernando Schultz Aldado · Giácomo Luiz Mancini (CC BY-SA 4.0) · John Seb Barber (CC BY 2.0) · Granjuanlll (CC BY-SA 3.0) · Jimmy Baikovicius (CC BY-SA 2.0) · Eduardo.terian (CC BY-SA 3.0) · María Cecilia (CC0) · mriaco (CC BY 3.0) · NaBUru38 (CC BY-SA 4.0) · Diego Delso · bullit · Roxyuru · NASA JSC · Walteriot · Juanedc (CC BY 2.0) · Jmmuguerza (CC BY-SA 4.0) · Silvio omar (CC BY-SA 4.0) · Albasmalko · Marco Antonio Correa Flores.

**Generated by AI:** vehicles and ferry seen from above (flux2-klein) · tracks and sound effects (Magnific — Lyria 3 Pro / ElevenLabs).

Open content from [INEMA.CLUB](https://inema.club).

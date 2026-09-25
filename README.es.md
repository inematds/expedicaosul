[PT](README.md) · [EN](README.en.md) · **ES**

# Expedição Sul — animaciones de recorrido

[![Expedição Sul](guia/assets/banner.jpg)](https://inematds.github.io/expedicaosul/guia/es/)

Tres viajes en auto por los Andes, por la pampa y por la costa de Uruguay, convertidos en **animaciones de mapa**:
satélite real, el vehículo avanzando por la carretera real, panel con km, altitud, país y carretera, y abajo un
**diario de a bordo** con foto real y un dato verificado de cada lugar por el que se pasa. Cada viaje sale en
**9:16** (Reels/Shorts/WhatsApp) y **16:9** (YouTube/TV), 60 fps en el master.

Hecho con [HyperFrames](https://hyperframes.heygen.com) (HTML → video) y Claude Code, el 24/09/2026.

## 📖 Guía de uso

Guía completa (los 8 videos + cómo funciona el motor de ruta + paso a paso): **https://inematds.github.io/expedicaosul/guia/es/**

---

## Los videos

| Viaje | Vehículo | Distancia | Duración | 9:16 | 16:9 |
|---|---|---|---|---|---|
| **Hua Hum: nuestro plan × nuestra aventura** — el plan y lo que pasó (camino cortado, frontera cerrada), con las fotos del viaje | VW Taos + Land Rover Defender 110 | 54,3 km planeados · ≈85 km recorridos | 174 s | [ver](videos/huahum-plan-y-aventura-9x16-es.mp4) | [ver](videos/huahum-plan-y-aventura-16x9-es.mp4) |
| **Hua Hum** — San Martín de los Andes (AR) ▸ Pirihueico (CL) | Hyundai Tucson + Land Rover Defender 110 | 54,3 km | 74,4 s | [ver](videos/trajeto-hua-hum-9x16.mp4) | [ver](videos/trajeto-hua-hum-16x9.mp4) |
| **La vuelta** — San Martín de los Andes ▸ Canela (RS) | Defender 110 | 2.797 km | 113,6 s | [ver](videos/volta-defender-9x16.mp4) | [ver](videos/volta-defender-16x9.mp4) |
| **La ida** — Canela ▸ San Martín de los Andes | Defender 110 | 2.882 km | 95,7 s | [ver](videos/ida-defender-9x16.mp4) | [ver](videos/ida-defender-16x9.mp4) |

<table>
<tr>
<td align="center"><b>Hua Hum</b><br><video src="videos/trajeto-hua-hum-9x16.mp4" poster="videos/trajeto-hua-hum-9x16.jpg" width="240" controls preload="none"></video></td>
<td align="center"><b>La vuelta</b><br><video src="videos/volta-defender-9x16.mp4" poster="videos/volta-defender-9x16.jpg" width="240" controls preload="none"></video></td>
<td align="center"><b>La ida</b><br><video src="videos/ida-defender-9x16.mp4" poster="videos/ida-defender-9x16.jpg" width="240" controls preload="none"></video></td>
</tr>
</table>

> Los archivos de este repositorio son la versión web (30 fps, ~43 MB). Los masters 60 fps (300+ MB) quedan fuera de git.

### Hua Hum (54,3 km, 1 frontera)
San Martín de los Andes → Lago Lácar → punto más alto del día (1.038 m, km 16,5, en la RP48 de ripio) → Playa de Yuco →
Lago Nonthué → Puerto Hua Hum → **Paso Hua Hum** (frontera AR ▸ CL, km 43,7) → Ruta CH-203 → Puerto Pirehueico.

### La vuelta (2.797 km, 3 países)
San Martín de los Andes → descenso de los Andes por la RN 237/RN 22 → Río Colorado ("adiós, Patagonia") → Bahía Blanca →
Azul → Moreno → Buenos Aires → **balsa Colonia Express por el Río de la Plata (51 km, 1h15)** → Colonia del Sacramento →
Paso de los Toros → **Fronteira da Paz** (Rivera/Sant'Ana do Livramento) → BR-158/BR-290 → Porto Alegre → Canela.

### La ida (2.882 km, 3 países)
Canela → BR-471 por Taim → **Chuí/Chuy** (BR ▸ UY) → La Paloma → Pueblo Garzón (la antigua estación de tren) →
Punta del Este → San Carlos → Colonia → **balsa hasta Buenos Aires** → Moreno → RN 5 → Santa Rosa → Río Colorado en
25 de Mayo ("hola, Patagonia") → San Martín de los Andes.

---

## Cómo se hizo

Un único **motor de animación de ruta** (HTML + GSAP, renderizado por HyperFrames) lee tres archivos de datos y dibuja
todo a partir de **un solo reloj** — posición del auto, cámara, línea recorrida, pines, HUD, riel de altitud y cards
salen de la misma función de tiempo, así que nada queda fuera de sincronía.

| Capa | Fuente |
|---|---|
| Ruta (carretera) | OSRM, por tramos entre las paradas del enlace de Google Maps |
| Balsa | línea OSM de **Colonia Express** (Buenos Aires ↔ Colonia), con la duración marcada en OSM |
| Satélite | Esri World Imagery — vista general (z7), corredor (z8) y recortes en alta (z10/z12) en cada parada; cada recorte solo aparece cuando cubre todo el cuadro |
| Lagos (Hua Hum) | repintados con los polígonos de agua de OSM (quita manchas de reflejo del mosaico) |
| Fronteras | OSM (admin_level=2) en ciudades fronterizas; Natural Earth en escala continental |
| Altitud | SRTM 30 m vía OpenTopoData (riel de altitud, HUD y cards de datos) |
| Datos de los cards | Wikipedia (ES/PT/EN), cada frase con fuente guardada en `*/data/facts/` |
| Fotos | Wikimedia Commons, verificadas por categoría/lugar, con autor y licencia |
| Vehículos y balsa vistos desde arriba | generados en flux2-klein local y recortados (croma key) |
| Pistas musicales | generadas (Lyria 3 Pro) y **analizadas** (BPM, entrada del groove, silencio): el auto arranca cuando entra el beat, la balsa cruza en el tramo tranquilo y el sello de frontera cae en el retorno de la música |

### Estructura

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

### Nuevo viaje con el motor

1. `data/`: rutas OSRM por tramos + `build_route2.py trip.json` (ruta única, balsa, frontera, altitud, paradas).
2. `build_tiles.py route_full.json ../assets` (satélite), `photos_search.py` / `photos_get.py` (fotos + créditos), `fetch_facts.py` (datos).
3. Escribir `assets/trip.js`: agenda de llegada/salida por parada (sincronizada con la música — `beat.py` mide BPM y fase), cards, sellos de frontera, rótulos.
4. `npx hyperframes check` → `python3 make_16x9.py <proj> <proj>-16x9` → `render_share.sh`.

---

## Estadísticas de producción

Medido en los logs de la sesión de Claude Code (tokens por llamada), no estimado. Costo en **dólar equivalente de API** por la tabla
oficial (Opus 5.5: US$ 4 entrada / 20 salida / 0,20 lectura de cache / 8 escritura de cache 1 h, por millón de tokens;
Haiku 4.5: 1 / 5 / 0,10 / 2). Quien usa Claude Code con suscripción no paga ese valor por uso — sirve para comparar.

### Costo y tiempo por video

| Video | Tiempo activo del agente | Llamadas | Costo IA (US$) | Créditos Magnific | Render local |
|---|---|---|---|---|---|
| Hua Hum 9:16 | 55 min | 89 | **13,12** | 190 | 3 × ~1m50 |
| Hua Hum 16:9 | ~5 min | 8 | **1,07** | — | 1m44 |
| La vuelta (9:16 + 16:9) | 38,5 min | 53 + 5 subagentes | **15,18** | 180 | 4 × ~2m40 |
| La ida (9:16 + 16:9) | 24,4 min | 37 + 4 subagentes | **6,85** | 160 | 2 × ~2m15 |
| **Total** | **~2h03** | **187 + 9** | **36,22** | **530** | ~24 min |

Composición del costo: agente principal (Opus 5.5) US$ 30,97 · revisor (3 consultas, Opus 5.5) US$ 4,32 ·
subagentes (Haiku 4.5, tareas mecánicas: bajar satélite y fotos, generar sprite, renderizar) US$ 0,93.
Costo cero: generación de imagen local (flux2-klein, ~2 min de GPU) y todos los renders (HyperFrames local).
Créditos Magnific: 3 pistas musicales × 160 + efectos (whoosh, sello, bocina de barco).

### Volumen de cache (tokens)

| Video | Leídos del cache | Grabados en cache (1 h) | Entrada sin cache | Salida | Acierto de cache |
|---|---|---|---|---|---|
| Hua Hum 9:16 | 24,64 M | 383 mil | 538 mil (revisor) | 136 mil + 14 mil (revisor) | 98,5% |
| Hua Hum 16:9 | 3,33 M | 20 mil | — | 12 mil | 99,4% |
| La vuelta | 29,59 M + 1,27 M (subag.) | 588 mil + 319 mil (subag.) | 439 mil (revisor) | 105 mil + 15 mil | 98,0% |
| La ida | 23,20 M + 0,63 M (subag.) | 112 mil + 224 mil (subag.) | — | 48 mil + 4 mil | 99,5% |

Lectura de los números:
- **98–99,5% de la entrada vino del cache** — es lo que mantiene el costo bajo pese a ~85 M tokens leídos.
- **El revisor es caro por llamada**: envía toda la conversación sin cache (~300–540 mil tokens por consulta).
- **El 16:9 casi no cuesta** (US$ 1,07 en Hua Hum; en la vuelta y en la ida es solo cambio de layout + render).
- **La ida costó menos de la mitad que la vuelta**: la vuelta pagó la construcción del motor genérico, la ida solo reutilizó.
- Una pausa larga derrumba el cache (validez de 1 h): una pregunta hecha 8 h después volvió a grabar ~760 mil tokens (US$ 7,41).

---

## Créditos

**Mapa y datos:** Esri World Imagery (Esri, Maxar, Earthstar Geographics) · © colaboradores de OpenStreetMap (ODbL) ·
Natural Earth · OSRM · SRTM 30 m vía OpenTopoData · Wikipedia (ES/PT/EN).

**Fotos (Wikimedia Commons):**
- Hua Hum — Albasmalko (dominio público) · Marco Antonio Correa Flores (CC BY-SA 4.0) · Falk2 (CC BY-SA 4.0) · Gervacio Rosales (CC BY 3.0) · Manueldutruel (CC BY-SA 4.0).
- La vuelta — Albasmalko · Alvaro Errandonea (CC BY 3.0) · Juan Corral / Municipalidad de Bahía Blanca (CC BY 2.5 AR) · Elquache (CC BY-SA 3.0) · Walteriot (CC BY-SA 3.0) · NASA JSC Earth Sciences (dominio público) · Roxyuru (CC BY-SA 3.0) · Diego Delso (CC BY-SA 3.0) · bullit (CC BY 3.0) · Zeroth (CC BY-SA 4.0) · Mx. Granger (CC0) · Fernando da Rosa (CC BY-SA 3.0) · Ricardo André Frantz (CC BY-SA 3.0) · Cristine Denardi Huff (CC BY-SA 4.0) · Rosanetur (CC BY 2.0) · Fernando Schultz Aldado (dominio público).
- La ida — Rosanetur · Fernando Schultz Aldado · Giácomo Luiz Mancini (CC BY-SA 4.0) · John Seb Barber (CC BY 2.0) · Granjuanlll (CC BY-SA 3.0) · Jimmy Baikovicius (CC BY-SA 2.0) · Eduardo.terian (CC BY-SA 3.0) · María Cecilia (CC0) · mriaco (CC BY 3.0) · NaBUru38 (CC BY-SA 4.0) · Diego Delso · bullit · Roxyuru · NASA JSC · Walteriot · Juanedc (CC BY 2.0) · Jmmuguerza (CC BY-SA 4.0) · Silvio omar (CC BY-SA 4.0) · Albasmalko · Marco Antonio Correa Flores.

**Generado por IA:** vehículos y ferry vistos desde arriba (flux2-klein) · pistas musicales y efectos de sonido (Magnific — Lyria 3 Pro / ElevenLabs).

Contenido abierto de [INEMA.CLUB](https://inema.club).

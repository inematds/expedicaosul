---
workflow: general-video
flow: automation
storyboard: no
message: "O comboio (Hyundai Tucson + Land Rover Defender 110 branca) cruza os Andes de San Martín de los Andes (AR) a Pirihueico (CL) pelo Paso Hua Hum — 54,3 km, 1 fronteira."
language: pt-BR
aspect: "9:16"
length: "~72s"
destination: redes sociais / WhatsApp (vertical)
---

## Intent

Pedido do usuário (verbatim): "quero que faca uma animação incrivel deste trajeto colocando imagens mostrando em um quadro o trajeto de dois carros andando e abaixo texto animacao e imagens de onde passamos, faca melhor q um profissional possa fazer. o carro é hunday tucson e uma defender 110 branca" + link do Google Maps (-40.1634936,-71.3558054 → Pirihueico, Panguipulli).

Conceito: **diário de bordo de expedição** — o mapa de satélite é o instrumento ao vivo (quadro superior, HUD com km, altitude, estrada, país), e o painel inferior é o diário que registra cada lugar quando o comboio passa (foto real + km + fato verificado).

## Decisões — respondidas pelo usuário
- Trajeto: link do Google Maps (origem/destino).
- Carros: Hyundai Tucson + Land Rover Defender 110 branca.
- Layout: quadro com o trajeto e os dois carros; abaixo texto, animação e imagens dos lugares.

## Decisões — inferidas (corrigir aqui)
- Formato 9:16 1080×1920, 60 fps (o layout "mapa em cima / diário embaixo" encaixa no vertical).
- Cor do Tucson: prata/cinza (não informada). Defender: geração nova (L663) — não informado se é a clássica.
- Carros no mapa são sprites vistos de cima gerados no flux2-klein (não fotos dos carros reais).
- Fotos dos lugares: Wikimedia Commons (licenças livres, créditos no fim).
- Fatos: Wikipedia ES + OSM + SRTM, salvos em `data/`.
- Trilha: gerada (Magnific / Lyria 3 Pro), instrumental; SFX: whoosh + carimbo na fronteira.
- Sem narração.

## Assets
- Rota: OSRM (`data/osrm.json`), POIs OSM (`data/overpass_pois.json`), altimetria SRTM30m (`data/elev.json`), fronteira OSM admin_level=2 (`data/border_osm.json`).
- Mapa: Esri World Imagery com lagos repintados a partir dos polígonos OSM (`data/water.py`).
- Superfície km 16,5: OSM RP48 surface=compacted (ripio) — verificado 2026-09-24.

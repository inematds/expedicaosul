---
workflow: general-video
flow: automation
storyboard: no
message: "Hua Hum: o plano (SMA ▸ Pirihueico, 54,3 km) e a estrada real — curva interrompida no km 32,1, Taos volta, Defender chega à ponte do Río Hua Hum, fronteira fechada por desmoronamentos, volta a San Martín."
language: pt-BR
aspect: "9:16"
length: "93,6 s"
destination: redes sociais / WhatsApp
---

## Intent

Pedido (2026-09-25, verbatim): "quero q no video do humhum o carro Volkswagen Taos prata, em vez do tuscon, e a landdefender 110 é uma do estilo de 2000, quero q apresente o roteiro interiro em uma parte onde o carro anda e o outro pdoe ser como vc ja tem. o video em duas partes uma o plano indo do inicio ao final em viusaul de toda rota. ai comeca nosso roteiro na primeira curva apos a altura do cafe quchuquina tivemos um interupcao pois teve arvores caidas e agua tranbordando. entao o carro taos voltou e a gente seguiu ate humhum tinha policia em uma ponte ou algo assim e ficou a fronteira fechada nao pudemos ir voltamos assim, quero um video com estes detalhes ida e volta apresentando minhas fontos tambem o tempo todo. faca e depois lhe mando o link das fotos"

Complemento: "o passo hua hum estava com muitos demoronamentos de pedra tambem para parte do chile"

## Estrutura v3 (2026-09-25) — pedido: "tem que ficar claro o que era o plano", 3 quadros, fotos sem movimento, aventura bem mais longa
- **Três quadros:** mapa geral fixo (os dois carros sempre visíveis) · mapa detalhado (segue a Defender) · fotos paradas (só fade).
- **Nosso plano (0–38,4 s):** comboio visita as 8 paradas do plano (3,6 s cada) com fotos de referência do Commons.
- **Nossa aventura (38,4–174 s):** saída → mirador → rípio/neve → Yuco → Lácar/café → curva interrompida (88,8) → Taos volta · Defender segue → Puerto Hua Hum → polícia na ponte (124,8) → fronteira fechada (127,2) → volta (até 158,4) → resumo e créditos.
- Trilha de 96 s emendada no compasso: 0–72 | 21,6–72 | 43,2–94,8. Total 174 s.
- 43 fotos da viagem (hora do EXIF na legenda), escolhidas das 175 do zip pelas miniaturas embutidas (`data/fotos_scan.py`).

## Decisões — inferidas (corrigir aqui)
- **Km 32,1** = primeira curva depois do Café Quechuquina (café no OSM, km 31,7 da RP48; curva medida pela mudança de rumo da rota).
- **Polícia no km 42,48** = ponte da RP48 sobre o Río Hua Hum ("Paso Internacional Hua Hum" no OSM), 1,2 km antes do Complejo Fronterizo. O usuário disse "uma ponte ou algo assim".
- Taos parou atrás da Defender na curva e voltou dali; a Defender passou pela água.
- Km do resumo: Defender ≈ 85 (2 × 42,5), Taos ≈ 64 (2 × 32).
- Carros: sprites flux2-klein (`data/gen_cars2.py`, recorte `data/cut_cars2.py`) — VW Taos prata; Land Rover Defender 110 clássica (~2000, Td5 branca, rack de teto).

## Fotos
Carrossel contínuo no painel (7,2–84 s). Lista em `data/fotos.txt` → `python3 data/build_fotos.py` → `assets/fotos.js`.
Fotos da viagem vão em `assets/fotos/`. Espaços sem arquivo aparecem como "SUA FOTO" (rascunho). As do Commons em `assets/photos/` são provisórias.

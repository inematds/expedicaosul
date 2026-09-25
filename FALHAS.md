| data | o que quebrou | menor correção | prompt \| infra |
|---|---|---|---|
| 2026-09-25 | Clarão branco do cartaz AVENTURA cobria o vídeo desde t=0 | `tl.fromTo` aplica o estado inicial na hora; trocar por `tl.set` + `tl.to` no instante do impacto | prompt |
| 2026-09-25 | Zip de 1 GB de fotos pelo drive remoto a 250 KB/s (~70 min) | ler só o cabeçalho de cada JPG (EXIF + miniatura embutida) e baixar inteiras só as escolhidas | infra |
| 2026-09-24 | HUD mostrava ARGENTINA/FERRY após desembarcar em Colonia | parada arredondada (1654,3) < fim da balsa (1654,33): encaixar paradas da balsa no km exato + tolerância 0,1 km | prompt |
| 2026-09-24 | Texto do card antigo sobrepunha o novo na troca | tirar o bloco de texto antes (e−0,05 s) e só depois a foto | prompt |
| 2026-09-24 | Rótulos/pinos com opacidade 0 acusados como sobreposição e colisão de rótulos na visão geral | visibility hidden quando opacidade≈0 + anti-colisão + lista de rótulos-chave por viagem | prompt |
| 2026-09-24 | OSRM roteava Buenos Aires→Colonia por estrada (481 km) em vez da balsa | pernas separadas ancoradas nas pontas da linha OSM do ferry (Colonia Express) | prompt |
| 2026-09-24 | Linha do perfil CH-203 cortada antes do fim (animação draw-on) | strokeDasharray maior que o comprimento do path (700→1400) | prompt |
| 2026-09-24 | build_route.py StopIteration ao achar o passo "CH 203" no OSRM | casar por substring '203' em ref+name | prompt |
| 2026-09-24 | Rótulos de mapa/títulos com opacidade 0 acusados como sobreposição no check | visibility hidden depois do fade + declutter por distância (HUD/carros) | prompt |

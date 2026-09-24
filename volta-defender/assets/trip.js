/* Configuração da viagem: A VOLTA (San Martín de los Andes → Canela), só a Defender 110.
   Tempos alinhados à trilha: groove entra em 9,4 s; silêncio 60–64,6 s (balsa); volta em 64,8 s; fade 106–113,6 s.
   Fatos: Wikipedia (data/facts), OSM (balsa, fronteira), SRTM (altitudes), OSRM (distâncias/tempo). */
window.TRIP = {
  dur: 113.6,
  title: { k: "EXPEDIÇÃO SUL · A VOLTA", lines: ["Dos Andes", "à Serra", "<span class=\"arrow\">▸</span> Gaúcha"] },
  brandSub: "AR ▸ UY ▸ BR",
  intro: {
    vehicle: "DEFENDER 110", sub: "LAND ROVER · BRANCA",
    chips: [["2.797", "KM", "DE ESTRADA E ÁGUA"], ["3", "PAÍSES", "AR · UY · BR"], ["1", "BALSA", "RÍO DE LA PLATA"]],
  },
  // agenda das paradas (arr = chega, dep = sai) — só as do link
  schedule: [
    { id: "sma", dep: 9.4, dwellKm: 42 },
    { id: "bb", arr: 27.0, dep: 28.2, dwellKm: 42 },
    { id: "moreno", arr: 44.4, dep: 45.6, dwellKm: 40 },
    { id: "ferry_ba", arr: 50.6, dep: 56.2, dwellKm: 80 },
    { id: "ferry_col", arr: 64.8, dep: 66.4, dwellKm: 50 },
    { id: "livramento", arr: 78.0, dep: 79.6, dwellKm: 40 },
    { id: "poa", arr: 91.0, dep: 92.2, dwellKm: 55 },
    { id: "canela", arr: 97.6, dwellKm: 40 },
  ],
  ferry: { dep: 56.2, arr: 64.8 },
  outro: { t0: 99.6, t1: 102.8 },
  ovLabels: ["sma", "bb", "ferry_ba", "ferry_col", "livramento", "canela"],
  countries: [["AR", "ARGENTINA"], ["UY", "URUGUAI"], ["BR", "BRASIL"]], // AR até o fim da balsa, UY até a fronteira, BR depois
  stamps: [
    { t: 64.8, s1: "ARGENTINA ▸ URUGUAI", s2: "COLONIA", s3: "KM 1.654 · FIM DA BALSA" },
    { t: 78.0, s1: "URUGUAI ▸ BRASIL", s2: "FRONTEIRA DA PAZ", s3: "KM 2.180 · RIVERA–LIVRAMENTO" },
  ],
  mapLabels: [
    ["ARGENTINA", -64.6, -36.4, "country", 46],
    ["URUGUAI", -55.2, -33.3, "country", 40],
    ["BRASIL", -54.3, -28.6, "country", 40],
    ["CHILE", -71.9, -36.3, "country", 34],
    ["OCEANO ATLÂNTICO", -56.5, -38.0, "sea", 30],
    ["RÍO DE LA PLATA", -56.3, -35.55, "sea", 20],
  ],
  cards: [
    { id: "sma", s: 7.2, e: 13.2, img: "sma", km: "0", kick: "KM 0 · NEUQUÉN · ARGENTINA", ttl: "San Martín de los Andes", body: "Começa a volta: <em>2.797 km</em> até Canela, cruzando a Argentina, o Uruguai e o sul do Brasil." },
    { id: "descida", s: 13.2, e: 19.6, data: { big: "925", unit: "KM", lab1: "SAN MARTÍN ▸ BAHÍA BLANCA", lab2: "DE 1.046 M A 26 M", k0: 0, k1: 924.9, ax0: "1.046 M · KM 115", ax1: "26 M · BAHÍA BLANCA" }, kick: "RN 237 · RN 22 · ESTEPA", ttl: "Descendo os Andes", body: "Da cordilheira ao pampa: a estrada perde mais de <em>1.000 m</em> de altitude até o Atlântico." },
    { id: "riocolorado", s: 19.6, e: 27.0, img: "riocolorado", km: "757", kick: "KM 757 · RN 22 · PASSAGEM", ttl: "Adeus, Patagônia", body: "O <em>Río Colorado</em> marca, por tradição, o limite norte da Patagônia argentina." },
    { id: "bb", s: 27.0, e: 36.0, img: "bahiablanca", km: "925", kick: "KM 925 · BUENOS AIRES · ARGENTINA", ttl: "Bahía Blanca", body: "Fundada em 1828 como <em>“Fortaleza Protectora Argentina”</em>. 335.180 habitantes (censo 2022)." },
    { id: "azul", s: 36.0, e: 44.4, img: "azul", km: "1.270", kick: "KM 1.270 · RN 3 · PASSAGEM", ttl: "Azul", body: "A <em>“cidade cervantina”</em>: a Casa Ronco guarda a maior coleção de Cervantes fora da Espanha." },
    { id: "moreno", s: 44.4, e: 50.6, img: "moreno", km: "1.560", kick: "KM 1.560 · GRANDE BUENOS AIRES", ttl: "Moreno", body: "Oeste da Grande Buenos Aires, <em>576.632 habitantes</em> (censo 2022). O povoado nasceu com a ferrovia, em 1860." },
    { id: "ferry_ba", s: 50.6, e: 56.2, img: "coloniaexpress", km: "1.603", kick: "KM 1.603 · PUERTO MADERO SUR", ttl: "Colonia Express", body: "A Defender embarca: <em>51 km de balsa</em> pelo Río de la Plata até o Uruguai (1h15)." },
    { id: "rioplata", s: 56.2, e: 64.8, img: "rioplata", km: "1.628", kick: "EM PLENO RIO · BALSA", ttl: "Río de la Plata", body: "Nasce da união dos rios <em>Paraná e Uruguai</em> e deságua no Atlântico." },
    { id: "ferry_col", s: 64.8, e: 72.0, img: "colonia", inset: "colonia2", km: "1.654", kick: "KM 1.654 · URUGUAI", ttl: "Colonia del Sacramento", body: "Fundada por portugueses em 1680, a cidade mais antiga do Uruguai. Bairro histórico: <em>Patrimônio da Humanidade</em> (1995)." },
    { id: "pasotoros", s: 72.0, e: 78.0, img: "pasotoros", km: "1.929", kick: "KM 1.929 · RUTA 5 · PASSAGEM", ttl: "Paso de los Toros", body: "Às margens do <em>Río Negro</em>, no cruzamento da Ruta 5 — perto da represa de Rincón del Bonete." },
    { id: "livramento", s: 78.0, e: 84.0, img: "rivera", inset: "rivera2", km: "2.180", kick: "KM 2.180 · FRONTEIRA URUGUAI–BRASIL", ttl: "Fronteira da Paz", body: "Rivera e Sant'Ana do Livramento: duas cidades, dois países, separados por uma <em>linha imaginária</em>." },
    { id: "saogabriel", s: 84.0, e: 91.0, data: { big: "493", unit: "KM", lab1: "LIVRAMENTO ▸ PORTO ALEGRE", lab2: "BR-158 · BR-290", k0: 2181.5, k1: 2673.6, ax0: "218 M · LIVRAMENTO", ax1: "50 M · PORTO ALEGRE" }, kick: "KM 2.346 · SÃO GABRIEL · PASSAGEM", ttl: "Pampa gaúcho", body: "Pela BR-290, São Gabriel, a <em>“Terra dos Marechais”</em>, no coração do bioma Pampa." },
    { id: "poa", s: 91.0, e: 97.6, img: "poa", inset: "poa2", km: "2.674", kick: "KM 2.674 · RIO GRANDE DO SUL", ttl: "Porto Alegre", body: "A capital gaúcha às margens do <em>Guaíba</em>: quase 1,4 milhão de habitantes." },
    { id: "canela", s: 97.6, e: 104.0, img: "canela", inset: "canela2", km: "2.797", kick: "KM 2.797 · SERRA GAÚCHA · CHEGADA", ttl: "Canela", body: "A <em>837 m</em> de altitude, terra da Catedral de Pedra e da Cascata do Caracol. Fim da volta." },
    { id: "summary", s: 104.0, e: 109.0, stats: [["2.797", "KM", "DE ESTRADA E BALSA"], ["3", "PAÍSES", "AR ▸ UY ▸ BR"], ["51", "KM", "DE BALSA · 1H15"], ["≈38", "H", "AO VOLANTE (EST.)"]], kick: "DIÁRIO DE BORDO · RESUMO", ttl: "De volta", body: "San Martín de los Andes ▸ Canela, de <em>Defender 110</em>, com uma travessia do Río de la Plata no meio." },
  ],
  endTitle: { k: "DE VOLTA · 2.797 KM", h: "Andes <span class=\"accent\">▸</span> Serra" },
  credits: {
    s: 109.0,
    photos: "Albasmalko (dom. público) · Alvaro Errandonea (CC BY 3.0) · Juan Corral / Municipalidad de Bahía Blanca (CC BY 2.5 AR) · Elquache (CC BY-SA 3.0) · Walteriot (CC BY-SA 3.0) · NASA JSC Earth Sciences (dom. público) · Roxyuru (CC BY-SA 3.0) · Diego Delso (CC BY-SA 3.0) · bullit (CC BY 3.0) · Zeroth (CC BY-SA 4.0) · Mx. Granger (CC0) · Fernando da Rosa (CC BY-SA 3.0) · Ricardo André Frantz (CC BY-SA 3.0) · Cristine Denardi Huff (CC BY-SA 4.0) · Rosanetur (CC BY 2.0) · Fernando Schultz Aldado (dom. público)",
  },
};

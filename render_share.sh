#!/usr/bin/env bash
# Uso: render_share.sh <pasta_projeto> <nome_saida>   -> renders/<nome>-60fps.mp4 (master) + <nome>.mp4 (compartilhar, -14 LUFS) copiado para ~/projetos/output/expedicaosul
set -euo pipefail
P="$1"; N="$2"; OUT=~/projetos/output/expedicaosul; mkdir -p "$OUT"
cd "$P"
npx hyperframes render -o "renders/$N-60fps.mp4" --quality delivery --fps 60 --skill general-video 2>&1 | grep -E "rendered in|Error|error" || true
test -s "renders/$N-60fps.mp4"
ffmpeg -loglevel error -y -i "renders/$N-60fps.mp4" -c:v libx264 -preset slow -crf 21 -maxrate 8M -bufsize 16M -pix_fmt yuv420p -movflags +faststart \
  -af "loudnorm=I=-14:TP=-1.0:LRA=11,volume=-1.5dB" -ar 48000 -c:a aac -b:a 192k "renders/$N.mp4"
ffprobe -v error -show_entries stream=codec_type,width,height,r_frame_rate:format=duration,size -of compact "renders/$N.mp4"
ffmpeg -hide_banner -i "renders/$N.mp4" -vn -af loudnorm=print_format=summary -f null - 2>&1 | grep -E "Input Integrated|Input True Peak"
cp "renders/$N.mp4" "$OUT/"
echo "OK $OUT/$N.mp4"

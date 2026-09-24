#!/usr/bin/env bash
# Uso: tg_encode.sh <entrada.mp4> <saida.mp4>  -> versão ≤ ~44 MB para o Telegram (30 fps, 2 passadas, bitrate pela duração)
set -euo pipefail
IN="$(realpath "$1")"; OUT="$(realpath -m "$2")"; TMP=$(mktemp -d)
DUR=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$IN")
VB=$(python3 -c "d=$DUR; print(int((44*8*1024)/d - 160))")
cd "$TMP"
ffmpeg -loglevel error -y -i "$IN" -r 30 -c:v libx264 -preset slow -b:v ${VB}k -pass 1 -an -f mp4 /dev/null
ffmpeg -loglevel error -y -i "$IN" -r 30 -c:v libx264 -preset slow -b:v ${VB}k -pass 2 -pix_fmt yuv420p -movflags +faststart -c:a aac -b:a 160k "$OUT"
rm -rf "$TMP"
echo "$(basename "$OUT") $(du -m "$OUT" | cut -f1)MB video ${VB}k"

#!/bin/bash
# startup.sh - Tu dong chay khi sinh vien khoi dong container

echo "=================================================================="
echo "    CHAO MUNG DEN VOI BAI THUC HANH: SCENE DIFFERENCE STEGANALYSIS"
echo "=================================================================="
echo ""
echo "[*] Dang tu dong sinh cac ca kiem thu video (video_clean.mp4, video_stego.mp4)..."
python3 generate_test_cases.py

echo ""
echo "[+] Moi truong thuc hanh da san sang!"
echo "    Hay doc file instructions.txt de biet chi tiet cac nhiem vu:"
echo "    cat instructions.txt"
echo "=================================================================="

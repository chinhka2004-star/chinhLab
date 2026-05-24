#!/bin/bash
# checkwork.sh - Script tu dong cham diem tai cho cho sinh vien (100 diem)

SCORE_CLEAN=0
SCORE_STEGO=0
SCORE_FORMAT=0

echo "=================================================================="
echo "          BAT DAU QUA TRINH GIAM DINH & CHAM DIEM TU DONG"
echo "=================================================================="
echo ""

# 1. Kiem tra xem ma nguon detect.py co ton tai khong
if [ ! -f "detect.py" ]; then
    echo "[!] LOI: Khong tim thay file detect.py cua sinh vien!"
    exit 1
fi

# 2. Chay thu nghiem Ca kiem thu 1: Video sach (video_clean.mp4)
echo "[*] Kiem thu 1: Chay detect.py tren video_clean.mp4..."
rm -f report_clean.txt
python3 detect.py -i video_clean.mp4 -o report_clean.txt -t 10.0 > /dev/null 2>&1

if [ -f "report_clean.txt" ]; then
    # Kiem tra ket qua phan loai co phai la CLEAN khong
    if grep -q "RESULT: CLEAN" report_clean.txt; then
        echo "[+] DAT: Phat hien chinh xac Video sach la CLEAN. (+40 diem)"
        SCORE_CLEAN=40
    else
        echo "[-] KHONG DAT: Bao dong gia! Video sach bi phan loai sai."
    fi
else
    echo "[-] KHONG DAT: Chuong trinh bi loi hoac khong sinh file bao cao report_clean.txt."
fi

echo ""

# 3. Chay thu nghiem Ca kiem thu 2: Video stego (video_stego.mp4)
echo "[*] Kiem thu 2: Chay detect.py tren video_stego.mp4..."
rm -f report_stego.txt
python3 detect.py -i video_stego.mp4 -o report_stego.txt -t 10.0 > /dev/null 2>&1

if [ -f "report_stego.txt" ]; then
    # Kiem tra ket qua phan loai co phai la STEGO khong
    if grep -q "RESULT: STEGO" report_stego.txt; then
        # Kiem tra xem co dinh vi dung frame 30 va 60 khong
        if grep -q "SUSPICIOUS_FRAMES:.*30" report_stego.txt && grep -q "SUSPICIOUS_FRAMES:.*60" report_stego.txt; then
            echo "[+] DAT: Phat hien chinh xac va dinh vi dung frame 30, 60. (+40 diem)"
            SCORE_STEGO=40
        else
            echo "[-] KHONG DAT: Phat hien duoc STEGO nhung dinh vi sai vi tri frame bi nhung!"
        fi
    else
        echo "[-] KHONG DAT: Bo sot tin an! Video stego bi phan loai la CLEAN."
    fi
else
    echo "[-] KHONG DAT: Chuong trinh bi loi hoac khong sinh file bao cao report_stego.txt."
fi

echo ""

# 4. Kiem tra dinh dang file bao cao report.txt dung chuan yeu cau
echo "[*] Kiem thu 3: Kiem tra dinh dang file bao cao report.txt..."
# Sinh report.txt tu video_stego.mp4
rm -f report.txt
python3 detect.py -i video_stego.mp4 -o report.txt -t 10.0 > /dev/null 2>&1

if [ -f "report.txt" ]; then
    HAS_VIDEO=$(grep -q "VIDEO: " report.txt; echo $?)
    HAS_RESULT=$(grep -q "RESULT: " report.txt; echo $?)
    HAS_FRAMES=$(grep -q "SUSPICIOUS_FRAMES: " report.txt; echo $?)
    
    if [ $HAS_VIDEO -eq 0 ] && [ $HAS_RESULT -eq 0 ] && [ $HAS_FRAMES -eq 0 ]; then
        echo "[+] DAT: Dinh dang file report.txt chinh xac theo mau. (+20 diem)"
        SCORE_FORMAT=20
    else
        echo "[-] KHONG DAT: File report.txt thieu cac truong thong tin bat buoc (VIDEO, RESULT, SUSPICIOUS_FRAMES)."
    fi
else
    echo "[-] KHONG DAT: Khong tim thay file bao cao report.txt cho kieu cham diem."
fi

echo ""

# 5. Tong hop va xuat diem cho he thong Labtainer
SCORE_TOTAL=$((SCORE_CLEAN + SCORE_STEGO + SCORE_FORMAT))

mkdir -p /home/ubuntu/.local/result
echo "CLEAN_SCORE=$SCORE_CLEAN" > /home/ubuntu/.local/result/detect.grade
echo "STEGO_SCORE=$SCORE_STEGO" >> /home/ubuntu/.local/result/detect.grade
echo "FORMAT_SCORE=$SCORE_FORMAT" >> /home/ubuntu/.local/result/detect.grade
echo "TOTAL_SCORE=$SCORE_TOTAL" >> /home/ubuntu/.local/result/detect.grade

echo "=================================================================="
echo "                 KET QUA DANH GIA (GRADES SUMMARY)"
echo "=================================================================="
echo "  1. Nhan dien Video sach (CLEAN):       $SCORE_CLEAN / 40"
echo "  2. Nhan dien Video giu tin (STEGO):    $SCORE_STEGO / 40"
echo "  3. Dinh dang bao cao (report.txt):     $SCORE_FORMAT / 20"
echo "------------------------------------------------------------------"
echo "  TONG SO DIEM DAT DUOC:                 $SCORE_TOTAL / 100"
echo "=================================================================="
echo "[*] Tang chung cham diem da duoc ghi nhan va truyen ve may Host!"

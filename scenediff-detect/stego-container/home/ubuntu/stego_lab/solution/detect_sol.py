import os
import sys
import math
import shutil
import argparse
import subprocess
from PIL import Image

def calculate_frame_difference(img1_path, img2_path):
    img1 = Image.open(img1_path).convert('L')
    img2 = Image.open(img2_path).convert('L')
    
    pixels1 = img1.load()
    pixels2 = img2.load()
    
    width, height = img1.size
    total_diff = 0
    
    for y in range(height):
        for x in range(width):
            total_diff += abs(pixels1[x, y] - pixels2[x, y])
            
    return total_diff / (width * height)

def detect_scene_changes(frames_dir, num_frames, threshold):
    scene_changes = []
    
    for i in range(1, num_frames):
        img1 = os.path.join(frames_dir, f"frame_{i-1:04d}.png")
        img2 = os.path.join(frames_dir, f"frame_{i:04d}.png")
        
        diff = calculate_frame_difference(img1, img2)
        if diff > threshold:
            scene_changes.append(i)
            
    return scene_changes

def calculate_shannon_entropy(bits):
    if not bits:
        return 0.0
    
    count0 = bits.count(0)
    count1 = bits.count(1)
    total = len(bits)
    
    p0 = count0 / total
    p1 = count1 / total
    
    entropy = 0.0
    if p0 > 0:
        entropy -= p0 * math.log2(p0)
    if p1 > 0:
        entropy -= p1 * math.log2(p1)
        
    return entropy

def analyze_lsb_entropy(frame_path, max_pixels=2000):
    img = Image.open(frame_path)
    pixels = img.load()
    width, height = img.size
    
    bits = []
    pixel_count = 0
    
    for y in range(height):
        for x in range(width):
            if pixel_count >= max_pixels:
                break
            r, g, b = pixels[x, y]
            bits.append(r & 1)
            bits.append(g & 1)
            bits.append(b & 1)
            pixel_count += 1
            
    return calculate_shannon_entropy(bits)

def main():
    parser = argparse.ArgumentParser(description="Scene Difference Steganalysis Tool")
    parser.add_argument('-i', '--input', required=True, help="Input MP4 video file")
    parser.add_argument('-o', '--output', default="report.txt", help="Output report file path")
    parser.add_argument('-t', '--threshold', type=float, default=10.0, help="Grayscale difference threshold")
    args = parser.parse_args()
    
    temp_dir = 'temp_unpack'
    os.makedirs(temp_dir, exist_ok=True)
    
    # 1. Giải nén video thành các frame hình ảnh PNG
    print(f"[*] Đang giải nén video {args.input}...")
    subprocess.run([
        'ffmpeg', '-y', '-i', args.input,
        os.path.join(temp_dir, 'frame_%04d.png')
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    # 2. Đếm số lượng frame giải nén
    frames = sorted([f for f in os.listdir(temp_dir) if f.endswith('.png')])
    num_frames = len(frames)
    
    if num_frames == 0:
        print("[!] Không thể giải nén khung hình nào từ video.")
        shutil.rmtree(temp_dir)
        sys.exit(1)
        
    print(f"[+] Giải nén thành công {num_frames} khung hình.")
    
    # Đổi tên frame để khớp với quy chuẩn index 0-based
    for idx, f_name in enumerate(frames):
        src = os.path.join(temp_dir, f_name)
        dst = os.path.join(temp_dir, f"frame_{idx:04d}.png")
        if src != dst:
            os.rename(src, dst)
            
    # 3. Phát hiện chuyển cảnh
    print("[*] Đang phân tích chuyển cảnh...")
    scene_changes = detect_scene_changes(temp_dir, num_frames, args.threshold)
    print(f"[+] Phát hiện {len(scene_changes)} khung hình chuyển cảnh tại indices: {scene_changes}")
    
    # 4. Phân tích thống kê Entropy của LSB trên các khung hình chuyển cảnh
    suspicious_frames = []
    print("[*] Đang phân tích Shannon Entropy của LSB trên các khung hình chuyển cảnh...")
    
    for frame_idx in scene_changes:
        frame_path = os.path.join(temp_dir, f"frame_{frame_idx:04d}.png")
        entropy = analyze_lsb_entropy(frame_path)
        print(f"    - Frame {frame_idx:03d} | LSB Shannon Entropy: {entropy:.6f}")
        
        # Nếu entropy vượt ngưỡng 0.98, ta kết luận có dữ liệu nhúng ngẫu nhiên (Stego)
        if entropy > 0.98:
            suspicious_frames.append(frame_idx)
            
    # 5. Phân loại video & Xuất báo cáo
    is_stego = len(suspicious_frames) > 0
    result_str = "STEGO" if is_stego else "CLEAN"
    
    print(f"[+] KẾT QUẢ PHÂN TÍCH: Video này là {result_str}")
    
    with open(args.output, 'w', encoding='utf-8') as f:
        f.write(f"VIDEO: {os.path.basename(args.input)}\n")
        f.write(f"RESULT: {result_str}\n")
        if is_stego:
            f.write(f"SUSPICIOUS_FRAMES: {','.join(map(str, suspicious_frames))}\n")
        else:
            f.write("SUSPICIOUS_FRAMES: NONE\n")
            
    # Dọn dẹp
    shutil.rmtree(temp_dir)
    print(f"[+] Báo cáo kết quả giám định đã được lưu tại {args.output}")

if __name__ == '__main__':
    main()

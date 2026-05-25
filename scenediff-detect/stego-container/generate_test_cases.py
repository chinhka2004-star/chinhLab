import os
import math
import random
import subprocess
from PIL import Image, ImageDraw

def generate_base_frames(width, height, num_frames):
    frames_dir = 'temp_raw_frames'
    os.makedirs(frames_dir, exist_ok=True)
    
    for i in range(num_frames):
        # Thiết lập các scene change đột ngột
        if 0 <= i < 30:
            bg_color = (0, 0, 240)      # Cảnh 1: Xanh dương
        elif 30 <= i < 60:
            bg_color = (240, 0, 0)      # Cảnh 2: Đỏ (Scene change tại frame 30)
        elif 60 <= i < 90:
            bg_color = (0, 240, 0)      # Cảnh 3: Xanh lá (Scene change tại frame 60)
        else:
            bg_color = (240, 240, 0)    # Cảnh 4: Vàng (Scene change tại frame 90)
            
        img = Image.new('RGB', (width, height), bg_color)
        draw = ImageDraw.Draw(img)
        
        # Vật thể chuyển động tuần hoàn mượt mà
        cx = int(width / 2 + 80 * math.cos(2 * math.pi * i / 60))
        cy = int(height / 2 + 60 * math.sin(2 * math.pi * i / 60))
        draw.ellipse([cx - 15, cy - 15, cx + 15, cy + 15], fill=(255, 255, 255))
        
        img.save(os.path.join(frames_dir, f"frame_{i:04d}.png"))
    return frames_dir

def embed_random_stego(frame_path, message):
    # Nhúng chuỗi ngẫu nhiên (Entropy cực cao) vào LSB của frame
    msg_bytes = (message + '\0').encode('utf-8')
    bits = []
    for byte in msg_bytes:
        for i in range(8):
            bits.append((byte >> (7 - i)) & 1)
            
    num_bits = len(bits)
    bit_idx = 0
    
    img = Image.open(frame_path)
    pixels = img.load()
    width, height = img.size
    
    for y in range(height):
        for x in range(width):
            if bit_idx >= num_bits:
                break
            r, g, b = pixels[x, y]
            
            if bit_idx < num_bits:
                r = (r & ~1) | bits[bit_idx]
                bit_idx += 1
            if bit_idx < num_bits:
                g = (g & ~1) | bits[bit_idx]
                bit_idx += 1
            if bit_idx < num_bits:
                b = (b & ~1) | bits[bit_idx]
                bit_idx += 1
                
            pixels[x, y] = (r, g, b)
            
    img.save(frame_path)

def build_video_from_frames(frames_dir, output_path):
    subprocess.run([
        'ffmpeg', '-y',
        '-framerate', '30',
        '-i', os.path.join(frames_dir, 'frame_%04d.png'),
        '-c:v', 'libx264rgb', '-crf', '0',
        output_path
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def generate():
    width, height = 320, 240
    num_frames = 120
    
    print("[*] Đang khởi tạo các khung hình cơ sở cho 2 Ca kiểm thử...")
    raw_dir = generate_base_frames(width, height, num_frames)
    
    # 1. Tạo video sạch (video_clean.mp4)
    print("[*] Đang đóng gói Video sạch: video_clean.mp4...")
    build_video_from_frames(raw_dir, 'video_clean.mp4')
    
    # 2. Tạo video stego (video_stego.mp4) - Nhúng dữ liệu ngẫu nhiên entropy cao vào LSB của scene changes
    print("[*] Đang nhúng dữ liệu ngẫu nhiên mật mã vào chuyển cảnh (frame 30 và 60)...")
    # Sinh dữ liệu ngẫu nhiên độ dài lớn để phủ kín LSB của pixel
    random.seed(42)
    random_msg = "".join(chr(random.randint(33, 126)) for _ in range(3000))
    
    # Nhúng vào frame 30 và 60 (là 2 frame chuyển cảnh chính)
    embed_random_stego(os.path.join(raw_dir, 'frame_0030.png'), random_msg)
    embed_random_stego(os.path.join(raw_dir, 'frame_0060.png'), random_msg)
    
    print("[*] Đang đóng gói Video Stego: video_stego.mp4...")
    build_video_from_frames(raw_dir, 'video_stego.mp4')
    
    # Dọn dẹp
    for f in os.listdir(raw_dir):
        os.remove(os.path.join(raw_dir, f))
    os.rmdir(raw_dir)
    print("[+] Hoàn thành sinh dữ liệu video_clean.mp4 và video_stego.mp4 thành công!")

if __name__ == '__main__':
    generate()

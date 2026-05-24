import os
import sys
import math
import shutil
import argparse
import subprocess
from PIL import Image

def calculate_frame_difference(img1_path, img2_path):
    """
    TÁC VỤ 2.1: Tính toán sai lệch tuyệt đối trung bình thang xám giữa 2 khung hình
    Yêu cầu:
    - Mở 2 hình ảnh bằng Pillow, chuyển sang hệ màu Grayscale ('L').
    - Tính tổng hiệu tuyệt đối giữa các pixel cùng vị trí của 2 hình ảnh.
    - Trả về giá trị hiệu trung bình (tổng hiệu / tổng số pixel).
    """
    # TODO: Sinh viên hoàn thành code tại đây
    pass

def detect_scene_changes(frames_dir, num_frames, threshold):
    """
    TÁC VỤ 2.2: Phát hiện chuyển cảnh
    Yêu cầu:
    - Duyệt qua toàn bộ danh sách khung hình từ 1 đến num_frames - 1.
    - So sánh frame(i) và frame(i-1) bằng hàm calculate_frame_difference.
    - Nếu độ sai lệch > threshold, thêm index i vào danh sách chuyển cảnh.
    - Trả về danh sách indices chuyển cảnh.
    """
    # TODO: Sinh viên hoàn thành code tại đây
    pass

def calculate_shannon_entropy(bits):
    """
    TÁC VỤ 2.3: Tính toán Entropy Shannon của chuỗi bit
    Yêu cầu:
    - Đếm số lượng bit 0 và bit 1 trong mảng `bits`.
    - Tính toán xác suất p0 (tỷ lệ bit 0) và p1 (tỷ lệ bit 1).
    - Áp dụng công thức: H = - (p0 * log2(p0) + p1 * log2(p1)).
    - Lưu ý xử lý trường hợp xác suất bằng 0 để tránh lỗi toán học.
    - Trả về giá trị Entropy.
    """
    # TODO: Sinh viên hoàn thành code tại đây
    pass

def analyze_lsb_entropy(frame_path, max_pixels=2000):
    """
    TÁC VỤ 2.4: Trích xuất LSB và tính Entropy của khung hình
    Yêu cầu:
    - Mở hình ảnh bằng Pillow, truy cập dữ liệu pixel.
    - Duyệt qua tối đa `max_pixels` pixel đầu tiên của khung hình.
    - Với mỗi pixel, trích xuất bit LSB (bit cuối) của 3 kênh màu R, G, B.
    - Lưu tất cả các bit LSB này vào một mảng phẳng.
    - Gọi hàm calculate_shannon_entropy để tính toán Entropy của mảng bit này.
    - Trả về giá trị Entropy tính được.
    """
    # TODO: Sinh viên hoàn thành code tại đây
    pass

def main():
    parser = argparse.ArgumentParser(description="Scene Difference Steganalysis Tool")
    parser.add_argument('-i', '--input', required=True, help="Input MP4 video file")
    parser.add_argument('-o', '--output', default="report.txt", help="Output report file path")
    parser.add_argument('-t', '--threshold', type=float, default=10.0, help="Grayscale difference threshold")
    args = parser.parse_args()
    
    temp_dir = 'temp_unpack'
    os.makedirs(temp_dir, exist_ok=True)
    
    # 1. Giải nén video thành các frame hình ảnh PNG sử dụng FFmpeg
    print(f"[*] Đang giải nén video {args.input}...")
    subprocess.run([
        'ffmpeg', '-y', '-i', args.input,
        os.path.join(temp_dir, 'frame_%04d.png')
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    # Đếm số lượng frame giải nén
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
            
    # 2. Phát hiện chuyển cảnh
    print("[*] Đang phân tích chuyển cảnh...")
    scene_changes = detect_scene_changes(temp_dir, num_frames, args.threshold)
    
    if scene_changes is None:
        scene_changes = []
        
    print(f"[+] Phát hiện {len(scene_changes)} khung hình chuyển cảnh tại indices: {scene_changes}")
    
    # 3. Phân tích thống kê Entropy của LSB trên các khung hình chuyển cảnh
    suspicious_frames = []
    print("[*] Đang phân tích Shannon Entropy của LSB trên các khung hình chuyển cảnh...")
    
    for frame_idx in scene_changes:
        frame_path = os.path.join(temp_dir, f"frame_{frame_idx:04d}.png")
        entropy = analyze_lsb_entropy(frame_path)
        
        if entropy is None:
            entropy = 0.0
            
        print(f"    - Frame {frame_idx:03d} | LSB Shannon Entropy: {entropy:.6f}")
        
        # Nếu entropy vượt ngưỡng 0.98, ta kết luận có dữ liệu nhúng ngẫu nhiên (Stego)
        if entropy > 0.98:
            suspicious_frames.append(frame_idx)
            
    # 4. Phân loại video & Xuất báo cáo
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

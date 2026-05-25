# chinhLab: HỆ THỐNG PHÒNG THỰC HÀNH AN NINH MẠNG VÀ PHÁT HIỆN GIẤU TIN

Chào mừng thầy/cô và các bạn sinh viên đến với **chinhLab**! Đây là kho lưu trữ chứa bài thực hành an ninh mạng nâng cao được đóng gói chuẩn hóa dưới dạng **Labtainers IModule** để chạy trên hệ điều hành ảo hóa Debian/Ubuntu.

## 🔬 Chủ đề: Phát hiện giấu tin trong Video dựa trên sự khác biệt khung cảnh (Scene Difference Steganalysis)

Bài thực hành **`scenediff-detect`** được thiết kế nhằm giúp sinh viên hiểu rõ góc độ **phòng thủ an ninh mạng (Steganalysis)**: Làm thế nào để phân tích dữ liệu đa phương tiện, phát hiện mã độc ẩn hoặc dữ liệu giấu bất hợp pháp (steganography) bằng phương pháp vi sai chuyển cảnh và thống kê lý thuyết thông tin **Shannon Entropy**.

---

## 📂 1. Cấu trúc bài Lab `scenediff-detect`

```text
/
├── imodule.tar                                      # Gói cài đặt Labtainers đóng gói sẵn
├── Tai_lieu_huong_dan_Scene_Difference_Steganalysis.md # Tài liệu hướng dẫn đầy đủ (bản in ấn)
├── README.md                                        # Tài liệu trang chủ hướng dẫn nhanh
└── scenediff-detect/                                # Thư mục cấu hình cốt lõi bài Lab
    ├── config/
    │   ├── start.config                             # Cấu hình container stego-container
    │   └── lab.conf                                 # Phiên bản và mô tả bài lab
    ├── dockerfiles/
    │   └── Dockerfile.scenediff-detect.stego-container.student # Định nghĩa Dockerfile học viên
    ├── instr_config/
    │   ├── results.config                           # Khai báo biến trích xuất điểm số
    │   └── goals.config                             # Quy chuẩn mục tiêu đánh giá tự động
    └── stego-container/
        ├── detect.py                            # Khung mã nguồn sinh viên cần hoàn thiện (TODO)
        ├── generate_test_cases.py               # Tự động sinh video sạch và video stego
        ├── startup.sh                           # Tập lệnh tự chạy khi kích hoạt lab
        ├── instructions.txt                     # Hướng dẫn nhiệm vụ trong container
        ├── checkwork.sh                         # Kịch bản tự chấm điểm tại chỗ (100 điểm)
        └── solution/
            └── detect_sol.py                    # Giải pháp mẫu hoàn chỉnh của giảng viên
```

---

## 🛠️ 2. Quy trình Cài đặt & Khởi chạy dành cho Sinh viên

Sinh viên chỉ cần thực hiện 4 bước lệnh đơn giản trực tiếp trên máy ảo Labtainers để bắt đầu:

### Bước 1: Nạp bài Lab từ chinhLab về hệ thống cục bộ
```bash
imodule https://github.com/chinhka2004-star/chinhLab/raw/main/imodule.tar
```

### Bước 2: Di chuyển vào không gian làm việc sinh viên
```bash
cd ~/labtainer/labtainer-student
```

### Bước 3: Biên dịch Docker Image cục bộ cho phòng Lab (Bắt buộc)
```bash
rebuild scenediff-detect
```

### Bước 4: Kích hoạt Container ảo Ubuntu và làm bài
```bash
labtainer scenediff-detect
```

---

## 🧪 3. Cơ chế Phân tích & Phát hiện ẩn tin (Steganalysis Logic)

Trong truyền thông đa phương tiện, dòng bit LSB của các điểm ảnh có xu hướng mang quy luật tự nhiên (độ hỗn loạn thấp, **Shannon Entropy $< 0.95$**). Khi kẻ tấn công nhúng thông tin ẩn (stego) - vốn thường được mã hóa hoặc nén để đảm bảo tính bí mật - các bit LSB này sẽ trở nên phân bố cực kỳ ngẫu nhiên và hỗn loạn, dẫn đến **Shannon Entropy tiệm cận $1.0$ ($> 0.98$)**.

Công cụ `detect.py` của sinh viên sẽ:
1. Phát hiện các khung hình chuyển cảnh có sự biến động lớn về màu sắc trung bình thang xám.
2. Trích xuất bit LSB của các kênh màu R, G, B từ các khung hình này.
3. Tính toán Entropy Shannon:
   $$H(X) = - \sum_{i} P(x_i) \log_2 P(x_i)$$
4. Đưa ra chẩn đoán: Nếu Entropy của khung hình $> 0.98$, ghi nhận khung hình đó bị xâm hại (`STEGO`).

---

## 📈 4. Hệ thống Chấm điểm tự động (Grading Matrix)

Khi sinh viên chạy `./checkwork.sh` bên trong container hoặc hệ thống máy host chấm điểm bằng `checkwork scenediff-detect`, thang điểm 100 được tính như sau:

| STT | Tiêu chí đánh giá | Điểm số | Điều kiện đạt |
| :-: | :--- | :-: | :--- |
| **1** | Nhận diện chính xác Video Sạch | **40 điểm** | Không báo động giả trên `video_clean.mp4` |
| **2** | Nhận diện & Định vị Video Stego | **40 điểm** | Phát hiện `video_stego.mp4` và chỉ ra chính xác frame 30, 60 |
| **3** | Đúng định dạng báo cáo | **20 điểm** | File `report.txt` chứa đủ các trường bắt buộc |

---

## 🛡️ Bản quyền & Thiết kế
- **Giảng viên thiết kế:** Kỹ sư An toàn thông tin & Giảng viên An ninh mạng.
- **Môi trường vận hành:** Tự động hóa hoàn toàn thông qua **Labtainer Framework**.
- **GitHub Repository:** [chinhka2004-star/chinhLab](https://github.com/chinhka2004-star/chinhLab)

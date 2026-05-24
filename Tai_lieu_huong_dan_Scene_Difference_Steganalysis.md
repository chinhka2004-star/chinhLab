BÀI THỰC HÀNH: PHÁT HIỆN GIẤU TIN TRONG VIDEO DỰA TRÊN SỰ KHÁC BIỆT KHUNG CẢNH
Mục tiêu bài thực hành
Trong bài lab này, sinh viên sẽ đóng vai trò là một chuyên gia phân tích an toàn thông tin (Blue Team), tìm hiểu và thực hành kỹ thuật phát hiện giấu tin (Steganalysis) trong video dựa trên thuật toán phát hiện chuyển cảnh kết hợp với phép phân tích thống kê toán học Shannon Entropy trên dòng bit LSB (Least Significant Bit).
Bài lab tập trung hoàn toàn vào việc thực thi tự động hóa hệ thống kịch bản, theo dõi và giám sát sự biến đổi dữ liệu, kiểm tra tính toàn vẹn của báo cáo kết quả thông qua hệ thống chấm điểm tự động của Labtainer framework.
Kỹ năng đạt được
- Hiểu sâu sắc kỹ thuật phân tích và giám định đa phương tiện (Media Forensics).
- Nắm vững công thức Shannon Entropy và ứng dụng của nó trong việc phân tích mật độ phân bổ thông tin ngẫu nhiên trên các bit LSB của kênh màu RGB.
- Kỹ năng thiết lập ngưỡng chẩn đoán để phân biệt và định vị bất thường giữa khung hình chứa tin ẩn (stego) và khung hình tự nhiên (clean).
- Kỹ năng kiểm thử tự động bài lab thông qua hệ thống kết xuất tang chứng vật lý tự động của Labtainers.
Yêu cầu đối với sinh viên
- Có kiến thức nền tảng về xác suất thống kê và lý thuyết thông tin (Information Theory).
- Có khả năng lập trình Python cơ bản và thao tác với ảnh số qua thư viện Pillow (PIL).
- Có khả năng sử dụng các lệnh điều khiển Linux nâng cao, quản lý gói phần mềm hệ thống hệ điều hành Debian/Ubuntu.
Kiến thức bổ trợ
Lý thuyết Shannon Entropy đo lường mức độ bất định hoặc độ hỗn loạn của một nguồn thông tin. Đối với dòng bit LSB có độ dài $N$:
- Nếu dòng bit chứa thông điệp ngẫu nhiên (hoặc đã nén/mã hóa), tỷ lệ bit 0 và bit 1 sẽ cân bằng ($\approx 50\%$), dẫn tới Entropy tiệm cận $1.0$.
- Nếu dòng bit tự nhiên, nó sẽ chứa nhiều quy luật và nhiễu đều (Entropy thấp, thường $< 0.95$).
Thông tin lab
Thông tin
Chi tiết
Tên lab
scenediff-detect
Container
ubuntu
Công cụ chính
python3, pip, pillow, ffmpeg, ffprobe
Phương pháp
Phát hiện chuyển cảnh vi sai + Phân tích Shannon Entropy LSB RGB
Dữ liệu đầu vào
Video sạch (video_clean.mp4), Video chứa tin ẩn (video_stego.mp4)

Vấn đề kỹ thuật
1. Thuật toán phân tích chuyển cảnh (Scene Change Detection)
Hệ thống sử dụng phép so khớp sự sai khác trung bình của ma trận ảnh thang xám giữa hai khung hình kề nhau để khoanh vùng các khung hình chuyển cảnh có khả năng cao bị lợi dụng để nhúng tin ẩn.
2. Thuật toán phân tích thống kê LSB Entropy
Trích xuất dòng bit LSB từ các kênh màu RGB của khung hình chuyển cảnh. Sử dụng công thức toán học Shannon Entropy để đo độ hỗn loạn của dòng bit này. Khi độ hỗn loạn vượt ngưỡng $0.98$, hệ thống chẩn đoán khung hình đó có chứa mã ẩn (stego).
Khởi động Lab
Chuẩn bị môi trường hệ thống:
1. Sử dụng lệnh imodule để nạp cấu hình bài thực hành từ kho lưu trữ về hệ thống cục bộ:
imodule https://github.com/chinhka2004-star/chinhLab/raw/main/imodule.tar
2. Di chuyển vào không gian làm việc của sinh viên trong framework Labtainer:
cd ~/labtainer/labtainer-student
3. Biên dịch và xây dựng Docker Image cục bộ cho phòng Lab (Bắt buộc đối với bài Lab tùy chỉnh):
rebuild scenediff-detect
4. Khởi chạy bài lab để kích hoạt container ảo Ubuntu:
labtainer scenediff-detect
Nhiệm vụ
Task 1: Khởi động môi trường và kiểm tra các file thành phần
Bước 1: Sau khi hệ thống kích hoạt container thành công, màn hình xuất hiện dấu nhắc lệnh ubuntu@ubuntu:~$
Bước 2: Sử dụng lệnh liệt kê thư mục để xác minh các file kịch bản lập trình có sẵn:
ls -l
Yêu cầu bắt buộc: Sinh viên kiểm tra thấy sự hiện diện đầy đủ của các file: detect.py, generate_test_cases.py, startup.sh và instructions.txt.
Task 2: Cấu hình môi trường và cài đặt các thư viện ảnh chuyên dụng
Bước 1: Tiến hành cập nhật danh sách các kho lưu trữ phần mềm hệ thống:
sudo apt-get update
Bước 2: Cài đặt thư viện xử lý ảnh Pillow cho Python 3:
sudo apt-get install python3-pillow -y
Bước 3: Cài đặt công cụ ffmpeg để giải nén video:
sudo apt-get install ffmpeg -y
Task 3: Thực thi sinh ca kiểm thử tự động
Bước 1: Hệ thống khi khởi động container đã tự động kích hoạt sinh tệp tin kiểm thử. Sinh viên có thể chạy lại thủ công bằng lệnh:
python3 generate_test_cases.py
Bước 2: Kiểm tra sự tồn tại vật lý của file video sạch và video chứa tin ẩn bằng lệnh:
ls -l video_clean.mp4 video_stego.mp4
Task 4: Phân tích và phát hiện trên Video sạch
Bước 1: Thực thi công cụ detect.py trên video sạch để xác nhận tính chính xác (không báo động giả):
python3 detect.py -i video_clean.mp4 -o report_clean.txt -t 10.0
Bước 2: Đọc báo cáo kết quả và xác nhận kết quả là CLEAN:
cat report_clean.txt
Task 5: Phân tích, phát hiện và định vị khung hình Stego trên Video chứa tin ẩn
Bước 1: Thực thi công cụ detect.py trên video stego để phát hiện và định vị khung hình bị xâm hại:
python3 detect.py -i video_stego.mp4 -o report.txt -t 10.0
Bước 2: Đọc báo cáo và xác nhận kết quả là STEGO, đồng thời chỉ ra đúng các khung hình bị nhúng stego (Indices: 30, 60):
cat report.txt
Kết Thúc Bài Lab
Trước khi kết thúc, sinh viên thực hiện kiểm thử tiến độ chấm điểm tự động bằng cách chạy script tại chỗ:
./checkwork.sh
Quay lại Terminal Host và thực thi lệnh giám định của Labtainer:
checkwork scenediff-detect
1. Tại Terminal máy ảo Ubuntu, nhập lệnh thoát:
exit
2. Tại Terminal hệ thống máy Host, gõ lệnh chấm dứt phiên làm việc:
stoplab
Để thực hiện lại bài thực hành từ đầu (Reset toàn bộ cấu hình), sử dụng lệnh cấu hình hệ thống:
labtainer -r scenediff-detect

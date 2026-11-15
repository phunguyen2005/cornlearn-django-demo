# SkyLearn — Đề tài tìm hiểu Django Framework

> Đây là project phục vụ **đề tài tìm hiểu và demo học tập**, không phải sản phẩm thương mại hoặc hệ thống production. Project minh họa cách xây dựng một hệ thống quản lý học tập bằng Django theo mô hình server-rendered.

## Thông tin ứng dụng

| Thông tin | Nội dung |
| --- | --- |
| Tên ứng dụng | SkyLearn |
| Loại ứng dụng | Learning Management System (LMS) |
| Mục đích | Tìm hiểu Django Framework và demo nghiệp vụ quản lý học tập |
| Backend | Python, Django 4.0.8 |
| Giao diện | Django Templates, Bootstrap 5, HTML/CSS/JavaScript |
| Cơ sở dữ liệu mặc định | SQLite |
| Xác thực | Django Session Authentication, CSRF và phân quyền theo vai trò |
| Ngôn ngữ | Python 3.8+ |
| Trạng thái | Bản demo học tập — đang tiếp tục hoàn thiện |

## Phạm vi demo

Ứng dụng mô phỏng các nghiệp vụ chính của một hệ thống quản lý học tập:

- Quản lý tài khoản, hồ sơ và vai trò người dùng.
- Quản lý sinh viên, giảng viên, phụ huynh và khoa/bộ môn.
- Quản lý chương trình đào tạo, học phần, học kỳ và niên khóa.
- Đăng ký, hủy đăng ký học phần và phân công giảng viên.
- Quản lý tài liệu, video và tài nguyên môn học.
- Nhập điểm thành phần, tính điểm tổng kết, GPA/CGPA và xếp loại.
- Xuất phiếu đăng ký và bảng điểm dạng PDF.
- Tạo quiz, làm bài, lưu tiến độ, chấm điểm và theo dõi kết quả.
- Tin tức, sự kiện, dashboard và tìm kiếm nội dung.
- Khu vực thanh toán ở mức prototype để phục vụ minh họa.

## Cấu trúc nghiệp vụ

| Django app | Vai trò chính |
| --- | --- |
| `accounts` | Người dùng, hồ sơ, xác thực và phân quyền |
| `core` | Tin tức, sự kiện, học kỳ, niên khóa và dashboard |
| `course` | Chương trình, học phần, phân công và đăng ký môn |
| `result` | Điểm, kết quả học tập và xuất PDF |
| `quiz` | Câu hỏi, bài làm, tiến độ và chấm điểm |
| `payments` | Hóa đơn và giao diện thanh toán thử nghiệm |
| `search` | Tìm kiếm tổng hợp nội dung |

## Công nghệ sử dụng

- Python 3.8+
- Django 4.0.8
- SQLite
- Django Templates và Django Forms
- Bootstrap 5, crispy-forms
- django-filter và django-modeltranslation
- ReportLab/xhtml2pdf cho tài liệu PDF
- WhiteNoise cho static files
- Stripe/GoPay ở trạng thái minh họa

## Cài đặt và chạy local

### 1. Tạo môi trường ảo

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 2. Cài dependencies

```powershell
pip install -r requirements.txt
```

### 3. Tạo file môi trường

```powershell
Copy-Item .env.example .env
```

Sau đó cập nhật `SECRET_KEY` và các biến email trong `.env`. Không commit file `.env` lên GitHub.

### 4. Khởi tạo database và tài khoản quản trị

```powershell
python manage.py migrate
python manage.py createsuperuser
```

### 5. Kiểm tra và chạy ứng dụng

```powershell
python manage.py check
python manage.py runserver
```

Mở trình duyệt tại <http://127.0.0.1:8000>.

## Lưu ý về repository

- Đây là bản demo dùng cho học tập, báo cáo và trình bày đề tài.
- Không sử dụng dữ liệu người dùng thật, secret key thật hoặc thông tin thanh toán thật.
- Database SQLite local, cache, file upload runtime và môi trường ảo không được đưa vào repository.
- Tài liệu phân tích trong thư mục `docs/` mô tả kiến trúc, nghiệp vụ, quyền hạn, contract backend, kiểm thử và giới hạn hiện tại.
- Logic nghiệp vụ hiện tại được bảo toàn để phục vụ việc đối chiếu và trình bày đề tài.

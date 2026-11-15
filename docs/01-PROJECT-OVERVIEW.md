# Tổng quan SkyLearn

> Baseline: [SkyCascade/SkyLearn](https://github.com/SkyCascade/SkyLearn), nhánh `main`, commit `d57f57bd505447b59fdf82b16469494443cafe0c`. Đây là bản kiểm kê mã nguồn, không phải đặc tả tính năng mới. Trạng thái tải source và kiểm thử: [11-SETUP-AND-DEPLOYMENT.md](11-SETUP-AND-DEPLOYMENT.md).

SkyLearn là LMS và hệ thống quản lý học vụ dạng Django server-rendered. Phạm vi có quản lý tài khoản, chương trình, học phần, phân công giảng viên, đăng ký/hủy môn, tài liệu/video, nhập điểm, báo cáo PDF, quiz, tin/sự kiện, tìm kiếm và các trang thanh toán thử nghiệm. [README](../README.md) có mô tả rộng hơn mã; khi bất đồng, `models.py`, `views.py`, `urls.py` là bằng chứng chính.

## Người dùng

Admin/superuser, giảng viên, sinh viên, phụ huynh và trưởng bộ môn được biểu diễn trong `accounts.User`; hai vai trò sau có model nhưng chức năng chuyên biệt ít hoặc chưa nối route. Xem [`accounts/models.py`](../accounts/models.py) và [ma trận quyền](05-ROLES-AND-PERMISSIONS.md).

## Công nghệ

Python (README yêu cầu 3.8+), Django 4.0.8, SQLite, Django Templates, forms/CSRF/session authentication, django-filter, crispy-forms + Bootstrap 5, django-modeltranslation, django-jet-reboot, ReportLab/xhtml2pdf, WhiteNoise; Stripe/GoPay ở trạng thái mẫu. Phiên bản từ [`requirements/base.txt`](../requirements/base.txt), [`requirements/local.txt`](../requirements/local.txt), [`config/settings.py`](../config/settings.py). Không có REST API/DRF trong `INSTALLED_APPS` hay `config/urls.py`.

## 7 ứng dụng nghiệp vụ

| App | Trách nhiệm | Mã nguồn |
| --- | --- | --- |
| accounts | User, Student, Parent, DepartmentHead; hồ sơ, tài khoản | [`accounts/models.py`](../accounts/models.py) |
| core | Tin/sự kiện, niên khóa, học kỳ, dashboard, log | [`core/views.py`](../core/views.py) |
| course | Chương trình, học phần, phân công, tài nguyên, add/drop | [`course/views.py`](../course/views.py) |
| result | Điểm thành phần, điểm chữ, GPA/CGPA, PDF | [`result/models.py`](../result/models.py) |
| quiz | Quiz, câu hỏi, lượt làm, tiến độ, marking | [`quiz/views.py`](../quiz/views.py) |
| payments | Invoice và giao diện/call thanh toán chưa hoàn chỉnh | [`payments/views.py`](../payments/views.py) |
| search | Tìm kiếm 4 loại nội dung | [`search/views.py`](../search/views.py) |

## Ranh giới

Không coi nội dung [TODO](../TODO.md) là nghiệp vụ hoàn thành: lịch trường, deadline add/drop, dashboard động và tích hợp thanh toán. Không suy diễn rằng điểm quiz tự đẩy vào điểm học phần; hai nơi lưu riêng ([`quiz/models.py`](../quiz/models.py), [`result/models.py`](../result/models.py)).


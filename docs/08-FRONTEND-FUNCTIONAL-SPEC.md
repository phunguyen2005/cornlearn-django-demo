# Đặc tả chức năng frontend (không có thiết kế trực quan)

> Baseline SkyLearn `main@d57f57bd505447b59fdf82b16469494443cafe0c`. Các ID nối với [03](03-BUSINESS-REQUIREMENTS.md), [06](06-BACKEND-CONTRACTS.md) và [09](09-TRACEABILITY-MATRIX.md).

Screen ID là điểm tương tác của route gốc; PDF/JSON/POST-only được xem là hành động từ màn hình liên quan. Screen ID không quyết định layout/màu/chữ. Các màn hình gốc cần giữ để đối chiếu. Route list và backend handler ở [06](06-BACKEND-CONTRACTS.md).

| Screen ID | Màn hình/chức năng | Vai trò | Dữ liệu/thao tác | Route |
| --- | --- | --- | --- | --- |
| SCR-001 | Xem tin tức và sự kiện | Theo view; xem 05 | Hiển thị context của `home_view`; thao tác GET/POST theo [BR-001](03-BUSINESS-REQUIREMENTS.md) | `/` |
| SCR-002 | Đăng tin/sự kiện | Theo view; xem 05 | Hiển thị context của `post_add`; thao tác GET/POST theo [BR-002](03-BUSINESS-REQUIREMENTS.md) | `/add_item/` |
| SCR-003 | Sửa tin/sự kiện | Giảng viên/Admin | Hiển thị context của `edit_post`; thao tác GET/POST theo [BR-003](03-BUSINESS-REQUIREMENTS.md) | `/item/<int:pk>/edit/` |
| SCR-004 | Xóa tin/sự kiện | Giảng viên/Admin | Hiển thị context của `delete_post`; thao tác GET/POST theo [BR-004](03-BUSINESS-REQUIREMENTS.md) | `/item/<int:pk>/delete/` |
| SCR-005 | Danh sách niên khóa | Giảng viên/Admin | Hiển thị context của `session_list_view`; thao tác GET/POST theo [BR-005](03-BUSINESS-REQUIREMENTS.md) | `/session/` |
| SCR-006 | Tạo niên khóa | Giảng viên/Admin | Hiển thị context của `session_add_view`; thao tác GET/POST theo [BR-006](03-BUSINESS-REQUIREMENTS.md) | `/session/add/` |
| SCR-007 | Sửa niên khóa | Giảng viên/Admin | Hiển thị context của `session_update_view`; thao tác GET/POST theo [BR-007](03-BUSINESS-REQUIREMENTS.md) | `/session/<int:pk>/edit/` |
| SCR-008 | Xóa niên khóa | Giảng viên/Admin | Hiển thị context của `session_delete_view`; thao tác GET/POST theo [BR-008](03-BUSINESS-REQUIREMENTS.md) | `/session/<int:pk>/delete/` |
| SCR-009 | Danh sách học kỳ | Giảng viên/Admin | Hiển thị context của `semester_list_view`; thao tác GET/POST theo [BR-009](03-BUSINESS-REQUIREMENTS.md) | `/semester/` |
| SCR-010 | Tạo học kỳ | Giảng viên/Admin | Hiển thị context của `semester_add_view`; thao tác GET/POST theo [BR-010](03-BUSINESS-REQUIREMENTS.md) | `/semester/add/` |
| SCR-011 | Sửa học kỳ | Giảng viên/Admin | Hiển thị context của `semester_update_view`; thao tác GET/POST theo [BR-011](03-BUSINESS-REQUIREMENTS.md) | `/semester/<int:pk>/edit/` |
| SCR-012 | Xóa học kỳ | Giảng viên/Admin | Hiển thị context của `semester_delete_view`; thao tác GET/POST theo [BR-012](03-BUSINESS-REQUIREMENTS.md) | `/semester/<int:pk>/delete/` |
| SCR-013 | Xem thống kê quản trị | Admin | Hiển thị context của `dashboard_view`; thao tác GET/POST theo [BR-013](03-BUSINESS-REQUIREMENTS.md) | `/dashboard/` |
| SCR-014 | Mở trang quản trị | Admin | Hiển thị context của `admin_panel`; thao tác GET/POST theo [BR-014](03-BUSINESS-REQUIREMENTS.md) | `/accounts/admin_panel/` |
| SCR-015 | Xem hồ sơ | Theo view; xem 05 | Hiển thị context của `profile`; thao tác GET/POST theo [BR-015](03-BUSINESS-REQUIREMENTS.md) | `/accounts/profile/` |
| SCR-016 | Xem hồ sơ người khác | Admin | Hiển thị context của `profile_single`; thao tác GET/POST theo [BR-016](03-BUSINESS-REQUIREMENTS.md) | `/accounts/profile/<int:user_id>/detail/` |
| SCR-017 | Cập nhật hồ sơ | Theo view; xem 05 | Hiển thị context của `profile_update`; thao tác GET/POST theo [BR-017](03-BUSINESS-REQUIREMENTS.md) | `/accounts/setting/` |
| SCR-018 | Đổi mật khẩu | Theo view; xem 05 | Hiển thị context của `change_password`; thao tác GET/POST theo [BR-018](03-BUSINESS-REQUIREMENTS.md) | `/accounts/change_password/` |
| SCR-019 | Tra cứu giảng viên | Theo view; xem 05 | Hiển thị context của `LecturerFilterView`; thao tác GET/POST theo [BR-019](03-BUSINESS-REQUIREMENTS.md) | `/accounts/lecturers/` |
| SCR-020 | Thêm giảng viên | Admin | Hiển thị context của `staff_add_view`; thao tác GET/POST theo [BR-020](03-BUSINESS-REQUIREMENTS.md) | `/accounts/lecturer/add/` |
| SCR-021 | Sửa giảng viên | Admin | Hiển thị context của `edit_staff`; thao tác GET/POST theo [BR-021](03-BUSINESS-REQUIREMENTS.md) | `/accounts/staff/<int:pk>/edit/` |
| SCR-022 | Xóa giảng viên | Admin | Hiển thị context của `delete_staff`; thao tác GET/POST theo [BR-022](03-BUSINESS-REQUIREMENTS.md) | `/accounts/lecturers/<int:pk>/delete/` |
| SCR-023 | Tra cứu sinh viên | Theo view; xem 05 | Hiển thị context của `StudentListView`; thao tác GET/POST theo [BR-023](03-BUSINESS-REQUIREMENTS.md) | `/accounts/students/` |
| SCR-024 | Thêm sinh viên | Admin | Hiển thị context của `student_add_view`; thao tác GET/POST theo [BR-024](03-BUSINESS-REQUIREMENTS.md) | `/accounts/student/add/` |
| SCR-025 | Sửa sinh viên | Admin | Hiển thị context của `edit_student`; thao tác GET/POST theo [BR-025](03-BUSINESS-REQUIREMENTS.md) | `/accounts/student/<int:pk>/edit/` |
| SCR-026 | Xóa sinh viên | Admin | Hiển thị context của `delete_student`; thao tác GET/POST theo [BR-026](03-BUSINESS-REQUIREMENTS.md) | `/accounts/students/<int:pk>/delete/` |
| SCR-027 | Đổi chương trình của sinh viên | Admin | Hiển thị context của `edit_student_program`; thao tác GET/POST theo [BR-027](03-BUSINESS-REQUIREMENTS.md) | `/accounts/edit_student_program/<int:pk>/` |
| SCR-028 | Thêm phụ huynh | Theo view; xem 05 | Hiển thị context của `ParentAdd`; thao tác GET/POST theo [BR-028](03-BUSINESS-REQUIREMENTS.md) | `/accounts/parents/add/` |
| SCR-030 | Sinh viên tự đăng ký | Công khai | Hiển thị context của `register`; thao tác GET/POST theo [BR-030](03-BUSINESS-REQUIREMENTS.md) | `/accounts/register/` |
| SCR-031 | Xuất danh sách giảng viên PDF | Admin | Hiển thị context của `render_lecturer_pdf_list`; thao tác GET/POST theo [BR-031](03-BUSINESS-REQUIREMENTS.md) | `/accounts/create_lecturers_pdf_list/` |
| SCR-032 | Xuất danh sách sinh viên PDF | Admin | Hiển thị context của `render_student_pdf_list`; thao tác GET/POST theo [BR-032](03-BUSINESS-REQUIREMENTS.md) | `/accounts/create_students_pdf_list/` |
| SCR-033 | Danh sách chương trình | Theo view; xem 05 | Hiển thị context của `ProgramFilterView`; thao tác GET/POST theo [BR-033](03-BUSINESS-REQUIREMENTS.md) | `/programs/` |
| SCR-034 | Xem chương trình | Theo view; xem 05 | Hiển thị context của `program_detail`; thao tác GET/POST theo [BR-034](03-BUSINESS-REQUIREMENTS.md) | `/programs/<int:pk>/detail/` |
| SCR-035 | Thêm chương trình | Giảng viên/Admin | Hiển thị context của `program_add`; thao tác GET/POST theo [BR-035](03-BUSINESS-REQUIREMENTS.md) | `/programs/add/` |
| SCR-036 | Sửa chương trình | Giảng viên/Admin | Hiển thị context của `program_edit`; thao tác GET/POST theo [BR-036](03-BUSINESS-REQUIREMENTS.md) | `/programs/<int:pk>/edit/` |
| SCR-037 | Xóa chương trình | Giảng viên/Admin | Hiển thị context của `program_delete`; thao tác GET/POST theo [BR-037](03-BUSINESS-REQUIREMENTS.md) | `/programs/<int:pk>/delete/` |
| SCR-038 | Xem học phần | Theo view; xem 05 | Hiển thị context của `course_single`; thao tác GET/POST theo [BR-038](03-BUSINESS-REQUIREMENTS.md) | `/programs/course/<slug>/detail/` |
| SCR-039 | Thêm học phần | Giảng viên/Admin | Hiển thị context của `course_add`; thao tác GET/POST theo [BR-039](03-BUSINESS-REQUIREMENTS.md) | `/programs/<int:pk>/course/add/` |
| SCR-040 | Sửa học phần | Giảng viên/Admin | Hiển thị context của `course_edit`; thao tác GET/POST theo [BR-040](03-BUSINESS-REQUIREMENTS.md) | `/programs/course/<slug>/edit/` |
| SCR-041 | Xóa học phần | Giảng viên/Admin | Hiển thị context của `course_delete`; thao tác GET/POST theo [BR-041](03-BUSINESS-REQUIREMENTS.md) | `/programs/course/delete/<slug>/` |
| SCR-042 | Phân công giảng viên | Theo view; xem 05 | Hiển thị context của `CourseAllocationFormView`; thao tác GET/POST theo [BR-042](03-BUSINESS-REQUIREMENTS.md) | `/programs/course/assign/` |
| SCR-043 | Xem phân công | Theo view; xem 05 | Hiển thị context của `CourseAllocationFilterView`; thao tác GET/POST theo [BR-043](03-BUSINESS-REQUIREMENTS.md) | `/programs/course/allocated/` |
| SCR-044 | Sửa phân công | Giảng viên/Admin | Hiển thị context của `edit_allocated_course`; thao tác GET/POST theo [BR-044](03-BUSINESS-REQUIREMENTS.md) | `/programs/allocated_course/<int:pk>/edit/` |
| SCR-045 | Hủy phân công | Giảng viên/Admin | Hiển thị context của `deallocate_course`; thao tác GET/POST theo [BR-045](03-BUSINESS-REQUIREMENTS.md) | `/programs/course/<int:pk>/deallocate/` |
| SCR-046 | Tải tài liệu | Giảng viên/Admin | Hiển thị context của `handle_file_upload`; thao tác GET/POST theo [BR-046](03-BUSINESS-REQUIREMENTS.md) | `/programs/course/<slug>/documentations/upload/` |
| SCR-047 | Sửa tài liệu | Giảng viên/Admin | Hiển thị context của `handle_file_edit`; thao tác GET/POST theo [BR-047](03-BUSINESS-REQUIREMENTS.md) | `/programs/course/<slug>/documentations/<int:file_id>/edit/` |
| SCR-048 | Xóa tài liệu | Giảng viên/Admin | Hiển thị context của `handle_file_delete`; thao tác GET/POST theo [BR-048](03-BUSINESS-REQUIREMENTS.md) | `/programs/course/<slug>/documentations/<int:file_id>/delete/` |
| SCR-049 | Tải video | Giảng viên/Admin | Hiển thị context của `handle_video_upload`; thao tác GET/POST theo [BR-049](03-BUSINESS-REQUIREMENTS.md) | `/programs/course/<slug>/video_tutorials/upload/` |
| SCR-050 | Xem video | Theo view; xem 05 | Hiển thị context của `handle_video_single`; thao tác GET/POST theo [BR-050](03-BUSINESS-REQUIREMENTS.md) | `/programs/course/<slug>/video_tutorials/<video_slug>/detail/` |
| SCR-051 | Sửa video | Giảng viên/Admin | Hiển thị context của `handle_video_edit`; thao tác GET/POST theo [BR-051](03-BUSINESS-REQUIREMENTS.md) | `/programs/course/<slug>/video_tutorials/<video_slug>/edit/` |
| SCR-052 | Xóa video | Giảng viên/Admin | Hiển thị context của `handle_video_delete`; thao tác GET/POST theo [BR-052](03-BUSINESS-REQUIREMENTS.md) | `/programs/course/<slug>/video_tutorials/<video_slug>/delete/` |
| SCR-053 | Đăng ký học phần | Sinh viên/Admin | Hiển thị context của `course_registration`; thao tác GET/POST theo [BR-053](03-BUSINESS-REQUIREMENTS.md) | `/programs/course/registration/` |
| SCR-054 | Hủy học phần | Sinh viên/Admin | Hiển thị context của `course_drop`; thao tác GET/POST theo [BR-054](03-BUSINESS-REQUIREMENTS.md) | `/programs/course/drop/` |
| SCR-055 | Xem học phần của tôi | Theo view; xem 05 | Hiển thị context của `user_course_list`; thao tác GET/POST theo [BR-055](03-BUSINESS-REQUIREMENTS.md) | `/programs/my_courses/` |
| SCR-056 | Chọn môn nhập điểm | Giảng viên/Admin | Hiển thị context của `add_score`; thao tác GET/POST theo [BR-056](03-BUSINESS-REQUIREMENTS.md) | `/result/manage-score/` |
| SCR-057 | Nhập điểm thành phần | Giảng viên/Admin | Hiển thị context của `add_score_for`; thao tác GET/POST theo [BR-057](03-BUSINESS-REQUIREMENTS.md) | `/result/manage-score/<int:id>/` |
| SCR-058 | Xem điểm tổng kết | Sinh viên/Admin | Hiển thị context của `grade_result`; thao tác GET/POST theo [BR-058](03-BUSINESS-REQUIREMENTS.md) | `/result/grade/` |
| SCR-059 | Xem điểm đánh giá | Sinh viên/Admin | Hiển thị context của `assessment_result`; thao tác GET/POST theo [BR-059](03-BUSINESS-REQUIREMENTS.md) | `/result/assessment/` |
| SCR-062 | Xem danh sách quiz | Theo view; xem 05 | Hiển thị context của `quiz_list`; thao tác GET/POST theo [BR-062](03-BUSINESS-REQUIREMENTS.md) | `/quiz/<slug>/quizzes/` |
| SCR-063 | Xem tiến độ quiz | Theo view; xem 05 | Hiển thị context của `QuizUserProgressView`; thao tác GET/POST theo [BR-063](03-BUSINESS-REQUIREMENTS.md) | `/quiz/progress/` |
| SCR-064 | Xem bài quiz đã nộp | Giảng viên/Admin | Hiển thị context của `QuizMarkingList`; thao tác GET/POST theo [BR-064](03-BUSINESS-REQUIREMENTS.md) | `/quiz/marking_list/` |
| SCR-065 | Đánh dấu/chấm bài quiz | Giảng viên/Admin | Hiển thị context của `QuizMarkingDetail`; thao tác GET/POST theo [BR-065](03-BUSINESS-REQUIREMENTS.md) | `/quiz/marking/<int:pk>/` |
| SCR-066 | Làm bài quiz | Theo view; xem 05 | Hiển thị context của `QuizTake`; thao tác GET/POST theo [BR-066](03-BUSINESS-REQUIREMENTS.md) | `/quiz/<int:pk>/<slug>/take/` |
| SCR-067 | Tạo quiz | Theo view; xem 05 | Hiển thị context của `QuizCreateView`; thao tác GET/POST theo [BR-067](03-BUSINESS-REQUIREMENTS.md) | `/quiz/<slug>/quiz_add/` |
| SCR-068 | Sửa quiz | Theo view; xem 05 | Hiển thị context của `QuizUpdateView`; thao tác GET/POST theo [BR-068](03-BUSINESS-REQUIREMENTS.md) | `/quiz/<slug>/<int:pk>/add/` |
| SCR-069 | Xóa quiz | Giảng viên/Admin | Hiển thị context của `quiz_delete`; thao tác GET/POST theo [BR-069](03-BUSINESS-REQUIREMENTS.md) | `/quiz/<slug>/<int:pk>/delete/` |
| SCR-070 | Tạo câu hỏi trắc nghiệm | Theo view; xem 05 | Hiển thị context của `MCQuestionCreate`; thao tác GET/POST theo [BR-070](03-BUSINESS-REQUIREMENTS.md) | `/quiz/mc-question/add/<slug>/<int:quiz_id>/` |
| SCR-071 | Xem lựa chọn thanh toán | Chưa kiểm soát rõ | Hiển thị context của `PaymentGetwaysView`; thao tác GET/POST theo [BR-071](03-BUSINESS-REQUIREMENTS.md) | `/payments/` |
| SCR-072 | Xem trang PayPal mẫu | Chưa kiểm soát rõ | Hiển thị context của `payment_paypal`; thao tác GET/POST theo [BR-072](03-BUSINESS-REQUIREMENTS.md) | `/payments/paypal/` |
| SCR-073 | Xem trang Stripe mẫu | Chưa kiểm soát rõ | Hiển thị context của `payment_stripe`; thao tác GET/POST theo [BR-073](03-BUSINESS-REQUIREMENTS.md) | `/payments/stripe/` |
| SCR-074 | Xem trang Coinbase mẫu | Chưa kiểm soát rõ | Hiển thị context của `payment_coinbase`; thao tác GET/POST theo [BR-074](03-BUSINESS-REQUIREMENTS.md) | `/payments/coinbase/` |
| SCR-075 | Xem trang Paylike mẫu | Chưa kiểm soát rõ | Hiển thị context của `payment_paylike`; thao tác GET/POST theo [BR-075](03-BUSINESS-REQUIREMENTS.md) | `/payments/paylike/` |
| SCR-078 | Xem thông báo thanh toán | Chưa kiểm soát rõ | Hiển thị context của `payment_succeed`; thao tác GET/POST theo [BR-078](03-BUSINESS-REQUIREMENTS.md) | `/payments/payment-succeed/` |
| SCR-080 | Tạo/xem hóa đơn | Chưa kiểm soát rõ | Hiển thị context của `create_invoice`; thao tác GET/POST theo [BR-080](03-BUSINESS-REQUIREMENTS.md) | `/payments/create-invoice/` |
| SCR-081 | Xem hóa đơn theo mã | Chưa kiểm soát rõ | Hiển thị context của `invoice_detail`; thao tác GET/POST theo [BR-081](03-BUSINESS-REQUIREMENTS.md) | `/payments/invoice-detail/<int:id>/` |
| SCR-082 | Tìm kiếm toàn hệ thống | Theo view; xem 05 | Hiển thị context của `SearchView`; thao tác GET/POST theo [BR-082](03-BUSINESS-REQUIREMENTS.md) | `/search/` |

## Form và trạng thái chung

- Form fields phải lấy từ `accounts/forms.py`, `core/forms.py`, `course/forms.py`, `quiz/forms.py` và form/POST tự xử lý trong `result/views.py`/`payments/views.py`; đừng thay tên input. Field errors, non-field errors, CSRF token, file multipart, các lựa chọn checkbox/radio/formset và `DELETE` phải còn hoạt động.
- Loading: khi request đang gửi, ngăn submit lặp ở UI nhưng không giả định backend idempotent. Empty: danh sách rỗng, kỳ chưa kích hoạt, quiz không có câu hỏi theo handler. Success: hiển thị Django messages hoặc response. Error: hiển thị form errors/403/404 và lỗi handler; không biến mọi exception thành thông báo thành công.
- Điều hướng: giữ URL name, URL parameter `pk/id/slug/file_id/video_slug/quiz_id`, phân trang/filter `q` và các query của django-filter. PDF là download/action; JSON validation username và payment là tương tác, không tự tạo màn hình mới.
- Phân quyền UI: dựa trên backend ở [05](05-ROLES-AND-PERMISSIONS.md). Hiện có CBV thiếu guard; phải ghi issue trước khi thay đổi backend; chỉ ẩn nút không phải bảo vệ.

## Hợp đồng theo màn hình trọng tâm

`SCR-053` đăng ký môn: dữ liệu học kỳ, môn chưa đăng ký, môn đã đăng ký, tín chỉ; POST key là ID môn. `SCR-054` hủy: POST `course_ids`. `SCR-057` nhập điểm: năm điểm theo thứ tự cố định. `SCR-066` quiz: `answers`, tiến độ từng câu, kết quả. Số ID chính xác đối chiếu ma trận; source `course/views.py`, `result/views.py`, `quiz/views.py`.


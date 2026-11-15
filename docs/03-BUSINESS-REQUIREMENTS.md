# Danh mục nghiệp vụ gốc

> Baseline: [SkyCascade/SkyLearn](https://github.com/SkyCascade/SkyLearn), nhánh `main`, commit `d57f57bd505447b59fdf82b16469494443cafe0c`. Đây là bản kiểm kê mã nguồn, không phải đặc tả tính năng mới. Trạng thái tải source và kiểm thử: [11-SETUP-AND-DEPLOYMENT.md](11-SETUP-AND-DEPLOYMENT.md).

**Quy ước:** Một BR biểu diễn một hành động route-backed. Trạng thái “mẫu/lỗi” vẫn được ghi để không bỏ rơi giao diện gốc, không khẳng định hoạt động thành công. Điều kiện chung của route có `@login_required`: đăng nhập; role cụ thể ở [05](05-ROLES-AND-PERMISSIONS.md). POST form chịu CSRF và validation của Django. Chi tiết request/response ở [06](06-BACKEND-CONTRACTS.md).

### BR-001 — Xem tin tức và sự kiện

- **Actor/điều kiện:** Theo view; xem 05; theo decorator/CBV thực tế.
- **Luồng chính:** Đọc dữ liệu/điều kiện trong handler; render HTML hoặc response chuyên biệt.
- **Ngoại lệ/quy tắc:** Form không hợp lệ giữ trang/lỗi theo handler; đối tượng không tồn tại có thể trả 404 hoặc exception, tùy hàm lookup. Không áp đặt quy tắc bổ sung.
- **Kết quả:** HTML, redirect, PDF hoặc JSON theo handler; route `/`.
- **Nguồn:** [`core/views.py::home_view`](../core/views.py), [`core/urls.py`](../core/urls.py).

### BR-002 — Đăng tin/sự kiện

- **Actor/điều kiện:** Theo view; xem 05; theo decorator/CBV thực tế.
- **Luồng chính:** GET hiển thị form; POST validate/lưu; trả form lỗi hoặc redirect theo view.
- **Ngoại lệ/quy tắc:** Form không hợp lệ giữ trang/lỗi theo handler; đối tượng không tồn tại có thể trả 404 hoặc exception, tùy hàm lookup. Không áp đặt quy tắc bổ sung.
- **Kết quả:** HTML, redirect, PDF hoặc JSON theo handler; route `/add_item/`.
- **Nguồn:** [`core/views.py::post_add`](../core/views.py), [`core/urls.py`](../core/urls.py).

### BR-003 — Sửa tin/sự kiện

- **Actor/điều kiện:** Giảng viên/Admin; theo decorator/CBV thực tế.
- **Luồng chính:** GET hiển thị form; POST validate/lưu; trả form lỗi hoặc redirect theo view.
- **Ngoại lệ/quy tắc:** Form không hợp lệ giữ trang/lỗi theo handler; đối tượng không tồn tại có thể trả 404 hoặc exception, tùy hàm lookup. Không áp đặt quy tắc bổ sung.
- **Kết quả:** HTML, redirect, PDF hoặc JSON theo handler; route `/item/<int:pk>/edit/`.
- **Nguồn:** [`core/views.py::edit_post`](../core/views.py), [`core/urls.py`](../core/urls.py).

### BR-004 — Xóa tin/sự kiện

- **Actor/điều kiện:** Giảng viên/Admin; theo decorator/CBV thực tế.
- **Luồng chính:** Nhận đối tượng/ID; xác nhận hoặc POST theo view; xóa/hủy; redirect hoặc thông báo.
- **Ngoại lệ/quy tắc:** Form không hợp lệ giữ trang/lỗi theo handler; đối tượng không tồn tại có thể trả 404 hoặc exception, tùy hàm lookup. Không áp đặt quy tắc bổ sung.
- **Kết quả:** HTML, redirect, PDF hoặc JSON theo handler; route `/item/<int:pk>/delete/`.
- **Nguồn:** [`core/views.py::delete_post`](../core/views.py), [`core/urls.py`](../core/urls.py).

### BR-005 — Danh sách niên khóa

- **Actor/điều kiện:** Giảng viên/Admin; theo decorator/CBV thực tế.
- **Luồng chính:** Đọc dữ liệu/điều kiện trong handler; render HTML hoặc response chuyên biệt.
- **Ngoại lệ/quy tắc:** Form không hợp lệ giữ trang/lỗi theo handler; đối tượng không tồn tại có thể trả 404 hoặc exception, tùy hàm lookup. Không áp đặt quy tắc bổ sung.
- **Kết quả:** HTML, redirect, PDF hoặc JSON theo handler; route `/session/`.
- **Nguồn:** [`core/views.py::session_list_view`](../core/views.py), [`core/urls.py`](../core/urls.py).

### BR-006 — Tạo niên khóa

- **Actor/điều kiện:** Giảng viên/Admin; theo decorator/CBV thực tế.
- **Luồng chính:** GET hiển thị form; POST validate/lưu; trả form lỗi hoặc redirect theo view.
- **Ngoại lệ/quy tắc:** Form không hợp lệ giữ trang/lỗi theo handler; đối tượng không tồn tại có thể trả 404 hoặc exception, tùy hàm lookup. Không áp đặt quy tắc bổ sung.
- **Kết quả:** HTML, redirect, PDF hoặc JSON theo handler; route `/session/add/`.
- **Nguồn:** [`core/views.py::session_add_view`](../core/views.py), [`core/urls.py`](../core/urls.py).

### BR-007 — Sửa niên khóa

- **Actor/điều kiện:** Giảng viên/Admin; theo decorator/CBV thực tế.
- **Luồng chính:** GET hiển thị form; POST validate/lưu; trả form lỗi hoặc redirect theo view.
- **Ngoại lệ/quy tắc:** Form không hợp lệ giữ trang/lỗi theo handler; đối tượng không tồn tại có thể trả 404 hoặc exception, tùy hàm lookup. Không áp đặt quy tắc bổ sung.
- **Kết quả:** HTML, redirect, PDF hoặc JSON theo handler; route `/session/<int:pk>/edit/`.
- **Nguồn:** [`core/views.py::session_update_view`](../core/views.py), [`core/urls.py`](../core/urls.py).

### BR-008 — Xóa niên khóa

- **Actor/điều kiện:** Giảng viên/Admin; theo decorator/CBV thực tế.
- **Luồng chính:** Nhận đối tượng/ID; xác nhận hoặc POST theo view; xóa/hủy; redirect hoặc thông báo.
- **Ngoại lệ/quy tắc:** Form không hợp lệ giữ trang/lỗi theo handler; đối tượng không tồn tại có thể trả 404 hoặc exception, tùy hàm lookup. Không áp đặt quy tắc bổ sung.
- **Kết quả:** HTML, redirect, PDF hoặc JSON theo handler; route `/session/<int:pk>/delete/`.
- **Nguồn:** [`core/views.py::session_delete_view`](../core/views.py), [`core/urls.py`](../core/urls.py).

### BR-009 — Danh sách học kỳ

- **Actor/điều kiện:** Giảng viên/Admin; theo decorator/CBV thực tế.
- **Luồng chính:** Đọc dữ liệu/điều kiện trong handler; render HTML hoặc response chuyên biệt.
- **Ngoại lệ/quy tắc:** Form không hợp lệ giữ trang/lỗi theo handler; đối tượng không tồn tại có thể trả 404 hoặc exception, tùy hàm lookup. Không áp đặt quy tắc bổ sung.
- **Kết quả:** HTML, redirect, PDF hoặc JSON theo handler; route `/semester/`.
- **Nguồn:** [`core/views.py::semester_list_view`](../core/views.py), [`core/urls.py`](../core/urls.py).

### BR-010 — Tạo học kỳ

- **Actor/điều kiện:** Giảng viên/Admin; theo decorator/CBV thực tế.
- **Luồng chính:** GET hiển thị form; POST validate/lưu; trả form lỗi hoặc redirect theo view.
- **Ngoại lệ/quy tắc:** Form không hợp lệ giữ trang/lỗi theo handler; đối tượng không tồn tại có thể trả 404 hoặc exception, tùy hàm lookup. Không áp đặt quy tắc bổ sung.
- **Kết quả:** HTML, redirect, PDF hoặc JSON theo handler; route `/semester/add/`.
- **Nguồn:** [`core/views.py::semester_add_view`](../core/views.py), [`core/urls.py`](../core/urls.py).

### BR-011 — Sửa học kỳ

- **Actor/điều kiện:** Giảng viên/Admin; theo decorator/CBV thực tế.
- **Luồng chính:** GET hiển thị form; POST validate/lưu; trả form lỗi hoặc redirect theo view.
- **Ngoại lệ/quy tắc:** Form không hợp lệ giữ trang/lỗi theo handler; đối tượng không tồn tại có thể trả 404 hoặc exception, tùy hàm lookup. Không áp đặt quy tắc bổ sung.
- **Kết quả:** HTML, redirect, PDF hoặc JSON theo handler; route `/semester/<int:pk>/edit/`.
- **Nguồn:** [`core/views.py::semester_update_view`](../core/views.py), [`core/urls.py`](../core/urls.py).

### BR-012 — Xóa học kỳ

- **Actor/điều kiện:** Giảng viên/Admin; theo decorator/CBV thực tế.
- **Luồng chính:** Nhận đối tượng/ID; xác nhận hoặc POST theo view; xóa/hủy; redirect hoặc thông báo.
- **Ngoại lệ/quy tắc:** Form không hợp lệ giữ trang/lỗi theo handler; đối tượng không tồn tại có thể trả 404 hoặc exception, tùy hàm lookup. Không áp đặt quy tắc bổ sung.
- **Kết quả:** HTML, redirect, PDF hoặc JSON theo handler; route `/semester/<int:pk>/delete/`.
- **Nguồn:** [`core/views.py::semester_delete_view`](../core/views.py), [`core/urls.py`](../core/urls.py).

### BR-013 — Xem thống kê quản trị

- **Actor/điều kiện:** Admin; theo decorator/CBV thực tế.
- **Luồng chính:** Đọc dữ liệu/điều kiện trong handler; render HTML hoặc response chuyên biệt.
- **Ngoại lệ/quy tắc:** Form không hợp lệ giữ trang/lỗi theo handler; đối tượng không tồn tại có thể trả 404 hoặc exception, tùy hàm lookup. Không áp đặt quy tắc bổ sung.
- **Kết quả:** HTML, redirect, PDF hoặc JSON theo handler; route `/dashboard/`.
- **Nguồn:** [`core/views.py::dashboard_view`](../core/views.py), [`core/urls.py`](../core/urls.py).

### BR-014 — Mở trang quản trị

- **Actor/điều kiện:** Admin; theo decorator/CBV thực tế.
- **Luồng chính:** Đọc dữ liệu/điều kiện trong handler; render HTML hoặc response chuyên biệt.
- **Ngoại lệ/quy tắc:** Form không hợp lệ giữ trang/lỗi theo handler; đối tượng không tồn tại có thể trả 404 hoặc exception, tùy hàm lookup. Không áp đặt quy tắc bổ sung.
- **Kết quả:** HTML, redirect, PDF hoặc JSON theo handler; route `/accounts/admin_panel/`.
- **Nguồn:** [`accounts/views.py::admin_panel`](../accounts/views.py), [`accounts/urls.py`](../accounts/urls.py).

### BR-015 — Xem hồ sơ

- **Actor/điều kiện:** Theo view; xem 05; theo decorator/CBV thực tế.
- **Luồng chính:** Đọc dữ liệu/điều kiện trong handler; render HTML hoặc response chuyên biệt.
- **Ngoại lệ/quy tắc:** Form không hợp lệ giữ trang/lỗi theo handler; đối tượng không tồn tại có thể trả 404 hoặc exception, tùy hàm lookup. Không áp đặt quy tắc bổ sung.
- **Kết quả:** HTML, redirect, PDF hoặc JSON theo handler; route `/accounts/profile/`.
- **Nguồn:** [`accounts/views.py::profile`](../accounts/views.py), [`accounts/urls.py`](../accounts/urls.py).

### BR-016 — Xem hồ sơ người khác

- **Actor/điều kiện:** Admin; theo decorator/CBV thực tế.
- **Luồng chính:** Đọc dữ liệu/điều kiện trong handler; render HTML hoặc response chuyên biệt.
- **Ngoại lệ/quy tắc:** Form không hợp lệ giữ trang/lỗi theo handler; đối tượng không tồn tại có thể trả 404 hoặc exception, tùy hàm lookup. Không áp đặt quy tắc bổ sung.
- **Kết quả:** HTML, redirect, PDF hoặc JSON theo handler; route `/accounts/profile/<int:user_id>/detail/`.
- **Nguồn:** [`accounts/views.py::profile_single`](../accounts/views.py), [`accounts/urls.py`](../accounts/urls.py).

### BR-017 — Cập nhật hồ sơ

- **Actor/điều kiện:** Theo view; xem 05; theo decorator/CBV thực tế.
- **Luồng chính:** GET hiển thị form; POST validate/lưu; trả form lỗi hoặc redirect theo view.
- **Ngoại lệ/quy tắc:** Form không hợp lệ giữ trang/lỗi theo handler; đối tượng không tồn tại có thể trả 404 hoặc exception, tùy hàm lookup. Không áp đặt quy tắc bổ sung.
- **Kết quả:** HTML, redirect, PDF hoặc JSON theo handler; route `/accounts/setting/`.
- **Nguồn:** [`accounts/views.py::profile_update`](../accounts/views.py), [`accounts/urls.py`](../accounts/urls.py).

### BR-018 — Đổi mật khẩu

- **Actor/điều kiện:** Theo view; xem 05; theo decorator/CBV thực tế.
- **Luồng chính:** Đọc dữ liệu/điều kiện trong handler; render HTML hoặc response chuyên biệt.
- **Ngoại lệ/quy tắc:** Form không hợp lệ giữ trang/lỗi theo handler; đối tượng không tồn tại có thể trả 404 hoặc exception, tùy hàm lookup. Không áp đặt quy tắc bổ sung.
- **Kết quả:** HTML, redirect, PDF hoặc JSON theo handler; route `/accounts/change_password/`.
- **Nguồn:** [`accounts/views.py::change_password`](../accounts/views.py), [`accounts/urls.py`](../accounts/urls.py).

### BR-019 — Tra cứu giảng viên

- **Actor/điều kiện:** Theo view; xem 05; theo decorator/CBV thực tế.
- **Luồng chính:** Đọc dữ liệu/điều kiện trong handler; render HTML hoặc response chuyên biệt.
- **Ngoại lệ/quy tắc:** Form không hợp lệ giữ trang/lỗi theo handler; đối tượng không tồn tại có thể trả 404 hoặc exception, tùy hàm lookup. Không áp đặt quy tắc bổ sung.
- **Kết quả:** HTML, redirect, PDF hoặc JSON theo handler; route `/accounts/lecturers/`.
- **Nguồn:** [`accounts/views.py::LecturerFilterView`](../accounts/views.py), [`accounts/urls.py`](../accounts/urls.py).

### BR-020 — Thêm giảng viên

- **Actor/điều kiện:** Admin; theo decorator/CBV thực tế.
- **Luồng chính:** GET hiển thị form; POST validate/lưu; trả form lỗi hoặc redirect theo view.
- **Ngoại lệ/quy tắc:** Form không hợp lệ giữ trang/lỗi theo handler; đối tượng không tồn tại có thể trả 404 hoặc exception, tùy hàm lookup. Không áp đặt quy tắc bổ sung.
- **Kết quả:** HTML, redirect, PDF hoặc JSON theo handler; route `/accounts/lecturer/add/`.
- **Nguồn:** [`accounts/views.py::staff_add_view`](../accounts/views.py), [`accounts/urls.py`](../accounts/urls.py).

### BR-021 — Sửa giảng viên

- **Actor/điều kiện:** Admin; theo decorator/CBV thực tế.
- **Luồng chính:** GET hiển thị form; POST validate/lưu; trả form lỗi hoặc redirect theo view.
- **Ngoại lệ/quy tắc:** Form không hợp lệ giữ trang/lỗi theo handler; đối tượng không tồn tại có thể trả 404 hoặc exception, tùy hàm lookup. Không áp đặt quy tắc bổ sung.
- **Kết quả:** HTML, redirect, PDF hoặc JSON theo handler; route `/accounts/staff/<int:pk>/edit/`.
- **Nguồn:** [`accounts/views.py::edit_staff`](../accounts/views.py), [`accounts/urls.py`](../accounts/urls.py).

### BR-022 — Xóa giảng viên

- **Actor/điều kiện:** Admin; theo decorator/CBV thực tế.
- **Luồng chính:** Nhận đối tượng/ID; xác nhận hoặc POST theo view; xóa/hủy; redirect hoặc thông báo.
- **Ngoại lệ/quy tắc:** Form không hợp lệ giữ trang/lỗi theo handler; đối tượng không tồn tại có thể trả 404 hoặc exception, tùy hàm lookup. Không áp đặt quy tắc bổ sung.
- **Kết quả:** HTML, redirect, PDF hoặc JSON theo handler; route `/accounts/lecturers/<int:pk>/delete/`.
- **Nguồn:** [`accounts/views.py::delete_staff`](../accounts/views.py), [`accounts/urls.py`](../accounts/urls.py).

### BR-023 — Tra cứu sinh viên

- **Actor/điều kiện:** Theo view; xem 05; theo decorator/CBV thực tế.
- **Luồng chính:** Đọc dữ liệu/điều kiện trong handler; render HTML hoặc response chuyên biệt.
- **Ngoại lệ/quy tắc:** Form không hợp lệ giữ trang/lỗi theo handler; đối tượng không tồn tại có thể trả 404 hoặc exception, tùy hàm lookup. Không áp đặt quy tắc bổ sung.
- **Kết quả:** HTML, redirect, PDF hoặc JSON theo handler; route `/accounts/students/`.
- **Nguồn:** [`accounts/views.py::StudentListView`](../accounts/views.py), [`accounts/urls.py`](../accounts/urls.py).

### BR-024 — Thêm sinh viên

- **Actor/điều kiện:** Admin; theo decorator/CBV thực tế.
- **Luồng chính:** GET hiển thị form; POST validate/lưu; trả form lỗi hoặc redirect theo view.
- **Ngoại lệ/quy tắc:** Form không hợp lệ giữ trang/lỗi theo handler; đối tượng không tồn tại có thể trả 404 hoặc exception, tùy hàm lookup. Không áp đặt quy tắc bổ sung.
- **Kết quả:** HTML, redirect, PDF hoặc JSON theo handler; route `/accounts/student/add/`.
- **Nguồn:** [`accounts/views.py::student_add_view`](../accounts/views.py), [`accounts/urls.py`](../accounts/urls.py).

### BR-025 — Sửa sinh viên

- **Actor/điều kiện:** Admin; theo decorator/CBV thực tế.
- **Luồng chính:** GET hiển thị form; POST validate/lưu; trả form lỗi hoặc redirect theo view.
- **Ngoại lệ/quy tắc:** Form không hợp lệ giữ trang/lỗi theo handler; đối tượng không tồn tại có thể trả 404 hoặc exception, tùy hàm lookup. Không áp đặt quy tắc bổ sung.
- **Kết quả:** HTML, redirect, PDF hoặc JSON theo handler; route `/accounts/student/<int:pk>/edit/`.
- **Nguồn:** [`accounts/views.py::edit_student`](../accounts/views.py), [`accounts/urls.py`](../accounts/urls.py).

### BR-026 — Xóa sinh viên

- **Actor/điều kiện:** Admin; theo decorator/CBV thực tế.
- **Luồng chính:** Nhận đối tượng/ID; xác nhận hoặc POST theo view; xóa/hủy; redirect hoặc thông báo.
- **Ngoại lệ/quy tắc:** Form không hợp lệ giữ trang/lỗi theo handler; đối tượng không tồn tại có thể trả 404 hoặc exception, tùy hàm lookup. Không áp đặt quy tắc bổ sung.
- **Kết quả:** HTML, redirect, PDF hoặc JSON theo handler; route `/accounts/students/<int:pk>/delete/`.
- **Nguồn:** [`accounts/views.py::delete_student`](../accounts/views.py), [`accounts/urls.py`](../accounts/urls.py).

### BR-027 — Đổi chương trình của sinh viên

- **Actor/điều kiện:** Admin; theo decorator/CBV thực tế.
- **Luồng chính:** GET hiển thị form; POST validate/lưu; trả form lỗi hoặc redirect theo view.
- **Ngoại lệ/quy tắc:** Form không hợp lệ giữ trang/lỗi theo handler; đối tượng không tồn tại có thể trả 404 hoặc exception, tùy hàm lookup. Không áp đặt quy tắc bổ sung.
- **Kết quả:** HTML, redirect, PDF hoặc JSON theo handler; route `/accounts/edit_student_program/<int:pk>/`.
- **Nguồn:** [`accounts/views.py::edit_student_program`](../accounts/views.py), [`accounts/urls.py`](../accounts/urls.py).

### BR-028 — Thêm phụ huynh

- **Actor/điều kiện:** Theo view; xem 05; theo decorator/CBV thực tế.
- **Luồng chính:** Đọc dữ liệu/điều kiện trong handler; render HTML hoặc response chuyên biệt.
- **Ngoại lệ/quy tắc:** Form không hợp lệ giữ trang/lỗi theo handler; đối tượng không tồn tại có thể trả 404 hoặc exception, tùy hàm lookup. Không áp đặt quy tắc bổ sung.
- **Kết quả:** HTML, redirect, PDF hoặc JSON theo handler; route `/accounts/parents/add/`.
- **Nguồn:** [`accounts/views.py::ParentAdd`](../accounts/views.py), [`accounts/urls.py`](../accounts/urls.py).

### BR-029 — Kiểm tra tên đăng nhập

- **Actor/điều kiện:** Công khai; không yêu cầu đăng nhập trong view.
- **Luồng chính:** Đọc dữ liệu/điều kiện trong handler; render HTML hoặc response chuyên biệt.
- **Ngoại lệ/quy tắc:** Form không hợp lệ giữ trang/lỗi theo handler; đối tượng không tồn tại có thể trả 404 hoặc exception, tùy hàm lookup. Không áp đặt quy tắc bổ sung.
- **Kết quả:** HTML, redirect, PDF hoặc JSON theo handler; route `/accounts/ajax/validate-username/`.
- **Nguồn:** [`accounts/views.py::validate_username`](../accounts/views.py), [`accounts/urls.py`](../accounts/urls.py).

### BR-030 — Sinh viên tự đăng ký

- **Actor/điều kiện:** Công khai; không yêu cầu đăng nhập trong view.
- **Luồng chính:** GET hiển thị form; POST validate/lưu; trả form lỗi hoặc redirect theo view.
- **Ngoại lệ/quy tắc:** Form không hợp lệ giữ trang/lỗi theo handler; đối tượng không tồn tại có thể trả 404 hoặc exception, tùy hàm lookup. Không áp đặt quy tắc bổ sung.
- **Kết quả:** HTML, redirect, PDF hoặc JSON theo handler; route `/accounts/register/`.
- **Nguồn:** [`accounts/views.py::register`](../accounts/views.py), [`accounts/urls.py`](../accounts/urls.py).

### BR-031 — Xuất danh sách giảng viên PDF

- **Actor/điều kiện:** Admin; theo decorator/CBV thực tế.
- **Luồng chính:** Đọc dữ liệu/điều kiện trong handler; render HTML hoặc response chuyên biệt.
- **Ngoại lệ/quy tắc:** Form không hợp lệ giữ trang/lỗi theo handler; đối tượng không tồn tại có thể trả 404 hoặc exception, tùy hàm lookup. Không áp đặt quy tắc bổ sung.
- **Kết quả:** HTML, redirect, PDF hoặc JSON theo handler; route `/accounts/create_lecturers_pdf_list/`.
- **Nguồn:** [`accounts/views.py::render_lecturer_pdf_list`](../accounts/views.py), [`accounts/urls.py`](../accounts/urls.py).

### BR-032 — Xuất danh sách sinh viên PDF

- **Actor/điều kiện:** Admin; theo decorator/CBV thực tế.
- **Luồng chính:** Đọc dữ liệu/điều kiện trong handler; render HTML hoặc response chuyên biệt.
- **Ngoại lệ/quy tắc:** Form không hợp lệ giữ trang/lỗi theo handler; đối tượng không tồn tại có thể trả 404 hoặc exception, tùy hàm lookup. Không áp đặt quy tắc bổ sung.
- **Kết quả:** HTML, redirect, PDF hoặc JSON theo handler; route `/accounts/create_students_pdf_list/`.
- **Nguồn:** [`accounts/views.py::render_student_pdf_list`](../accounts/views.py), [`accounts/urls.py`](../accounts/urls.py).

### BR-033 — Danh sách chương trình

- **Actor/điều kiện:** Theo view; xem 05; theo decorator/CBV thực tế.
- **Luồng chính:** Đọc dữ liệu/điều kiện trong handler; render HTML hoặc response chuyên biệt.
- **Ngoại lệ/quy tắc:** Form không hợp lệ giữ trang/lỗi theo handler; đối tượng không tồn tại có thể trả 404 hoặc exception, tùy hàm lookup. Không áp đặt quy tắc bổ sung.
- **Kết quả:** HTML, redirect, PDF hoặc JSON theo handler; route `/programs/`.
- **Nguồn:** [`course/views.py::ProgramFilterView`](../course/views.py), [`course/urls.py`](../course/urls.py).

### BR-034 — Xem chương trình

- **Actor/điều kiện:** Theo view; xem 05; theo decorator/CBV thực tế.
- **Luồng chính:** Đọc dữ liệu/điều kiện trong handler; render HTML hoặc response chuyên biệt.
- **Ngoại lệ/quy tắc:** Form không hợp lệ giữ trang/lỗi theo handler; đối tượng không tồn tại có thể trả 404 hoặc exception, tùy hàm lookup. Không áp đặt quy tắc bổ sung.
- **Kết quả:** HTML, redirect, PDF hoặc JSON theo handler; route `/programs/<int:pk>/detail/`.
- **Nguồn:** [`course/views.py::program_detail`](../course/views.py), [`course/urls.py`](../course/urls.py).

### BR-035 — Thêm chương trình

- **Actor/điều kiện:** Giảng viên/Admin; theo decorator/CBV thực tế.
- **Luồng chính:** GET hiển thị form; POST validate/lưu; trả form lỗi hoặc redirect theo view.
- **Ngoại lệ/quy tắc:** Form không hợp lệ giữ trang/lỗi theo handler; đối tượng không tồn tại có thể trả 404 hoặc exception, tùy hàm lookup. Không áp đặt quy tắc bổ sung.
- **Kết quả:** HTML, redirect, PDF hoặc JSON theo handler; route `/programs/add/`.
- **Nguồn:** [`course/views.py::program_add`](../course/views.py), [`course/urls.py`](../course/urls.py).

### BR-036 — Sửa chương trình

- **Actor/điều kiện:** Giảng viên/Admin; theo decorator/CBV thực tế.
- **Luồng chính:** GET hiển thị form; POST validate/lưu; trả form lỗi hoặc redirect theo view.
- **Ngoại lệ/quy tắc:** Form không hợp lệ giữ trang/lỗi theo handler; đối tượng không tồn tại có thể trả 404 hoặc exception, tùy hàm lookup. Không áp đặt quy tắc bổ sung.
- **Kết quả:** HTML, redirect, PDF hoặc JSON theo handler; route `/programs/<int:pk>/edit/`.
- **Nguồn:** [`course/views.py::program_edit`](../course/views.py), [`course/urls.py`](../course/urls.py).

### BR-037 — Xóa chương trình

- **Actor/điều kiện:** Giảng viên/Admin; theo decorator/CBV thực tế.
- **Luồng chính:** Nhận đối tượng/ID; xác nhận hoặc POST theo view; xóa/hủy; redirect hoặc thông báo.
- **Ngoại lệ/quy tắc:** Form không hợp lệ giữ trang/lỗi theo handler; đối tượng không tồn tại có thể trả 404 hoặc exception, tùy hàm lookup. Không áp đặt quy tắc bổ sung.
- **Kết quả:** HTML, redirect, PDF hoặc JSON theo handler; route `/programs/<int:pk>/delete/`.
- **Nguồn:** [`course/views.py::program_delete`](../course/views.py), [`course/urls.py`](../course/urls.py).

### BR-038 — Xem học phần

- **Actor/điều kiện:** Theo view; xem 05; theo decorator/CBV thực tế.
- **Luồng chính:** Đọc dữ liệu/điều kiện trong handler; render HTML hoặc response chuyên biệt.
- **Ngoại lệ/quy tắc:** Form không hợp lệ giữ trang/lỗi theo handler; đối tượng không tồn tại có thể trả 404 hoặc exception, tùy hàm lookup. Không áp đặt quy tắc bổ sung.
- **Kết quả:** HTML, redirect, PDF hoặc JSON theo handler; route `/programs/course/<slug>/detail/`.
- **Nguồn:** [`course/views.py::course_single`](../course/views.py), [`course/urls.py`](../course/urls.py).

### BR-039 — Thêm học phần

- **Actor/điều kiện:** Giảng viên/Admin; theo decorator/CBV thực tế.
- **Luồng chính:** GET hiển thị form; POST validate/lưu; trả form lỗi hoặc redirect theo view.
- **Ngoại lệ/quy tắc:** Form không hợp lệ giữ trang/lỗi theo handler; đối tượng không tồn tại có thể trả 404 hoặc exception, tùy hàm lookup. Không áp đặt quy tắc bổ sung.
- **Kết quả:** HTML, redirect, PDF hoặc JSON theo handler; route `/programs/<int:pk>/course/add/`.
- **Nguồn:** [`course/views.py::course_add`](../course/views.py), [`course/urls.py`](../course/urls.py).

### BR-040 — Sửa học phần

- **Actor/điều kiện:** Giảng viên/Admin; theo decorator/CBV thực tế.
- **Luồng chính:** GET hiển thị form; POST validate/lưu; trả form lỗi hoặc redirect theo view.
- **Ngoại lệ/quy tắc:** Form không hợp lệ giữ trang/lỗi theo handler; đối tượng không tồn tại có thể trả 404 hoặc exception, tùy hàm lookup. Không áp đặt quy tắc bổ sung.
- **Kết quả:** HTML, redirect, PDF hoặc JSON theo handler; route `/programs/course/<slug>/edit/`.
- **Nguồn:** [`course/views.py::course_edit`](../course/views.py), [`course/urls.py`](../course/urls.py).

### BR-041 — Xóa học phần

- **Actor/điều kiện:** Giảng viên/Admin; theo decorator/CBV thực tế.
- **Luồng chính:** Nhận đối tượng/ID; xác nhận hoặc POST theo view; xóa/hủy; redirect hoặc thông báo.
- **Ngoại lệ/quy tắc:** Form không hợp lệ giữ trang/lỗi theo handler; đối tượng không tồn tại có thể trả 404 hoặc exception, tùy hàm lookup. Không áp đặt quy tắc bổ sung.
- **Kết quả:** HTML, redirect, PDF hoặc JSON theo handler; route `/programs/course/delete/<slug>/`.
- **Nguồn:** [`course/views.py::course_delete`](../course/views.py), [`course/urls.py`](../course/urls.py).

### BR-042 — Phân công giảng viên

- **Actor/điều kiện:** Theo view; xem 05; theo decorator/CBV thực tế.
- **Luồng chính:** Đọc dữ liệu/điều kiện trong handler; render HTML hoặc response chuyên biệt.
- **Ngoại lệ/quy tắc:** Form không hợp lệ giữ trang/lỗi theo handler; đối tượng không tồn tại có thể trả 404 hoặc exception, tùy hàm lookup. Không áp đặt quy tắc bổ sung.
- **Kết quả:** HTML, redirect, PDF hoặc JSON theo handler; route `/programs/course/assign/`.
- **Nguồn:** [`course/views.py::CourseAllocationFormView`](../course/views.py), [`course/urls.py`](../course/urls.py).

### BR-043 — Xem phân công

- **Actor/điều kiện:** Theo view; xem 05; theo decorator/CBV thực tế.
- **Luồng chính:** Đọc dữ liệu/điều kiện trong handler; render HTML hoặc response chuyên biệt.
- **Ngoại lệ/quy tắc:** Form không hợp lệ giữ trang/lỗi theo handler; đối tượng không tồn tại có thể trả 404 hoặc exception, tùy hàm lookup. Không áp đặt quy tắc bổ sung.
- **Kết quả:** HTML, redirect, PDF hoặc JSON theo handler; route `/programs/course/allocated/`.
- **Nguồn:** [`course/views.py::CourseAllocationFilterView`](../course/views.py), [`course/urls.py`](../course/urls.py).

### BR-044 — Sửa phân công

- **Actor/điều kiện:** Giảng viên/Admin; theo decorator/CBV thực tế.
- **Luồng chính:** GET hiển thị form; POST validate/lưu; trả form lỗi hoặc redirect theo view.
- **Ngoại lệ/quy tắc:** Form không hợp lệ giữ trang/lỗi theo handler; đối tượng không tồn tại có thể trả 404 hoặc exception, tùy hàm lookup. Không áp đặt quy tắc bổ sung.
- **Kết quả:** HTML, redirect, PDF hoặc JSON theo handler; route `/programs/allocated_course/<int:pk>/edit/`.
- **Nguồn:** [`course/views.py::edit_allocated_course`](../course/views.py), [`course/urls.py`](../course/urls.py).

### BR-045 — Hủy phân công

- **Actor/điều kiện:** Giảng viên/Admin; theo decorator/CBV thực tế.
- **Luồng chính:** Nhận đối tượng/ID; xác nhận hoặc POST theo view; xóa/hủy; redirect hoặc thông báo.
- **Ngoại lệ/quy tắc:** Form không hợp lệ giữ trang/lỗi theo handler; đối tượng không tồn tại có thể trả 404 hoặc exception, tùy hàm lookup. Không áp đặt quy tắc bổ sung.
- **Kết quả:** HTML, redirect, PDF hoặc JSON theo handler; route `/programs/course/<int:pk>/deallocate/`.
- **Nguồn:** [`course/views.py::deallocate_course`](../course/views.py), [`course/urls.py`](../course/urls.py).

### BR-046 — Tải tài liệu

- **Actor/điều kiện:** Giảng viên/Admin; theo decorator/CBV thực tế.
- **Luồng chính:** GET hiển thị form; POST validate/lưu; trả form lỗi hoặc redirect theo view.
- **Ngoại lệ/quy tắc:** Form không hợp lệ giữ trang/lỗi theo handler; đối tượng không tồn tại có thể trả 404 hoặc exception, tùy hàm lookup. Không áp đặt quy tắc bổ sung.
- **Kết quả:** HTML, redirect, PDF hoặc JSON theo handler; route `/programs/course/<slug>/documentations/upload/`.
- **Nguồn:** [`course/views.py::handle_file_upload`](../course/views.py), [`course/urls.py`](../course/urls.py).

### BR-047 — Sửa tài liệu

- **Actor/điều kiện:** Giảng viên/Admin; theo decorator/CBV thực tế.
- **Luồng chính:** GET hiển thị form; POST validate/lưu; trả form lỗi hoặc redirect theo view.
- **Ngoại lệ/quy tắc:** Form không hợp lệ giữ trang/lỗi theo handler; đối tượng không tồn tại có thể trả 404 hoặc exception, tùy hàm lookup. Không áp đặt quy tắc bổ sung.
- **Kết quả:** HTML, redirect, PDF hoặc JSON theo handler; route `/programs/course/<slug>/documentations/<int:file_id>/edit/`.
- **Nguồn:** [`course/views.py::handle_file_edit`](../course/views.py), [`course/urls.py`](../course/urls.py).

### BR-048 — Xóa tài liệu

- **Actor/điều kiện:** Giảng viên/Admin; theo decorator/CBV thực tế.
- **Luồng chính:** Nhận đối tượng/ID; xác nhận hoặc POST theo view; xóa/hủy; redirect hoặc thông báo.
- **Ngoại lệ/quy tắc:** Form không hợp lệ giữ trang/lỗi theo handler; đối tượng không tồn tại có thể trả 404 hoặc exception, tùy hàm lookup. Không áp đặt quy tắc bổ sung.
- **Kết quả:** HTML, redirect, PDF hoặc JSON theo handler; route `/programs/course/<slug>/documentations/<int:file_id>/delete/`.
- **Nguồn:** [`course/views.py::handle_file_delete`](../course/views.py), [`course/urls.py`](../course/urls.py).

### BR-049 — Tải video

- **Actor/điều kiện:** Giảng viên/Admin; theo decorator/CBV thực tế.
- **Luồng chính:** GET hiển thị form; POST validate/lưu; trả form lỗi hoặc redirect theo view.
- **Ngoại lệ/quy tắc:** Form không hợp lệ giữ trang/lỗi theo handler; đối tượng không tồn tại có thể trả 404 hoặc exception, tùy hàm lookup. Không áp đặt quy tắc bổ sung.
- **Kết quả:** HTML, redirect, PDF hoặc JSON theo handler; route `/programs/course/<slug>/video_tutorials/upload/`.
- **Nguồn:** [`course/views.py::handle_video_upload`](../course/views.py), [`course/urls.py`](../course/urls.py).

### BR-050 — Xem video

- **Actor/điều kiện:** Theo view; xem 05; theo decorator/CBV thực tế.
- **Luồng chính:** Đọc dữ liệu/điều kiện trong handler; render HTML hoặc response chuyên biệt.
- **Ngoại lệ/quy tắc:** Form không hợp lệ giữ trang/lỗi theo handler; đối tượng không tồn tại có thể trả 404 hoặc exception, tùy hàm lookup. Không áp đặt quy tắc bổ sung.
- **Kết quả:** HTML, redirect, PDF hoặc JSON theo handler; route `/programs/course/<slug>/video_tutorials/<video_slug>/detail/`.
- **Nguồn:** [`course/views.py::handle_video_single`](../course/views.py), [`course/urls.py`](../course/urls.py).

### BR-051 — Sửa video

- **Actor/điều kiện:** Giảng viên/Admin; theo decorator/CBV thực tế.
- **Luồng chính:** GET hiển thị form; POST validate/lưu; trả form lỗi hoặc redirect theo view.
- **Ngoại lệ/quy tắc:** Form không hợp lệ giữ trang/lỗi theo handler; đối tượng không tồn tại có thể trả 404 hoặc exception, tùy hàm lookup. Không áp đặt quy tắc bổ sung.
- **Kết quả:** HTML, redirect, PDF hoặc JSON theo handler; route `/programs/course/<slug>/video_tutorials/<video_slug>/edit/`.
- **Nguồn:** [`course/views.py::handle_video_edit`](../course/views.py), [`course/urls.py`](../course/urls.py).

### BR-052 — Xóa video

- **Actor/điều kiện:** Giảng viên/Admin; theo decorator/CBV thực tế.
- **Luồng chính:** Nhận đối tượng/ID; xác nhận hoặc POST theo view; xóa/hủy; redirect hoặc thông báo.
- **Ngoại lệ/quy tắc:** Form không hợp lệ giữ trang/lỗi theo handler; đối tượng không tồn tại có thể trả 404 hoặc exception, tùy hàm lookup. Không áp đặt quy tắc bổ sung.
- **Kết quả:** HTML, redirect, PDF hoặc JSON theo handler; route `/programs/course/<slug>/video_tutorials/<video_slug>/delete/`.
- **Nguồn:** [`course/views.py::handle_video_delete`](../course/views.py), [`course/urls.py`](../course/urls.py).

### BR-053 — Đăng ký học phần

- **Actor/điều kiện:** Sinh viên/Admin; theo decorator/CBV thực tế.
- **Luồng chính:** Đọc dữ liệu/điều kiện trong handler; render HTML hoặc response chuyên biệt.
- **Ngoại lệ/quy tắc:** Nếu chưa có học kỳ hiện hành, hiển thị thông báo; POST hiện lấy ID từ khóa của POST và tạo TakenCourse, chưa kiểm tra lại điều kiện GET.
- **Kết quả:** HTML, redirect, PDF hoặc JSON theo handler; route `/programs/course/registration/`.
- **Nguồn:** [`course/views.py::course_registration`](../course/views.py), [`course/urls.py`](../course/urls.py).

### BR-054 — Hủy học phần

- **Actor/điều kiện:** Sinh viên/Admin; theo decorator/CBV thực tế.
- **Luồng chính:** Nhận đối tượng/ID; xác nhận hoặc POST theo view; xóa/hủy; redirect hoặc thông báo.
- **Ngoại lệ/quy tắc:** POST danh sách course_ids; xóa TakenCourse phù hợp. Không có GET response tường minh.
- **Kết quả:** HTML, redirect, PDF hoặc JSON theo handler; route `/programs/course/drop/`.
- **Nguồn:** [`course/views.py::course_drop`](../course/views.py), [`course/urls.py`](../course/urls.py).

### BR-055 — Xem học phần của tôi

- **Actor/điều kiện:** Theo view; xem 05; theo decorator/CBV thực tế.
- **Luồng chính:** Đọc dữ liệu/điều kiện trong handler; render HTML hoặc response chuyên biệt.
- **Ngoại lệ/quy tắc:** Form không hợp lệ giữ trang/lỗi theo handler; đối tượng không tồn tại có thể trả 404 hoặc exception, tùy hàm lookup. Không áp đặt quy tắc bổ sung.
- **Kết quả:** HTML, redirect, PDF hoặc JSON theo handler; route `/programs/my_courses/`.
- **Nguồn:** [`course/views.py::user_course_list`](../course/views.py), [`course/urls.py`](../course/urls.py).

### BR-056 — Chọn môn nhập điểm

- **Actor/điều kiện:** Giảng viên/Admin; theo decorator/CBV thực tế.
- **Luồng chính:** GET hiển thị form; POST validate/lưu; trả form lỗi hoặc redirect theo view.
- **Ngoại lệ/quy tắc:** Cần session và semester hiện hành; nếu thiếu hiển thị thông báo.
- **Kết quả:** HTML, redirect, PDF hoặc JSON theo handler; route `/result/manage-score/`.
- **Nguồn:** [`result/views.py::add_score`](../result/views.py), [`result/urls.py`](../result/urls.py).

### BR-057 — Nhập điểm thành phần

- **Actor/điều kiện:** Giảng viên/Admin; theo decorator/CBV thực tế.
- **Luồng chính:** GET hiển thị form; POST validate/lưu; trả form lỗi hoặc redirect theo view.
- **Ngoại lệ/quy tắc:** POST mỗi key là TakenCourse.id, mỗi value là 5 điểm; tính total/grade/point/GPA; source có catch-all except.
- **Kết quả:** HTML, redirect, PDF hoặc JSON theo handler; route `/result/manage-score/<int:id>/`.
- **Nguồn:** [`result/views.py::add_score_for`](../result/views.py), [`result/urls.py`](../result/urls.py).

### BR-058 — Xem điểm tổng kết

- **Actor/điều kiện:** Sinh viên/Admin; theo decorator/CBV thực tế.
- **Luồng chính:** Lấy dữ liệu theo user/kỳ/môn; tính hoặc trình bày; trả HTML/PDF.
- **Ngoại lệ/quy tắc:** Form không hợp lệ giữ trang/lỗi theo handler; đối tượng không tồn tại có thể trả 404 hoặc exception, tùy hàm lookup. Không áp đặt quy tắc bổ sung.
- **Kết quả:** HTML, redirect, PDF hoặc JSON theo handler; route `/result/grade/`.
- **Nguồn:** [`result/views.py::grade_result`](../result/views.py), [`result/urls.py`](../result/urls.py).

### BR-059 — Xem điểm đánh giá

- **Actor/điều kiện:** Sinh viên/Admin; theo decorator/CBV thực tế.
- **Luồng chính:** Lấy dữ liệu theo user/kỳ/môn; tính hoặc trình bày; trả HTML/PDF.
- **Ngoại lệ/quy tắc:** Form không hợp lệ giữ trang/lỗi theo handler; đối tượng không tồn tại có thể trả 404 hoặc exception, tùy hàm lookup. Không áp đặt quy tắc bổ sung.
- **Kết quả:** HTML, redirect, PDF hoặc JSON theo handler; route `/result/assessment/`.
- **Nguồn:** [`result/views.py::assessment_result`](../result/views.py), [`result/urls.py`](../result/urls.py).

### BR-060 — Xuất bảng điểm PDF

- **Actor/điều kiện:** Giảng viên/Admin; theo decorator/CBV thực tế.
- **Luồng chính:** Lấy dữ liệu theo user/kỳ/môn; tính hoặc trình bày; trả HTML/PDF.
- **Ngoại lệ/quy tắc:** Form không hợp lệ giữ trang/lỗi theo handler; đối tượng không tồn tại có thể trả 404 hoặc exception, tùy hàm lookup. Không áp đặt quy tắc bổ sung.
- **Kết quả:** HTML, redirect, PDF hoặc JSON theo handler; route `/result/result/print/<int:id>/`.
- **Nguồn:** [`result/views.py::result_sheet_pdf_view`](../result/views.py), [`result/urls.py`](../result/urls.py).

### BR-061 — Xuất phiếu đăng ký PDF

- **Actor/điều kiện:** Sinh viên/Admin; theo decorator/CBV thực tế.
- **Luồng chính:** Đọc dữ liệu/điều kiện trong handler; render HTML hoặc response chuyên biệt.
- **Ngoại lệ/quy tắc:** Form không hợp lệ giữ trang/lỗi theo handler; đối tượng không tồn tại có thể trả 404 hoặc exception, tùy hàm lookup. Không áp đặt quy tắc bổ sung.
- **Kết quả:** HTML, redirect, PDF hoặc JSON theo handler; route `/result/registration/form/`.
- **Nguồn:** [`result/views.py::course_registration_form`](../result/views.py), [`result/urls.py`](../result/urls.py).

### BR-062 — Xem danh sách quiz

- **Actor/điều kiện:** Theo view; xem 05; theo decorator/CBV thực tế.
- **Luồng chính:** Đọc dữ liệu/điều kiện trong handler; render HTML hoặc response chuyên biệt.
- **Ngoại lệ/quy tắc:** Form không hợp lệ giữ trang/lỗi theo handler; đối tượng không tồn tại có thể trả 404 hoặc exception, tùy hàm lookup. Không áp đặt quy tắc bổ sung.
- **Kết quả:** HTML, redirect, PDF hoặc JSON theo handler; route `/quiz/<slug>/quizzes/`.
- **Nguồn:** [`quiz/views.py::quiz_list`](../quiz/views.py), [`quiz/urls.py`](../quiz/urls.py).

### BR-063 — Xem tiến độ quiz

- **Actor/điều kiện:** Theo view; xem 05; theo decorator/CBV thực tế.
- **Luồng chính:** Đọc dữ liệu/điều kiện trong handler; render HTML hoặc response chuyên biệt.
- **Ngoại lệ/quy tắc:** Progress.list_all_cat_scores() trả {}; thống kê category chưa thực hiện.
- **Kết quả:** HTML, redirect, PDF hoặc JSON theo handler; route `/quiz/progress/`.
- **Nguồn:** [`quiz/views.py::QuizUserProgressView`](../quiz/views.py), [`quiz/urls.py`](../quiz/urls.py).

### BR-064 — Xem bài quiz đã nộp

- **Actor/điều kiện:** Giảng viên/Admin; theo decorator/CBV thực tế.
- **Luồng chính:** Đọc dữ liệu/điều kiện trong handler; render HTML hoặc response chuyên biệt.
- **Ngoại lệ/quy tắc:** Form không hợp lệ giữ trang/lỗi theo handler; đối tượng không tồn tại có thể trả 404 hoặc exception, tùy hàm lookup. Không áp đặt quy tắc bổ sung.
- **Kết quả:** HTML, redirect, PDF hoặc JSON theo handler; route `/quiz/marking_list/`.
- **Nguồn:** [`quiz/views.py::QuizMarkingList`](../quiz/views.py), [`quiz/urls.py`](../quiz/urls.py).

### BR-065 — Đánh dấu/chấm bài quiz

- **Actor/điều kiện:** Giảng viên/Admin; theo decorator/CBV thực tế.
- **Luồng chính:** Đọc dữ liệu/điều kiện trong handler; render HTML hoặc response chuyên biệt.
- **Ngoại lệ/quy tắc:** Form không hợp lệ giữ trang/lỗi theo handler; đối tượng không tồn tại có thể trả 404 hoặc exception, tùy hàm lookup. Không áp đặt quy tắc bổ sung.
- **Kết quả:** HTML, redirect, PDF hoặc JSON theo handler; route `/quiz/marking/<int:pk>/`.
- **Nguồn:** [`quiz/views.py::QuizMarkingDetail`](../quiz/views.py), [`quiz/urls.py`](../quiz/urls.py).

### BR-066 — Làm bài quiz

- **Actor/điều kiện:** Theo view; xem 05; theo decorator/CBV thực tế.
- **Luồng chính:** Đọc dữ liệu/điều kiện trong handler; render HTML hoặc response chuyên biệt.
- **Ngoại lệ/quy tắc:** Chỉ user đăng nhập; quiz phải có câu hỏi; single_attempt chặn lượt hoàn thành; lượt chưa xong được tiếp tục.
- **Kết quả:** HTML, redirect, PDF hoặc JSON theo handler; route `/quiz/<int:pk>/<slug>/take/`.
- **Nguồn:** [`quiz/views.py::QuizTake`](../quiz/views.py), [`quiz/urls.py`](../quiz/urls.py).

### BR-067 — Tạo quiz

- **Actor/điều kiện:** Theo view; xem 05; theo decorator/CBV thực tế.
- **Luồng chính:** Đọc dữ liệu/điều kiện trong handler; render HTML hoặc response chuyên biệt.
- **Ngoại lệ/quy tắc:** Form không hợp lệ giữ trang/lỗi theo handler; đối tượng không tồn tại có thể trả 404 hoặc exception, tùy hàm lookup. Không áp đặt quy tắc bổ sung.
- **Kết quả:** HTML, redirect, PDF hoặc JSON theo handler; route `/quiz/<slug>/quiz_add/`.
- **Nguồn:** [`quiz/views.py::QuizCreateView`](../quiz/views.py), [`quiz/urls.py`](../quiz/urls.py).

### BR-068 — Sửa quiz

- **Actor/điều kiện:** Theo view; xem 05; theo decorator/CBV thực tế.
- **Luồng chính:** Đọc dữ liệu/điều kiện trong handler; render HTML hoặc response chuyên biệt.
- **Ngoại lệ/quy tắc:** Form không hợp lệ giữ trang/lỗi theo handler; đối tượng không tồn tại có thể trả 404 hoặc exception, tùy hàm lookup. Không áp đặt quy tắc bổ sung.
- **Kết quả:** HTML, redirect, PDF hoặc JSON theo handler; route `/quiz/<slug>/<int:pk>/add/`.
- **Nguồn:** [`quiz/views.py::QuizUpdateView`](../quiz/views.py), [`quiz/urls.py`](../quiz/urls.py).

### BR-069 — Xóa quiz

- **Actor/điều kiện:** Giảng viên/Admin; theo decorator/CBV thực tế.
- **Luồng chính:** Nhận đối tượng/ID; xác nhận hoặc POST theo view; xóa/hủy; redirect hoặc thông báo.
- **Ngoại lệ/quy tắc:** Form không hợp lệ giữ trang/lỗi theo handler; đối tượng không tồn tại có thể trả 404 hoặc exception, tùy hàm lookup. Không áp đặt quy tắc bổ sung.
- **Kết quả:** HTML, redirect, PDF hoặc JSON theo handler; route `/quiz/<slug>/<int:pk>/delete/`.
- **Nguồn:** [`quiz/views.py::quiz_delete`](../quiz/views.py), [`quiz/urls.py`](../quiz/urls.py).

### BR-070 — Tạo câu hỏi trắc nghiệm

- **Actor/điều kiện:** Theo view; xem 05; theo decorator/CBV thực tế.
- **Luồng chính:** Đọc dữ liệu/điều kiện trong handler; render HTML hoặc response chuyên biệt.
- **Ngoại lệ/quy tắc:** Formset yêu cầu >=2 lựa chọn và đúng một đáp án đúng.
- **Kết quả:** HTML, redirect, PDF hoặc JSON theo handler; route `/quiz/mc-question/add/<slug>/<int:quiz_id>/`.
- **Nguồn:** [`quiz/views.py::MCQuestionCreate`](../quiz/views.py), [`quiz/urls.py`](../quiz/urls.py).

### BR-071 — Xem lựa chọn thanh toán

- **Actor/điều kiện:** Chưa kiểm soát rõ; theo decorator/CBV thực tế.
- **Luồng chính:** Đọc dữ liệu/điều kiện trong handler; render HTML hoặc response chuyên biệt.
- **Ngoại lệ/quy tắc:** Form không hợp lệ giữ trang/lỗi theo handler; đối tượng không tồn tại có thể trả 404 hoặc exception, tùy hàm lookup. Không áp đặt quy tắc bổ sung.
- **Kết quả:** HTML, redirect, PDF hoặc JSON theo handler; route `/payments/`.
- **Nguồn:** [`payments/views.py::PaymentGetwaysView`](../payments/views.py), [`payments/urls.py`](../payments/urls.py).

### BR-072 — Xem trang PayPal mẫu

- **Actor/điều kiện:** Chưa kiểm soát rõ; theo decorator/CBV thực tế.
- **Luồng chính:** Đọc dữ liệu/điều kiện trong handler; render HTML hoặc response chuyên biệt.
- **Ngoại lệ/quy tắc:** Form không hợp lệ giữ trang/lỗi theo handler; đối tượng không tồn tại có thể trả 404 hoặc exception, tùy hàm lookup. Không áp đặt quy tắc bổ sung.
- **Kết quả:** HTML, redirect, PDF hoặc JSON theo handler; route `/payments/paypal/`.
- **Nguồn:** [`payments/views.py::payment_paypal`](../payments/views.py), [`payments/urls.py`](../payments/urls.py).

### BR-073 — Xem trang Stripe mẫu

- **Actor/điều kiện:** Chưa kiểm soát rõ; theo decorator/CBV thực tế.
- **Luồng chính:** Đọc dữ liệu/điều kiện trong handler; render HTML hoặc response chuyên biệt.
- **Ngoại lệ/quy tắc:** Form không hợp lệ giữ trang/lỗi theo handler; đối tượng không tồn tại có thể trả 404 hoặc exception, tùy hàm lookup. Không áp đặt quy tắc bổ sung.
- **Kết quả:** HTML, redirect, PDF hoặc JSON theo handler; route `/payments/stripe/`.
- **Nguồn:** [`payments/views.py::payment_stripe`](../payments/views.py), [`payments/urls.py`](../payments/urls.py).

### BR-074 — Xem trang Coinbase mẫu

- **Actor/điều kiện:** Chưa kiểm soát rõ; theo decorator/CBV thực tế.
- **Luồng chính:** Đọc dữ liệu/điều kiện trong handler; render HTML hoặc response chuyên biệt.
- **Ngoại lệ/quy tắc:** Form không hợp lệ giữ trang/lỗi theo handler; đối tượng không tồn tại có thể trả 404 hoặc exception, tùy hàm lookup. Không áp đặt quy tắc bổ sung.
- **Kết quả:** HTML, redirect, PDF hoặc JSON theo handler; route `/payments/coinbase/`.
- **Nguồn:** [`payments/views.py::payment_coinbase`](../payments/views.py), [`payments/urls.py`](../payments/urls.py).

### BR-075 — Xem trang Paylike mẫu

- **Actor/điều kiện:** Chưa kiểm soát rõ; theo decorator/CBV thực tế.
- **Luồng chính:** Đọc dữ liệu/điều kiện trong handler; render HTML hoặc response chuyên biệt.
- **Ngoại lệ/quy tắc:** Form không hợp lệ giữ trang/lỗi theo handler; đối tượng không tồn tại có thể trả 404 hoặc exception, tùy hàm lookup. Không áp đặt quy tắc bổ sung.
- **Kết quả:** HTML, redirect, PDF hoặc JSON theo handler; route `/payments/paylike/`.
- **Nguồn:** [`payments/views.py::payment_paylike`](../payments/views.py), [`payments/urls.py`](../payments/urls.py).

### BR-076 — Gửi lệnh Stripe mẫu

- **Actor/điều kiện:** Chưa kiểm soát rõ; theo decorator/CBV thực tế.
- **Luồng chính:** Đọc dữ liệu/điều kiện trong handler; render HTML hoặc response chuyên biệt.
- **Ngoại lệ/quy tắc:** Giá trị charge cố định 500 EUR, redirect tên 'completed' không có trong routes.
- **Kết quả:** HTML, redirect, PDF hoặc JSON theo handler; route `/payments/stripe-charge/`.
- **Nguồn:** [`payments/views.py::stripe_charge`](../payments/views.py), [`payments/urls.py`](../payments/urls.py).

### BR-077 — Gửi lệnh GoPay mẫu

- **Actor/điều kiện:** Chưa kiểm soát rõ; theo decorator/CBV thực tế.
- **Luồng chính:** Đọc dữ liệu/điều kiện trong handler; render HTML hoặc response chuyên biệt.
- **Ngoại lệ/quy tắc:** Form không hợp lệ giữ trang/lỗi theo handler; đối tượng không tồn tại có thể trả 404 hoặc exception, tùy hàm lookup. Không áp đặt quy tắc bổ sung.
- **Kết quả:** HTML, redirect, PDF hoặc JSON theo handler; route `/payments/gopay-charge/`.
- **Nguồn:** [`payments/views.py::gopay_charge`](../payments/views.py), [`payments/urls.py`](../payments/urls.py).

### BR-078 — Xem thông báo thanh toán

- **Actor/điều kiện:** Chưa kiểm soát rõ; theo decorator/CBV thực tế.
- **Luồng chính:** Đọc dữ liệu/điều kiện trong handler; render HTML hoặc response chuyên biệt.
- **Ngoại lệ/quy tắc:** Form không hợp lệ giữ trang/lỗi theo handler; đối tượng không tồn tại có thể trả 404 hoặc exception, tùy hàm lookup. Không áp đặt quy tắc bổ sung.
- **Kết quả:** HTML, redirect, PDF hoặc JSON theo handler; route `/payments/payment-succeed/`.
- **Nguồn:** [`payments/views.py::payment_succeed`](../payments/views.py), [`payments/urls.py`](../payments/urls.py).

### BR-079 — Đánh dấu hoàn tất thanh toán mẫu

- **Actor/điều kiện:** Chưa kiểm soát rõ; theo decorator/CBV thực tế.
- **Luồng chính:** Đọc dữ liệu/điều kiện trong handler; render HTML hoặc response chuyên biệt.
- **Ngoại lệ/quy tắc:** request.is_ajax() là API cũ; dùng invoice_session như id dù create_invoice lưu invoice_code.
- **Kết quả:** HTML, redirect, PDF hoặc JSON theo handler; route `/payments/complete/`.
- **Nguồn:** [`payments/views.py::paymentComplete`](../payments/views.py), [`payments/urls.py`](../payments/urls.py).

### BR-080 — Tạo/xem hóa đơn

- **Actor/điều kiện:** Chưa kiểm soát rõ; theo decorator/CBV thực tế.
- **Luồng chính:** GET hiển thị form; POST validate/lưu; trả form lỗi hoặc redirect theo view.
- **Ngoại lệ/quy tắc:** Form không hợp lệ giữ trang/lỗi theo handler; đối tượng không tồn tại có thể trả 404 hoặc exception, tùy hàm lookup. Không áp đặt quy tắc bổ sung.
- **Kết quả:** HTML, redirect, PDF hoặc JSON theo handler; route `/payments/create-invoice/`.
- **Nguồn:** [`payments/views.py::create_invoice`](../payments/views.py), [`payments/urls.py`](../payments/urls.py).

### BR-081 — Xem hóa đơn theo mã

- **Actor/điều kiện:** Chưa kiểm soát rõ; theo decorator/CBV thực tế.
- **Luồng chính:** Đọc dữ liệu/điều kiện trong handler; render HTML hoặc response chuyên biệt.
- **Ngoại lệ/quy tắc:** URL nhận <int:id> nhưng handler nhận slug: lỗi hiện hữu.
- **Kết quả:** HTML, redirect, PDF hoặc JSON theo handler; route `/payments/invoice-detail/<int:id>/`.
- **Nguồn:** [`payments/views.py::invoice_detail`](../payments/views.py), [`payments/urls.py`](../payments/urls.py).

### BR-082 — Tìm kiếm toàn hệ thống

- **Actor/điều kiện:** Theo view; xem 05; theo decorator/CBV thực tế.
- **Luồng chính:** Đọc dữ liệu/điều kiện trong handler; render HTML hoặc response chuyên biệt.
- **Ngoại lệ/quy tắc:** Form không hợp lệ giữ trang/lỗi theo handler; đối tượng không tồn tại có thể trả 404 hoặc exception, tùy hàm lookup. Không áp đặt quy tắc bổ sung.
- **Kết quả:** HTML, redirect, PDF hoặc JSON theo handler; route `/search/`.
- **Nguồn:** [`search/views.py::SearchView`](../search/views.py), [`search/urls.py`](../search/urls.py).

## Quy tắc xuyên module

- Điểm tổng = assignment + mid_exam + quiz + attendance + final_exam; grade theo ngưỡng 90/85/80/75/70/65/60/55/50/45/0, point = tín chỉ × điểm quy đổi; PASS trừ F/NG. [`result/models.py`](../result/models.py)
- GPA là trung bình trọng số theo tín chỉ cho kỳ hiện hành; CGPA trên toàn bộ TakenCourse của sinh viên. [`result/models.py`](../result/models.py)
- Quiz có pass_mark 0–100, random_order, answers_at_end, exam_paper, single_attempt; lựa chọn trắc nghiệm có đúng một đáp án. [`quiz/models.py`](../quiz/models.py), [`quiz/forms.py`](../quiz/forms.py)
- Tính năng TODO không được đưa thành BR đã hoàn thành. [`TODO.md`](../TODO.md)


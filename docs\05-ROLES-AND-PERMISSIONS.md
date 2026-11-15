# Vai trò và phân quyền

> Baseline: [SkyCascade/SkyLearn](https://github.com/SkyCascade/SkyLearn), nhánh `main`, commit `d57f57bd505447b59fdf82b16469494443cafe0c`. Đây là bản kiểm kê mã nguồn, không phải đặc tả tính năng mới. Trạng thái tải source và kiểm thử: [11-SETUP-AND-DEPLOYMENT.md](11-SETUP-AND-DEPLOYMENT.md).

`accounts.User` dùng các flag `is_student`, `is_lecturer`, `is_parent`, `is_dep_head`, `is_superuser`; flag có thể đồng thời true (không có constraint loại trừ). Decorators `admin_required`, `lecturer_required`, `student_required` ở [`accounts/decorators.py`](../accounts/decorators.py) redirect `/` khi không hợp lệ; hai decorator sau cho superuser đi qua.

Có 5 loại vai trò được biểu diễn bởi flag/model: admin, giảng viên, sinh viên, phụ huynh, trưởng bộ môn. `User.get_user_role` chỉ trả nhãn cho bốn loại đầu, không xử lý `is_dep_head` và cũng không có fallback cho user không thuộc loại nào; đây là giới hạn hiện hữu của helper, không được suy diễn quyền mới cho trưởng bộ môn.

| Nhóm chức năng | Admin | Giảng viên | Sinh viên | Phụ huynh/trưởng bộ môn |
| --- | --- | --- | --- | --- |
| Dashboard, hồ sơ người khác, CRUD người dùng, PDF danh sách | Có | Không | Không | Không |
| Tin/sự kiện: xem | Có | Có | Có | Theo đăng nhập |
| Tin/sự kiện: thêm | Có | Có | Có | Theo đăng nhập: post_add thiếu role decorator |
| Tin/sự kiện: sửa/xóa | Có | Có | Không | Không |
| Chương trình/môn: xem | Theo login / CBV | Theo login / CBV | Theo login / CBV | Theo login / CBV |
| Chương trình/môn: CRUD, tài liệu/video | Có | Có | Không | Không |
| Phân công: tạo/xem | CBV thiếu role decorator | CBV thiếu role decorator | CBV thiếu role decorator | CBV thiếu role decorator |
| Đăng ký/hủy môn, xem điểm | Có qua student_required, nhưng cần Student record | Không | Có | Không |
| Nhập điểm, PDF bảng điểm | Có | Có | Không | Không |
| Quiz tạo/sửa/câu hỏi | CBV cần kiểm tra từng view | CBV cần kiểm tra từng view | CBV cần kiểm tra từng view | CBV cần kiểm tra từng view |
| Quiz làm bài | Đăng nhập | Đăng nhập | Đăng nhập | Đăng nhập |
| Quiz marking | Có | Có | Không | Không |
| Thanh toán/invoice | Thiếu decorator; không coi là bảo vệ | Thiếu decorator | Thiếu decorator | Thiếu decorator |


**Chính xác hơn:** xem decorators trên từng function/class tại [`accounts/views.py`](../accounts/views.py), [`course/views.py`](../course/views.py), [`quiz/views.py`](../quiz/views.py), [`core/views.py`](../core/views.py). `@login_required` áp dụng nhiều FBV; CBV không đồng đều. `QuizMarkingList/Detail` có login+lecturer; `QuizTake` login. Permission `view_sittings` khai báo trong `Sitting.Meta`, nhưng không thấy guard `permission_required` trên marking views; không coi nó là rào quyền đang được thực thi.

**Frontend mới:** chỉ ẩn/hiện chức năng theo quyền tương ứng backend thực tế, nhưng không thay đổi quyền backend bằng UI. Đánh dấu các route thiếu guard là rủi ro cần quyết định riêng trước khi sửa. Không suy đoán phụ huynh/trưởng bộ môn có dashboard riêng chỉ vì có flag/model.

